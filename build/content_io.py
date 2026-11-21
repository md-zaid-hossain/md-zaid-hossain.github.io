"""Content files <-> the Python data the page builders use.

  to_*(...)   Python data -> plain YAML-ready dicts (used once, by tools/export_content.py, to write content/*.yml)
  load(name)  content/<name>.yml -> the exact Python structures the builders expect (tuples where they use tuples)

Both directions live here so they stay in step: tools/check_roundtrip.py proves load(to(x)) == x.
Media: in content files a picture is "media/<folder>/<file>"; load() turns it into the site path "/media/<folder>/<file>".
"""
import functools
import glob
import os
import re

import yaml

CONTENT = os.environ.get("SITE_CONTENT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content"))
MEDIA_RE = re.compile(r"(?<![\w/.])media/[\w./-]+\.(?:webp|jpe?g|png|gif|svg|mp4|webm|glb|pdf)", re.I)


# ---------------------------------------------------------------- helpers
def site_paths(x):
    """media/... -> /media/... everywhere inside x."""
    if isinstance(x, dict):
        return {k: site_paths(v) for k, v in x.items()}
    if isinstance(x, list):
        return [site_paths(v) for v in x]
    if isinstance(x, tuple):
        return tuple(site_paths(v) for v in x)
    if isinstance(x, str):
        return MEDIA_RE.sub(lambda m: "/" + m.group(0), x)
    return x


