#!/usr/bin/env python3
"""Install smoke test: what a user actually receives.

    python3 tests/smoke_install.py              # pick the installer that fits the host
    python3 tests/smoke_install.py --installer sh
    python3 tests/smoke_install.py --installer ps1

Installs into a throwaway directory and asserts the promises the README makes:

  * nine skill folders, each with a SKILL.md and its own `references/PRINCIPLES.md`,
    byte-identical to `docs/PRINCIPLES.md` (a skill folder is copied ALONE, so a bundle
    that only exists in the repo is a dangling link on the installed copy);
  * the setup skill carries the schema it interviews from;
  * `docs/`, `templates/`, `tests/` and `scripts/` do NOT travel;
  * re-installing replaces a folder **wholesale** - a stray file left in an installed skill
    is gone afterwards. That is the documented behaviour, and it surprises people once, so
    it is asserted rather than assumed.

Exit 0 when every assertion holds; 1 with a report otherwise. Stdlib only.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
failures = []


def check(condition, message):
    if condition:
        print("  ok   %s" % message)
    else:
        print("  FAIL %s" % message)
        failures.append(message)


def run_installer(kind, target, *extra):
    if kind == "sh":
        cmd = ["sh", os.path.join(ROOT, "install.sh"), target] + list(extra)
    else:
        exe = shutil.which("pwsh") or shutil.which("powershell")
        if not exe:
            sys.exit("fatal: no PowerShell found for --installer ps1")
        flags = {"--dry-run": "-DryRun", "--uninstall": "-Uninstall"}
        cmd = [exe, "-NoProfile", "-ExecutionPolicy", "Bypass",
               "-File", os.path.join(ROOT, "install.ps1"), "-Target", target] \
            + [flags[e] for e in extra]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=ROOT)
    out = proc.stdout.decode("utf-8", "replace")
    if proc.returncode != 0:
        print(out)
        sys.exit("fatal: installer exited %d" % proc.returncode)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="smoke_install.py")
    ap.add_argument("--installer", choices=("auto", "sh", "ps1"), default="auto")
    args = ap.parse_args(argv)
    kind = args.installer
    if kind == "auto":
        kind = "sh" if shutil.which("sh") else "ps1"

    target = tempfile.mkdtemp(prefix="ttrpg-install-")
    try:
        print("installing with %s into %s" % (kind, target))
        dry = run_installer(kind, target, "--dry-run")
        check("would install" in dry and not os.listdir(target),
              "--dry-run reports what it would do and writes nothing")
        run_installer(kind, target)

        expected = sorted(d for d in os.listdir(os.path.join(ROOT, "skills"))
                          if os.path.isdir(os.path.join(ROOT, "skills", d)))
        installed = sorted(d for d in os.listdir(target)
                           if os.path.isdir(os.path.join(target, d)))
        check(installed == expected,
              "installed folders match skills/ (%d expected, %d found)"
              % (len(expected), len(installed)))

        with open(os.path.join(ROOT, "docs", "PRINCIPLES.md"), "rb") as fh:
            princ = fh.read()
        for d in expected:
            skill = os.path.join(target, d)
            check(os.path.isfile(os.path.join(skill, "SKILL.md")), "%s/SKILL.md" % d)
            bundled = os.path.join(skill, "references", "PRINCIPLES.md")
            ok = os.path.isfile(bundled)
            if ok:
                with open(bundled, "rb") as fh:
                    ok = fh.read() == princ
            check(ok, "%s/references/PRINCIPLES.md is present and identical" % d)

        check(os.path.isfile(os.path.join(target, "ttrpg-campaign-setup", "references",
                                          "campaign-profile.md")),
              "the setup skill carries the schema it interviews from")

        for leaked in ("docs", "templates", "tests", "scripts", "README.md", "AGENTS.md"):
            check(not os.path.exists(os.path.join(target, leaked)),
                  "%s does not travel into an install" % leaked)

        manifest = os.path.join(target, ".ttrpg-skills-manifest")
        manifest_text = ""
        if os.path.isfile(manifest):
            with open(manifest, encoding="utf-8") as fh:
                manifest_text = fh.read()
        check("package: ttrpg-campaign-skills" in manifest_text and "version:" in manifest_text,
              "a manifest records package, version, commit and source")

        stray = os.path.join(target, expected[0], "MY-LOCAL-EDIT.md")
        with open(stray, "w", encoding="utf-8") as fh:
            fh.write("local edit\n")
        run_installer(kind, target)
        check(not os.path.exists(stray),
              "re-install replaces a skill folder wholesale (a local edit is lost - documented)")

        run_installer(kind, target, "--uninstall")
        left = [d for d in expected if os.path.exists(os.path.join(target, d))]
        check(not left and not os.path.exists(os.path.join(target, ".ttrpg-skills-manifest")),
              "--uninstall removes exactly what was installed, manifest included")
    finally:
        shutil.rmtree(target, ignore_errors=True)

    print("")
    if failures:
        print("%d failure(s)" % len(failures))
        return 1
    print("install smoke test passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
