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


def run_installer(kind, target, *extra, **kwargs):
    allow_fail = kwargs.pop("allow_fail", False)
    if kind == "sh":
        cmd = ["sh", os.path.join(ROOT, "install.sh"), target] + list(extra)
    else:
        exe = shutil.which("pwsh") or shutil.which("powershell")
        if not exe:
            sys.exit("fatal: no PowerShell found for --installer ps1")
        flags = {"--dry-run": "-DryRun", "--uninstall": "-Uninstall", "--force": "-Force"}
        cmd = [exe, "-NoProfile", "-ExecutionPolicy", "Bypass",
               "-File", os.path.join(ROOT, "install.ps1"), "-Target", target] \
            + [flags[e] for e in extra]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=ROOT)
    out = proc.stdout.decode("utf-8", "replace")
    if proc.returncode != 0 and not allow_fail:
        print(out)
        sys.exit("fatal: installer exited %d" % proc.returncode)
    if allow_fail:
        return out, proc.returncode
    return out


def test_unmanaged_collision(kind):
    """An unmanaged folder (never installed by this package) must survive both a plain
    install and an --uninstall, and only --force may replace it."""
    target = tempfile.mkdtemp(prefix="ttrpg-install-unmanaged-")
    try:
        print("\nunmanaged-collision scenario with %s into %s" % (kind, target))
        victim = "ttrpg-campaign-setup"
        foreign_dir = os.path.join(target, victim)
        os.makedirs(foreign_dir)
        sentinel = os.path.join(foreign_dir, "NOT-OURS.md")
        with open(sentinel, "w", encoding="utf-8") as fh:
            fh.write("pre-existing, unmanaged content\n")

        out, code = run_installer(kind, target, allow_fail=True)
        check(code != 0, "install exits non-zero when an unmanaged collision is refused")
        check(os.path.isfile(sentinel), "unmanaged folder survives install without --force")
        with open(sentinel, encoding="utf-8") as fh:
            check(fh.read() == "pre-existing, unmanaged content\n",
                  "unmanaged folder's content is untouched")

        others = sorted(d for d in os.listdir(os.path.join(ROOT, "skills"))
                        if os.path.isdir(os.path.join(ROOT, "skills", d)) and d != victim)
        installed_others = [d for d in others if os.path.isdir(os.path.join(target, d))]
        check(installed_others == others,
              "the other skill folders install normally despite the one refusal")

        manifest = os.path.join(target, ".ttrpg-skills-manifest")
        manifest_text = ""
        if os.path.isfile(manifest):
            with open(manifest, encoding="utf-8") as fh:
                manifest_text = fh.read()
        check(("skill: %s" % victim) not in manifest_text,
              "the manifest does not claim ownership of the folder it refused to touch")

        out2, code2 = run_installer(kind, target, "--uninstall", allow_fail=True)
        check(code2 == 0, "--uninstall succeeds for the manifest-listed folders")
        check(os.path.isfile(sentinel),
              "unmanaged folder survives --uninstall too (it was never manifest-listed)")
        for d in others:
            check(not os.path.exists(os.path.join(target, d)),
                  "managed folder %s is removed by --uninstall" % d)

        out3, code3 = run_installer(kind, target, "--force", allow_fail=True)
        check(code3 == 0, "--force overrides the refusal and installs cleanly")
        check(os.path.isfile(os.path.join(target, victim, "SKILL.md")),
              "--force replaces the previously unmanaged folder with the real skill")
        check(not os.path.exists(sentinel),
              "--force replaces the unmanaged folder wholesale (old content gone)")
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_legacy_manifest_uninstall_refused(kind):
    """--uninstall must refuse a manifest with no `skill:` entries rather than guess."""
    target = tempfile.mkdtemp(prefix="ttrpg-install-legacy-")
    try:
        print("\nlegacy-manifest scenario with %s into %s" % (kind, target))
        run_installer(kind, target)
        manifest = os.path.join(target, ".ttrpg-skills-manifest")
        with open(manifest, encoding="utf-8") as fh:
            lines = [ln for ln in fh.read().splitlines() if not ln.startswith("skill: ")]
        with open(manifest, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

        out, code = run_installer(kind, target, "--uninstall", allow_fail=True)
        check(code != 0, "--uninstall refuses a legacy manifest with no skill: entries")
        expected = sorted(d for d in os.listdir(os.path.join(ROOT, "skills"))
                          if os.path.isdir(os.path.join(ROOT, "skills", d)))
        check(all(os.path.isdir(os.path.join(target, d)) for d in expected),
              "--uninstall touches nothing when it refuses")
    finally:
        shutil.rmtree(target, ignore_errors=True)


def test_manifest_traversal_rejected(kind):
    """A hand-edited manifest with a path-escaping `skill:` value (e.g. `skill: ../victim`)
    must be rejected by --uninstall before any deletion happens - not resolved and followed.
    The sibling `victim` directory must survive byte-for-byte, and the manifest itself must
    not be removed on a refused run."""
    base = tempfile.mkdtemp(prefix="ttrpg-install-traversal-")
    try:
        print("\nmanifest-traversal scenario with %s into %s" % (kind, base))
        target = os.path.join(base, "target")
        victim = os.path.join(base, "victim")
        os.makedirs(target)
        os.makedirs(victim)
        sentinel = os.path.join(victim, "SENTINEL.md")
        with open(sentinel, "w", encoding="utf-8") as fh:
            fh.write("do not delete me\n")

        manifest = os.path.join(target, ".ttrpg-skills-manifest")
        with open(manifest, "w", encoding="utf-8") as fh:
            fh.write(
                "package: ttrpg-campaign-skills\n"
                "version: 0\n"
                "commit: 0\n"
                "source: x\n"
                "installed: 1970-01-01T00:00:00Z\n"
                "skills: 1\n"
                "skill: ../victim\n"
            )

        out, code = run_installer(kind, target, "--uninstall", allow_fail=True)
        check(code != 0, "--uninstall refuses a manifest with a path-escaping skill: entry")
        check(os.path.isdir(victim), "sibling victim directory still exists after refused uninstall")
        check(os.path.isfile(sentinel), "victim sentinel file still exists")
        with open(sentinel, encoding="utf-8") as fh:
            check(fh.read() == "do not delete me\n", "victim content is byte-for-byte untouched")
        check(os.path.isfile(manifest), "the (invalid) manifest is not removed on a refused uninstall")

        # A second manifest, this time with one traversal entry alongside a legitimate-looking
        # one - the whole run must still fail closed and remove nothing at all.
        manifest2_target = os.path.join(base, "target2")
        os.makedirs(manifest2_target)
        real_skill = sorted(d for d in os.listdir(os.path.join(ROOT, "skills"))
                            if os.path.isdir(os.path.join(ROOT, "skills", d)))[0]
        os.makedirs(os.path.join(manifest2_target, real_skill))
        with open(os.path.join(manifest2_target, real_skill, "marker.md"), "w",
                  encoding="utf-8") as fh:
            fh.write("marker\n")
        manifest2 = os.path.join(manifest2_target, ".ttrpg-skills-manifest")
        with open(manifest2, "w", encoding="utf-8") as fh:
            fh.write(
                "package: ttrpg-campaign-skills\nversion: 0\ncommit: 0\nsource: x\n"
                "installed: 1970-01-01T00:00:00Z\nskills: 2\n"
                "skill: %s\nskill: ../victim\n" % real_skill
            )
        out2, code2 = run_installer(kind, manifest2_target, "--uninstall", allow_fail=True)
        check(code2 != 0, "--uninstall refuses the whole run when ANY entry is a path traversal")
        check(os.path.isfile(os.path.join(manifest2_target, real_skill, "marker.md")),
              "a legitimate-looking sibling entry is NOT removed when another entry is invalid"
              " (fail closed, not best-effort)")
        check(os.path.isdir(victim) and os.path.isfile(sentinel),
              "victim is still untouched after the mixed-entries attempt too")
    finally:
        shutil.rmtree(base, ignore_errors=True)


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
        check(all(("skill: %s" % d) in manifest_text for d in expected),
              "the manifest lists every installed skill folder by name (ownership record)")

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

    test_unmanaged_collision(kind)
    test_legacy_manifest_uninstall_refused(kind)
    test_manifest_traversal_rejected(kind)

    print("")
    if failures:
        print("%d failure(s)" % len(failures))
        return 1
    print("install smoke test passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
