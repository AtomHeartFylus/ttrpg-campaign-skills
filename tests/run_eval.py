#!/usr/bin/env python3
"""Set up, run and partly grade the behavioral evals.

    python3 tests/run_eval.py --list
    python3 tests/run_eval.py --setup session-prep            # work copy + the verbatim prompt
    python3 tests/run_eval.py --grade session-prep --work /tmp/eval-session-prep-xxxx
    python3 tests/run_eval.py --setup session-prep --agent 'my-agent-cli --prompt {prompt}'

Half of every rubric is an observable fact about a file ("the frontmatter carries `type:
session-prep`", "no heading contains the word spotlight", "every scene ends with an `If they
derail:` line"). Those boxes are ticked here, from the `eval-spec` block in each eval file.

The other half needs a reader and stays a human box - the runner prints it, never guesses it.
The split is the point: a grader who only has to judge the judgement calls actually runs the
evals, and the mechanical boxes stop rotting silently between models.

The agent under test is never invoked implicitly: give `--agent` a command containing `{prompt}`
(and, if it needs one, `{work}`), or run your harness by hand in the work directory.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from check_contract import utf8_stdout  # noqa: E402  (em-dashes in every fixture filename)
EVALS = os.path.join(HERE, "evals")
RESULTS = os.path.join(HERE, "results")
SPEC = re.compile(r"<!--\s*eval-spec\s*(\{.*?\})\s*-->", re.S)
PROMPT_BLOCK = re.compile(r"Prompt \(verbatim\):\s*\n\s*\n((?:>.*\n?)+)")


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def eval_names():
    return sorted(os.path.splitext(os.path.basename(p))[0]
                  for p in glob.glob(os.path.join(EVALS, "*.md")))


def load_eval(name, scenario=None):
    path = os.path.join(EVALS, name + ".md")
    if not os.path.isfile(path):
        sys.exit("fatal: no eval called %r (try --list)" % name)
    text = read(path)
    m = SPEC.search(text)
    spec = json.loads(m.group(1)) if m else {}
    prompts = [" ".join(ln.lstrip("> ").rstrip() for ln in block.strip().splitlines())
               for block in PROMPT_BLOCK.findall(text)]
    # An eval may hold several scenarios (planning vs. the refusal that matters more). Each is
    # a delta over the file's top-level spec, and picks the prompt it belongs to by index.
    scenarios = spec.pop("scenarios", None)
    if scenarios:
        key = scenario or sorted(scenarios)[0]
        if key not in scenarios:
            sys.exit("fatal: %s has no scenario %r (has: %s)"
                     % (name, key, ", ".join(sorted(scenarios))))
        spec.update(scenarios[key])
        spec["scenario"] = key
        idx = spec.get("prompt_index")
        if idx is not None and idx < len(prompts):
            prompts = [prompts[idx]]
    elif scenario:
        sys.exit("fatal: %s declares no scenarios" % name)
    spec.setdefault("prompts", prompts)
    spec.setdefault("name", name if not scenarios else "%s-%s" % (name, spec["scenario"]))
    spec.setdefault("path", path)
    spec.setdefault("mechanical", [])
    spec.setdefault("fixture", "fixture-campaign")
    return spec, text


def snapshot(base):
    out = {}
    for root, dirs, names in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for n in sorted(names):
            p = os.path.join(root, n)
            rel = os.path.relpath(p, base).replace("\\", "/")
            with open(p, "rb") as fh:
                out[rel] = hashlib.sha256(fh.read()).hexdigest()
    return out


def apply_setup(work, steps):
    done = []
    for step in steps:
        if "delete" in step:
            target = os.path.join(work, step["delete"])
            if os.path.isfile(target):
                os.remove(target)
                done.append("deleted %s" % step["delete"])
            else:
                sys.exit("fatal: setup wants to delete a file that is not there: %s"
                         % step["delete"])
        elif "create" in step:
            # A file whose mere existence is the trap (an audio file nobody consented to).
            c = step["create"]
            target = os.path.join(work, c["file"])
            parent = os.path.dirname(target)
            if parent and not os.path.isdir(parent):
                os.makedirs(parent)
            with open(target, "w", encoding="utf-8", newline="") as fh:
                fh.write(c.get("content", ""))
            done.append("created %s" % c["file"])
        elif "copy" in step:
            c = step["copy"]
            src = os.path.join(HERE, c["from"])
            if not os.path.isfile(src):
                sys.exit("fatal: setup wants to copy a file that is not there: %s" % c["from"])
            target = os.path.join(work, c["to"])
            parent = os.path.dirname(target)
            if parent and not os.path.isdir(parent):
                os.makedirs(parent)
            shutil.copyfile(src, target)
            done.append("copied %s -> %s" % (c["from"], c["to"]))
        elif "replace" in step:
            r = step["replace"]
            target = os.path.join(work, r["file"])
            src = read(target)
            if r["old"] not in src:
                sys.exit("fatal: setup anchor missing in %s: %r" % (r["file"], r["old"]))
            with open(target, "w", encoding="utf-8", newline="") as fh:
                fh.write(src.replace(r["old"], r["new"], 1))
            done.append("edited %s" % r["file"])
        else:
            sys.exit("fatal: unknown setup step %r" % step)
    return done


def do_setup(spec, work=None):
    fixture = os.path.join(HERE, spec["fixture"])
    if not os.path.isdir(fixture):
        sys.exit("fatal: no fixture %s" % spec["fixture"])
    work = work or tempfile.mkdtemp(prefix="eval-%s-" % spec["name"])
    dest = os.path.join(work, os.path.basename(fixture))
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(fixture, dest)
    for extra in spec.get("also_copy", []):
        src = os.path.join(HERE, extra)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(work, os.path.basename(src)))
    done = apply_setup(dest, spec.get("setup", []))
    state = {"eval": spec["name"], "fixture_dir": dest, "setup": done,
             "pristine": snapshot(dest)}
    with open(os.path.join(work, ".eval-state.json"), "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)
    return work, dest, state


def frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return {}
    return {k.strip(): v.strip() for k, v in
            re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", m.group(1), re.M)}


def find_artifacts(dest, state, spec):
    """New or changed files after the run - the agent's actual output, whatever it named it."""
    now = snapshot(dest)
    pristine = state["pristine"]
    changed = [rel for rel, h in sorted(now.items())
               if rel not in pristine or pristine[rel] != h]
    wanted = (spec.get("artifact") or {}).get("type")
    if not wanted:
        return changed, changed
    matched = []
    for rel in changed:
        if not rel.endswith(".md"):
            continue
        if frontmatter(read(os.path.join(dest, rel))).get("type") == wanted:
            matched.append(rel)
    return changed, matched


