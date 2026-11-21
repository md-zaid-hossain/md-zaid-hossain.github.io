"""Write .pages.yml (the Pages CMS editor config) from the content files themselves, so every key in the
YAML has a field in the form (nothing gets lost on save). Run after changing the shape of content/*.yml:
  python3 tools/make_pages_yml.py <site folder>"""
import glob, os, re, sys, yaml

SITE = os.path.abspath(sys.argv[1])
# keys the editor shows but should not touch (ids and layout switches used by the build)
HIDE = {"key", "gid", "id", "number", "kind", "f", "m", "q", "look", "ratio", "wide", "featured", "chapter", "no", "slug",
        "count", "own_layout", "chain_title", "other_images", "tag_box", "glb"}
LABEL = {"cap": "Caption", "do": "What I do", "doi": "DOI", "cv": "CV (PDF)", "pdf": "Paper PDF", "url": "Link",
         "focus": "Crop focus (e.g. 50% 45%)", "credit": "Photo credit (third-party photos)", "crumb": "Breadcrumb (CAPITALS)",
         "tag": "Label (CAPITALS)", "turntable": "Turntable sprite (9 x 8 frames)", "model": "3D model (GLB)",
         "image": "Picture", "lead": "Intro", "date": "Date (e.g. FEB 2023)", "end": "End (empty = now)"}
IMG = re.compile(r"^media/.+\.(webp|jpg|jpeg|png|gif|svg)$", re.I)
FILE = re.compile(r"^media/.+\.(mp4|webm|glb|pdf)$", re.I)


def merge(a, b):
    """Union of two values' shapes, so a key used in any entry gets a field."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(a)
        for k, v in b.items():
            out[k] = merge(out[k], v) if k in out else v
        return out
    if isinstance(a, list) and isinstance(b, list):
        return [merge_all(a + b)] if (a + b) else []
    return a if a not in (None, "") else b


def merge_all(items):
    out = None
    for it in items:
        out = it if out is None else merge(out, it)
    return out


def field(name, v):
    f = {"name": name, "label": LABEL.get(name, name.replace("_", " ").capitalize())}
    if name in HIDE:
        f["hidden"] = True
    if isinstance(v, list):
        inner = merge_all(v) if v else ""
        sub = field(name, inner)
        sub["list"] = True
        sub["label"] = f["label"]
        if "hidden" in f:
            sub["hidden"] = True
        return sub
    if isinstance(v, dict):
        f["type"] = "object"
        f["fields"] = [field(k, x) for k, x in v.items()]
    elif isinstance(v, bool):
        f["type"] = "boolean"
    elif isinstance(v, (int, float)):
        f["type"] = "number"
    elif isinstance(v, str) and IMG.match(v):
        f["type"] = "image"
    elif isinstance(v, str) and FILE.match(v):
        f["type"] = "file"
    elif isinstance(v, str) and (len(v) > 90 or "\n" in v):
        f["type"] = "text"
    else:
        f["type"] = "string"
    return f


def load(p):
    return yaml.safe_load(open(os.path.join(SITE, p)))


projects = merge_all([load(os.path.relpath(p, SITE)) for p in sorted(glob.glob(os.path.join(SITE, "content/projects/*.yml")))])
cfg = {
    "media": {"input": "media", "output": "media"},
    "content": [
        {"name": "projects", "label": "Projects", "type": "collection", "path": "content/projects", "format": "yaml",
         "filename": "{fields.slug}.yml", "view": {"fields": ["title", "no"], "sort": ["no"]},
         "fields": [field(k, v) for k, v in projects.items()]},
    ],
}
for name, label, path in [("gallery", "Gallery", "content/gallery.yml"), ("awards", "Awards and certificates", "content/awards.yml"),
                          ("research", "Research", "content/research.yml"), ("experience", "Experience", "content/experience.yml"),
                          ("site", "Site settings", "content/site.yml")]:
    data = load(path)
    cfg["content"].append({"name": name, "label": label, "type": "file", "path": path, "format": "yaml",
                           "fields": [field(k, v) for k, v in data.items()]})
# slugs are visible for new projects (they become the web address)
for f in cfg["content"][0]["fields"]:
    if f["name"] in ("slug", "no"):
        f.pop("hidden", None)
        f["label"] = {"slug": "Web address (projects/<this>/), small letters and dashes", "no": "Part number"}[f["name"]]
        f["required"] = True

head = ("# Pages CMS (https://pagescms.org): the browser editor for this site.\n"
        "# Open app.pagescms.org, sign in with GitHub, pick this repository: these forms appear.\n"
        "# Saving commits the change; GitHub Actions then rebuilds and publishes the site in about 2 minutes.\n"
        "# Made by tools/make_pages_yml.py from content/*.yml (every key has a field, hidden ones are ids the build needs).\n"
        "# Education and routines are not in the editor: their shape is too nested for forms. Change them through Claude or by hand.\n")
open(os.path.join(SITE, ".pages.yml"), "w").write(head + yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True, width=140))
print("fields:", sum(open(os.path.join(SITE, ".pages.yml")).read().count("- name:") for _ in [0]))
