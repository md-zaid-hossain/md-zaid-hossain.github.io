#!/usr/bin/env python3
"""Project detail pages (template approved by Zaid on 2026-11-20): dark, light and phone board for each page in
project_pages.PAGES. Board names: Proj<Key>, Proj<Key>Light, Proj<Key>Mobile."""
import os
import project_pages as PP
import type_scale as TS


def name(p):
    return "Proj" + p["key"].replace("-", " ").title().replace(" ", "")


if __name__ == "__main__":
    out = os.environ.get("PORTFOLIO_OUT", "/home/claude/zaid/project")
    for p in PP.PAGES:
        n = name(p)
        for theme, suf in [("dark", ""), ("light", "Light"), ("dark", "Mobile")]:
            open(f"{out}/{n}{suf}.dc.html", "w").write(TS.apply(PP.page(p, theme, f"{p['title']} · {theme}{' phone' if suf == 'Mobile' else ''}")))
    print(len(PP.PAGES), "project pages written")