def grade(spec, work):
    state_path = os.path.join(work, ".eval-state.json")
    if not os.path.isfile(state_path):
        sys.exit("fatal: %s has no .eval-state.json - run --setup first" % work)
    with open(state_path, encoding="utf-8") as fh:
        state = json.load(fh)
    dest = state["fixture_dir"]
    changed, artifacts = find_artifacts(dest, state, spec)

    print("eval %s - work %s" % (spec["name"], work))
    print("  changed files: %s" % (", ".join(changed) if changed else "(none)"))
    wanted = (spec.get("artifact") or {}).get("type")
    if wanted:
        print("  artifacts with `type: %s`: %s"
              % (wanted, ", ".join(artifacts) if artifacts else "(none)"))
    print("")

    text = "\n\n".join(read(os.path.join(dest, rel)) for rel in (artifacts or changed)
                       if rel.endswith(".md"))
    results = []
    for chk in spec["mechanical"]:
        ok, detail = run_check(chk, text, dest, state, changed, artifacts)
        results.append({"id": chk["id"], "cite": chk.get("cite", ""), "ok": ok,
                        "detail": detail, "why": chk.get("why", "")})
        print("  [%s] %-28s %s%s"
              % ("x" if ok else " ", chk["id"], detail,
                 "" if not chk.get("cite") else "  (%s)" % chk["cite"]))

    judged = [ln.strip() for ln in read(spec["path"]).splitlines()
              if ln.strip().startswith("- [ ]")]
    print("\n  %d mechanical box(es): %d passed, %d failed"
          % (len(results), sum(1 for r in results if r["ok"]),
             sum(1 for r in results if not r["ok"])))
    print("  %d rubric box(es) in %s still need a reader - grade them by hand"
          % (len(judged), os.path.relpath(spec["path"], ROOT).replace("\\", "/")))
    return results, changed, artifacts


