"""Put the files the pages load (pictures, clips, fonts, CSS, site.js) on small branches (cdn-0 ... cdn-5 for pictures and clips, cdn-a for fonts, CSS and site.js) and point
the pages at them. jsDelivr serves a GitHub repository only while the files at a commit stay under 50 MB, and the
whole site is about 110 MB, so the files are spread over the branches by a fixed rule (build.cdn_bin), about 20 MB each.

A branch gets a new commit only when its files changed, so unchanged branches keep their commit and jsDelivr keeps
them cached. Run by GitHub Actions after build/build.py:  python3 build/cdn_publish.py
  --dry-run   build the commits but do not push (for a local test)
Also: python3 build/cdn_publish.py --restore   copies earlier AVIF and 800 px copies back into media/ from the
branches, so build/web_copies.py only makes the new ones."""
import json
import os
import re
import subprocess
import sys
import tempfile

BUILD = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BUILD)
DIST = os.path.join(REPO, "dist")
sys.path.insert(0, BUILD)
LIMIT = 45_000_000   # stay well under jsDelivr's 50 MB


def git(*args, env=None, inp=None):
    return subprocess.run(["git", *args], cwd=REPO, env=env, input=inp, capture_output=True, text=True, check=True).stdout.strip()


def remote_branches():
    out = subprocess.run(["git", "ls-remote", "--heads", "origin", "cdn-*"], cwd=REPO, capture_output=True, text=True).stdout
    return {line.split("refs/heads/")[1]: line.split()[0] for line in out.splitlines() if "refs/heads/" in line}


def restore():
    """Bring earlier web copies back from the cdn branches (they keep the paths media/_avif/..., media/_thumbs/...)."""
    heads = remote_branches()
    if not heads:
        return 0
    git("fetch", "--depth=1", "origin", *heads.keys())
    n = 0
    for b in heads:
        files = git("ls-tree", "-r", "--name-only", f"origin/{b}").splitlines()
        for f in files:
            if f.startswith(("media/_avif/", "media/_thumbs/")):
                dst = os.path.join(REPO, f)
                if not os.path.exists(dst):
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    data = subprocess.run(["git", "show", f"origin/{b}:{f}"], cwd=REPO, capture_output=True, check=True).stdout
                    open(dst, "wb").write(data)
                    n += 1
    print(n, "earlier copies restored")
    return n


def publish(dry=False):
    import build as B   # noqa: E402  (the same bin rule as the pages)
    used = json.load(open(os.path.join(DIST, "cdn-files.json")))
    bins = {}
    for path in used:
        bins.setdefault(B.cdn_bin(path), []).append(path)
    heads = remote_branches()
    if heads:
        git("fetch", "--depth=1", "origin", *heads.keys())
    shas = {}
    for k in [str(i) for i in range(B.CDN_BINS)] + ["a"]:
        files = sorted(bins.get(k, []))
        size = sum(os.path.getsize(os.path.join(DIST, p.lstrip("/"))) for p in files)
        if size > LIMIT:
            sys.exit(f"cdn-{k} would hold {size / 1e6:.0f} MB, over the limit: raise CDN_BINS in build.py")
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, "index"))
            git("read-tree", "--empty", env=env)
            lines = []
            for p in files:
                blob = git("hash-object", "-w", os.path.join(DIST, p.lstrip("/")))
                lines.append(f"100644 {blob}\t{p.lstrip('/')}")
            if lines:
                git("update-index", "--index-info", env=env, inp="\n".join(lines) + "\n")
            tree = git("write-tree", env=env)
        branch = f"cdn-{k}"
        old = heads.get(branch)
        if old and git("rev-parse", f"{old}^{{tree}}") == tree:
            shas[k] = old
            print(f"{branch}: unchanged ({len(files)} files, {size / 1e6:.1f} MB)")
            continue
        args = ["commit-tree", tree, "-m", f"CDN files for the site ({len(files)} files)"]
        if old:
            args += ["-p", old]
        sha = git(*args)
        shas[k] = sha
        print(f"{branch}: new commit {sha[:7]} ({len(files)} files, {size / 1e6:.1f} MB)")
        if not dry:
            git("push", "origin", f"{sha}:refs/heads/{branch}")
    # point the pages at the branch commits
    n = 0
    for a, _, fs in os.walk(DIST):
        for f in fs:
            if f.endswith((".html", ".js", ".css", ".json")) and f != "cdn-files.json":
                p = os.path.join(a, f)
                s = open(p, encoding="utf-8").read()
                t = re.sub(r"__CDN(\w+?)__", lambda m: shas[m.group(1)], s)
                if t != s:
                    open(p, "w", encoding="utf-8").write(t)
                    n += 1
    os.remove(os.path.join(DIST, "cdn-files.json"))
    print(n, "files now point at the cdn branches")


if __name__ == "__main__":
    if "--restore" in sys.argv:
        restore()
    else:
        publish("--dry-run" in sys.argv)