def plain(x):
    """tuples -> lists, so YAML stays plain."""
    if isinstance(x, dict):
        return {k: plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [plain(v) for v in x]
    return x


def read(name):
    with open(os.path.join(CONTENT, name), encoding="utf-8") as fh:
        return site_paths(yaml.safe_load(fh))


def T(x):
    return tuple(x) if isinstance(x, list) else x


def stem(path):
    return os.path.splitext(os.path.basename(path))[0]


def opt(d, *keys):
    """copy only the keys that are present (and not None) in d"""
    return {k: d[k] for k in keys if k in d and d[k] is not None}


# ---------------------------------------------------------------- projects
HERO_KEYS = ("turntable", "glb", "render", "render_label", "render_alt", "still_cap")


def to_project(p, card, card_image):
    d = dict(no=p["no"], slug=p["slug"], key=p["key"], title=p["title"], crumb=p["crumb"], tags=list(p["tags"]), lead=p["lead"])
    if card:
        d["card"] = dict(category=card[1], filter=card[2], title=card[3], text=card[4], tools=list(card[5]))
        if card_image:
            d["card"]["image"] = card_image
    hero = opt(p, *HERO_KEYS)
    if p.get("still"):
        hero["still"] = dict(label=p["still"][0], image=p["still"][1], alt=p["still"][2])
    d["hero"] = hero
    d["spec"] = [dict(label=a, value=b) for a, b in p["spec"]]
    d["stats"] = [dict(value=a, label=b) for a, b in p["stats"]]
    secs = []
    for s in p["sections"]:
        t = {k: v for k, v in s.items() if k not in ("photos", "rows", "steps")}
        if "photos" in s:
            t["photos"] = [dict(image=a, caption=b) for a, b in s["photos"]]
        if "rows" in s:
            t["rows"] = [dict(label=a, value=b) for a, b in s["rows"]]
        if "steps" in s:
            t["steps"] = list(s["steps"])
        secs.append(t)
    d["sections"] = secs
    return d


@functools.cache
def load_projects():
    """-> (pages, cards, card_images). pages sorted by part number, prev and next filled in (the EV page takes part 3)."""
    files = [read(os.path.relpath(f, CONTENT)) for f in sorted(glob.glob(os.path.join(CONTENT, "projects", "*.yml")))]
    pages, cards, imgs, chain = [], [], {}, []
    for d in sorted(files, key=lambda d: d["no"]):
        chain.append((d["no"], (d.get("card") or {}).get("title") or d.get("chain_title") or d["title"]))
        if d.get("own_layout"):
            continue
        p = dict(key=d.get("key") or d["slug"], no=d["no"], slug=d["slug"], title=d["title"], crumb=d.get("crumb") or d["title"].upper(),
                 tags=list(d.get("tags") or []), lead=d.get("lead") or "")
        h = d.get("hero", {})
        p.update(opt(h, *HERO_KEYS))
        if h.get("still"):
            s = h["still"]
            p["still"] = (s["label"], s["image"], s["alt"])
        p["spec"] = [(r["label"], r["value"]) for r in d.get("spec", [])]
        p["stats"] = [(r["value"], r["label"]) for r in d.get("stats", [])]
        secs = []
        for s in d.get("sections", []):
            t = {k: v for k, v in s.items() if k not in ("photos", "rows", "steps")}
            if "photos" in s:
                t["photos"] = [(r["image"], r.get("caption", "")) for r in s["photos"]]
            if "rows" in s:
                t["rows"] = [(r["label"], r["value"]) for r in s["rows"]]
            if "steps" in s:
                t["steps"] = list(s["steps"])
            secs.append(t)
        p["sections"] = secs
        pages.append(p)
        c = d.get("card")
        if c:
            cards.append((p["key"], c["category"], c["filter"], c["title"], c["text"], list(c.get("tools", []))))
            if c.get("image"):
                imgs[p["key"]] = c["image"]
    # previous and next by part number, wrapping round
    for p in pages:
        i = [n for n, _ in chain].index(p["no"])
        p["prev"] = chain[i - 1]
        p["next"] = chain[(i + 1) % len(chain)]
    return pages, cards, imgs


# ---------------------------------------------------------------- gallery
def to_gallery(chapters, gal_img):
    used = set()
    out = []
    for key, label, sub, items in chapters:
        albums = []
        for a in items:
            t = {k: v for k, v in a.items() if k != "photos"}
            ph = []
            for pid, cap, focus in a["photos"]:
                if pid.startswith("/_blob/"):      # a picture from another page, used as it is
                    r = dict(image=pid, caption=cap, focus=focus)
                else:
                    img = gal_img.get(pid, "")
                    used.add(pid)
                    r = dict(image=img, caption=cap, focus=focus)
                    if not img.startswith("/_blob/") or stem(img) != pid:
                        r["id"] = pid
                ph.append(r)
            t["photos"] = ph
            albums.append(t)
        out.append(dict(chapter=key, label=label, subtitle=sub, albums=albums))
    extra = {k: v for k, v in gal_img.items() if k not in used}
    return dict(chapters=out, other_images=extra)


@functools.cache
def load_gallery():
    d = read("gallery.yml")
    chapters, img = [], dict(d.get("other_images") or {})
    for ch in d["chapters"]:
        albums = []
        for a in ch["albums"]:
            t = {k: v for k, v in a.items() if k != "photos"}
            ph = []
            for r in a.get("photos", []):
                if r.get("id"):
                    pid = r["id"]
                    if r.get("image"):
                        img[pid] = r["image"]
                elif r["image"].startswith("/media/gallery/"):
                    pid = stem(r["image"])
                    img[pid] = r["image"]
                else:                                # a picture kept in another folder: used by its path
                    pid = r["image"]
                ph.append((pid, r.get("caption", ""), r.get("focus", "50% 50%")))
            t["photos"] = ph
            albums.append(t)
        chapters.append((ch["chapter"], ch["label"], ch["subtitle"], albums))
    return chapters, img


# ---------------------------------------------------------------- awards
def to_awards(A):
    used = set()
    groups = []
    for g in A.GROUPS:
        certs = []
        for c in g[5]:
            r = dict(key=c[0], code=c[1], name=c[2], issuer=c[3], date=c[4], links=[dict(label=a, url=b) for a, b in c[5]])
            if len(c) > 6:
                r["note"] = c[6]
            if c[0] in A.IMG:
                r["image"] = A.IMG[c[0]]
                used.add(c[0])
            certs.append(r)
        groups.append(dict(id=g[0], number=g[1], title=g[2], short=g[3], count=g[4], certificates=certs))
    s = dict(A.SCHOLARSHIP)
    s["tag_box"] = list(s["tag_box"])
    s["team_members"] = [dict(name=a, url=b) for a, b in s["team_members"]]
    return dict(
        competitions=[dict(rank=r, event=e, organiser=o, date=d, key=k, **({"certificate": A.CERT_IMG[k]} if k in A.CERT_IMG else {}))
                      for r, e, o, d, k in A.COMPETITIONS],
        scholarship=s, certificate_groups=groups,
        other_images={k: v for k, v in A.IMG.items() if k not in used})


@functools.cache
def load_awards():
    d = read("awards.yml")
    comps = [(c["rank"], c["event"], c["organiser"], c["date"], c["key"]) for c in d["competitions"]]
    cert_img = {c["key"]: c["certificate"] for c in d["competitions"] if c.get("certificate")}
    s = dict(d["scholarship"])
    s["tag_box"] = tuple(s["tag_box"])
    s["team_members"] = [(m["name"], m["url"]) for m in s["team_members"]]
    img = dict(d.get("other_images") or {})
    groups = []
    for g in d["certificate_groups"]:
        certs = []
        for c in g["certificates"]:
            t = (c["key"], c["code"], c["name"], c["issuer"], c["date"], [(l["label"], l["url"]) for l in c.get("links", [])])
            if c.get("note"):
                t = t + (c["note"],)
            if c.get("image"):
                img[c["key"]] = c["image"]
            certs.append(t)
        groups.append((g["id"], g["number"], g["title"], g["short"], g["count"], certs))
    return dict(COMPETITIONS=comps, CERT_IMG=cert_img, SCHOLARSHIP=s, GROUPS=groups, IMG=img)


# ---------------------------------------------------------------- research
def _nums(x):
    return [dict(value=a, label=b) for a, b in x]


def to_research(R):
    papers = []
    for p in R.PAPERS:
        q = dict(p)
        if "nums" in q:
            q["nums"] = _nums(q["nums"])
        if q.get("metric"):
            q["metric"] = dict(value=q["metric"][0], label=q["metric"][1])
        papers.append(q)
    ongoing = []
    for p in R.ONGOING:
        q = dict(p)
        if "nums" in q:
            q["nums"] = _nums(q["nums"])
        ongoing.append(q)
    return dict(published=papers, in_progress=ongoing, figures=plain(R.B))


@functools.cache
def load_research():
    d = read("research.yml")

    def back(q):
        q = dict(q)
        if "nums" in q:
            q["nums"] = [(n["value"], n["label"]) for n in q["nums"]]
        if q.get("metric"):
            q["metric"] = (q["metric"]["value"], q["metric"]["label"])
        return q
    figs = {k: T(v) for k, v in (d.get("figures") or {}).items()}
    return dict(PAPERS=[back(p) for p in d["published"]], ONGOING=[back(p) for p in d.get("in_progress") or []], B=figs)


# ---------------------------------------------------------------- experience
def to_experience(X):
    roles = []
    for r in X.ROLES:
        q = dict(r)
        q["links"] = [dict(label=a, url=b) for a, b in q.get("links", [])]
        roles.append(q)
    return dict(roles=roles, client_jobs=[dict(year=a, job=b, delivered=c) for a, b, c in X.JOBS],
                campus=plain(X.CAMPUS), training=plain(X.TRAINING),
                photos={k: [dict(image=a, step=b, caption=c) for a, b, c in v] for k, v in X.PHOTOS.items()})


@functools.cache
def load_experience():
    d = read("experience.yml")
    roles = []
    for r in d["roles"]:
        q = dict(r)
        q["links"] = [(l["label"], l["url"]) for l in q.get("links") or []]
        roles.append(q)
    photos = {k: [(p["image"], p["step"], p["caption"]) for p in v] for k, v in d["photos"].items()}
    return dict(ROLES=roles, JOBS=[(j["year"], j["job"], j["delivered"]) for j in d["client_jobs"]],
                CAMPUS=d["campus"], TRAINING=d["training"], PHOTOS=photos,
                CNC_PHOTOS=photos.get("cnc", []), BOOTCAMP_PHOTOS=photos.get("bootcamp", []))


# ---------------------------------------------------------------- education
def _school(groups, subjects, extra):
    return dict(groups=[dict(name=a, subjects=list(b)) for a, b in groups], subjects=list(subjects), extra=list(extra))


def to_education(E):
    return dict(
        terms=[dict(key=a, label=b, period=c) for a, b, c in E.TERMS],
        areas=[dict(key=a, label=b) for a, b in E.AREAS],
        courses=[dict(term=a, code=b, title=c, area=d, kind=e, topics=list(f)) for a, b, c, d, e, f in E.COURSES],
        teachers={k: dict(name=v[0], profile=v[1], active=v[2]) for k, v in E.T.items()},
        taught_by=plain(E.TEACH),
        msc_courses=[dict(code=a, title=b, topics=list(c)) for a, b, c in E.MSC_COURSES],
        hsc=_school(E.HSC_GROUPS, E.HSC_SUBJECTS, E.HSC_EXTRA), ssc=_school(E.SSC_GROUPS, E.SSC_SUBJECTS, E.SSC_EXTRA))


@functools.cache
def load_education():
    d = read("education.yml")
    out = dict(
        TERMS=[(t["key"], t["label"], t["period"]) for t in d["terms"]],
        AREAS=[(a["key"], a["label"]) for a in d["areas"]],
        COURSES=[(c["term"], c["code"], c["title"], c["area"], c.get("kind") or "", list(c.get("topics") or [])) for c in d["courses"]],
        T={k: (v["name"], v["profile"], v.get("active", True)) for k, v in d["teachers"].items()},
        TEACH={k: list(v) for k, v in d["taught_by"].items()},
        MSC_COURSES=[(c["code"], c["title"], list(c.get("topics") or [])) for c in d["msc_courses"]],
        CAD_WINS=load_awards()["COMPETITIONS"])     # one list, kept in awards.yml
    for s in ("hsc", "ssc"):
        x = d[s]
        out[f"{s.upper()}_GROUPS"] = [(g["name"], list(g["subjects"])) for g in x["groups"]]
        out[f"{s.upper()}_SUBJECTS"] = list(x["subjects"])
        out[f"{s.upper()}_EXTRA"] = list(x["extra"])
    return out


# ---------------------------------------------------------------- routines
def to_routines(RT):
    return dict(slots=[dict(start=a, end=b) for a, b in RT.SLOTS], days=list(RT.DAYS), short_titles=dict(RT.SHORT),
                routines={t: {d: {int(s): dict(code=c, teachers=k) for s, (c, k) in v.items()} for d, v in days.items()}
                          for t, days in RT.ROUTINE.items()},
                teachers_only=sorted(RT.TEACHERS_ONLY))


@functools.cache
def load_routines():
    d = read("routines.yml")
    return dict(SLOTS=[(s["start"], s["end"]) for s in d["slots"]], DAYS=list(d["days"]), SHORT=dict(d["short_titles"]),
                ROUTINE={t: {day: {int(s): (c["code"], c["teachers"]) for s, c in v.items()} for day, v in days.items()}
                         for t, days in d["routines"].items()},
                TEACHERS_ONLY=set(d.get("teachers_only") or []))