def run_check(chk, text, dest, state, changed, artifacts):
    kind = chk["kind"]
    if kind == "frontmatter":
        values = [frontmatter(read(os.path.join(dest, rel))).get(chk["key"])
                  for rel in artifacts or changed if rel.endswith(".md")]
        ok = chk["equals"] in [v for v in values if v]
        return ok, "%s: %s == %r" % ("found" if ok else "missing", chk["key"], chk["equals"])
    if kind == "regex":
        n = len(re.findall(chk["pattern"], text, re.M | (re.I if chk.get("i") else 0)))
        lo, hi = chk.get("min", 1), chk.get("max")
        ok = n >= lo and (hi is None or n <= hi)
        return ok, "%d match(es) of /%s/ (min %s%s)" % (
            n, chk["pattern"], lo, "" if hi is None else ", max %d" % hi)
    if kind == "regex-changed":
        # Like "regex", but against EVERY changed .md file, not just the type-matched artifact -
        # for a fact that must show up in a file of a DIFFERENT type (a dossier, the hub, the
        # thread ledger) than the one `artifact.type` narrows `text` to.
        wide = "\n\n".join(read(os.path.join(dest, rel)) for rel in changed if rel.endswith(".md"))
        n = len(re.findall(chk["pattern"], wide, re.M | (re.I if chk.get("i") else 0)))
        lo, hi = chk.get("min", 1), chk.get("max")
        ok = n >= lo and (hi is None or n <= hi)
        return ok, "%d match(es) of /%s/ across all changed files (min %s%s)" % (
            n, chk["pattern"], lo, "" if hi is None else ", max %d" % hi)
    if kind == "file-exists":
        hits = glob.glob(os.path.join(dest, chk["glob"]), recursive=True)
        ok = bool(hits) if chk.get("expect", True) else not hits
        return ok, "%d file(s) matching %s" % (len(hits), chk["glob"])
    if kind == "no-new-files":
        # For a scenario whose correct behaviour is producing nothing at all.
        new = [rel for rel in changed if rel not in state["pristine"]
               and not any(re.match(pat, rel) for pat in chk.get("allow", []))]
        return not new, ("nothing created" if not new else "created: %s" % ", ".join(new))
    if kind == "untouched":
        # For evals whose correct behaviour is to CHANGE NOTHING but its own report.
        allowed = set(chk.get("allow_new", []))
        offenders = [rel for rel in changed
                     if rel in state["pristine"] and not any(
                         re.match(pat, rel) for pat in allowed)]
        return not offenders, ("nothing pre-existing modified" if not offenders
                               else "modified: %s" % ", ".join(offenders))
    return False, "unknown check kind %r" % kind


def record(spec, results, changed, artifacts, work, model):
    if not os.path.isdir(RESULTS):
        os.makedirs(RESULTS)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = re.sub(r"[^a-z0-9.-]+", "-", (model or "unknown").lower())
    path = os.path.join(RESULTS, "%s-%s-%s.json" % (stamp, spec["name"], slug))
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"eval": spec["name"], "model": model or "unknown", "when": stamp,
                   "work": work, "changed": changed, "artifacts": artifacts,
                   "mechanical": results,
                   "passed": all(r["ok"] for r in results)}, fh, indent=2)
    print("\n  recorded %s" % os.path.relpath(path, ROOT).replace("\\", "/"))
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(prog="run_eval.py", description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true", help="list evals and their mechanical cover")
    ap.add_argument("--setup", metavar="EVAL", help="prepare a work copy and print the prompt")
    ap.add_argument("--grade", metavar="EVAL", help="grade the mechanical boxes in --work")
    ap.add_argument("--work", help="the work directory (default: a fresh temp dir)")
    ap.add_argument("--scenario", help="which scenario of a multi-scenario eval (A, B, ...)")
    ap.add_argument("--agent", metavar="CMD",
                    help="run this command after setup; {prompt} and {work} are substituted")
    ap.add_argument("--model", help="what produced the output, recorded with --record")
    ap.add_argument("--record", action="store_true", help="write a result file under tests/results")
    args = ap.parse_args(argv)
    utf8_stdout()

    if args.list:
        for name in eval_names():
            text = read(os.path.join(EVALS, name + ".md"))
            m = SPEC.search(text)
            raw = json.loads(m.group(1)) if m else {}
            keys = sorted(raw.get("scenarios", {})) or [None]
            for key in keys:
                spec, _t = load_eval(name, key)
                mech = len(spec["mechanical"])
                print("%-20s %s  fixture=%s"
                      % (spec["name"], ("%d mechanical box(es)" % mech) if mech
                         else "judged only", spec["fixture"]))
        return 0

    name = args.setup or args.grade
    if not name:
        ap.error("give --setup EVAL, --grade EVAL, or --list")
    spec, _text = load_eval(name, args.scenario)

    if args.setup:
        work, dest, state = do_setup(spec, args.work)
        print("work copy: %s" % dest)
        for step in state["setup"]:
            print("  setup: %s" % step)
        for i, prompt in enumerate(spec["prompts"], 1):
            label = "prompt" if len(spec["prompts"]) == 1 else "prompt %d" % i
            print("\n--- %s (verbatim) ---\n%s\n" % (label, prompt))
        if not args.agent:
            print("run a fresh agent session in the work copy, then:\n"
                  "  python3 tests/run_eval.py --grade %s%s --work %s"
                  % (name, " --scenario %s" % spec["scenario"] if spec.get("scenario") else "",
                     work))
            return 0
        cmd = args.agent.replace("{prompt}", shlex.quote(spec["prompts"][0])) \
                        .replace("{work}", shlex.quote(dest))
        print("running agent: %s" % cmd)
        proc = subprocess.run(cmd, shell=True, cwd=dest)
        print("agent exited %d" % proc.returncode)
        results, changed, artifacts = grade(spec, work)
        if args.record:
            record(spec, results, changed, artifacts, work, args.model)
        return 0 if all(r["ok"] for r in results) else 1

    if not args.work:
        ap.error("--grade needs --work (the directory --setup created)")
    results, changed, artifacts = grade(spec, args.work)
    if args.record:
        record(spec, results, changed, artifacts, args.work, args.model)
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
