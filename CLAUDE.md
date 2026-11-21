# CLAUDE.md · rules for any Claude session working on this site

This is the portfolio of **Md. Zaid Hossain** (md-zaid-hossain.github.io). Static HTML, CSS and a little JavaScript,
built by `build/build.py` from `content/*.yml` and `media/`, published by GitHub Actions to GitHub Pages.
The pages are the approved design (Claude Design canvas v221), reproduced exactly; keep it that way.

## How Zaid works with you
- Chat is Bangla-led with English technical terms. Code comments in simple English.
- Do not ask him for facts that are in his files or in `content/`. Ask only for decisions: 2 or 3 options and your recommendation.
- Big changes: show a preview first (a screenshot or a branch), apply after his ok.
- Fix exactly what he points at. No extra layout changes he did not ask for.
- Tell him in 1 or 2 lines what changed; list only real open questions.

## How the site is built
- `python3 build/build.py` writes `dist/` (add `--serve` for http://localhost:8000). GitHub Actions runs the same on every push to main.
- `build/site_src/` = the approved mockup's page builders (Python, one per page; `site_parts.py`, `slideshow.py`,
  `videoplayer.py`, `routine.py`, `type_scale.py` are shared pieces). Their data lists are replaced at the end of each
  data module by `build/content_io.py`, which reads `content/*.yml`. So: **content changes go in `content/`; design changes go in `build/site_src/`.**
- Each page is rendered in all 6 themes and merged: theme-only CSS is scoped to `:root[data-theme="…"]`; theme-only
  attribute values (backdrop photos, hero gear, footer factory colours) are swapped by `build/assets/site.js` (`window.ZH_SWAP`).
  Without JavaScript the page shows the dark red theme.
- Speed: GitHub Pages is very slow from Bangladesh (about 20 KB/s), so on GitHub Actions every picture, clip, font,
  CSS file and site.js the pages load is served by jsDelivr. jsDelivr serves a commit only under 50 MB, so
  `build/cdn_publish.py` puts those files on small branches (cdn-0 ... cdn-5 about 20 MB each by a hash of the path,
  cdn-a for fonts, CSS and site.js) and fills their commits into the pages (`@__CDN<k>__` in the build). Never commit to
  the cdn-* branches by hand. `build/web_copies.py` makes the 800 px copies, AVIF copies and the first frame of each 3D
  sprite; they are not kept on main (gitignored). Pictures load lazily, grids use the 800 px copy, AVIF where the browser
  takes it, CSS sits in content-named files. Check after any change to this: layout must match pixel for pixel with
  pictures blocked (see mockup-source tools), and `checks/widths.py` answers CDN requests from dist/.
- `media/blob_to_media.json` maps the canvas picture ids still written in the builders (`/_blob/<id>`) to `media/` paths. Keep it.
- Text that lives in builder code, not in content/: the Home page summaries (hero, research list in `res_list.py`,
  experience list `exp_list.py`, education chart `edu_gantt.py`, skills `skill_cards.py`), the Projects page brief, the EV page (`build_ev.py`).
  When a content change makes one of these stale (a new paper, a new job), update it too.

## Where things are
- Text and lists: `content/*.yml` (one file per page; one file per project in `content/projects/`).
- Pictures, clips, 3D models, CV: `media/<page>/...`. Content files point at them as `media/...` paths.
- Pages CMS editor config: `.pages.yml`, made by `python3 tools/make_pages_yml.py .`. Re-run it after you add or rename a key in `content/`.
- CV: `cv-source/cv.html` → `node cv-source/pdf.js` writes `media/cv/Md_Zaid_Hossain_CV.pdf` (A4, one page).
- Never edit `dist/` (it is rebuilt every time).

## Before every commit
1. `python3 checks/content_check.py` prints `0 problems`.
2. `python3 build/build.py` builds without errors and lists no links still `#`.
3. `python3 checks/dashinv.py dist` prints 0; `python3 checks/widths.py dist` prints 0 problems.
4. Look at the changed pages in all 6 themes at 1440, 768, 390 and 360 px.

## Text rules (visible text)
- No em dash or en dash. No "/" or "+" as shorthand in sentences: write "and", "or", "with". Use a period, comma, colon or "·" in labels. ("CAD/CAM" and "AS/RS" stay as written.)
- A person's name never breaks across lines (wrap each name in a `nowrap` span). Short phone rows stay on one line.
- Course names are white (`--strong`) in dark themes.
- Numbers come from his papers and files. Never round or invent. Present-day facts (people, journal metrics) must be looked up.

## Look and behaviour
- Calm engineering look: drawing sheets, part numbers, gears. No loud highlights.
- Fonts: Inter (body), Space Grotesk (headings), IBM Plex Mono (labels). Self-hosted woff2.
- Buttons are the bracket button `.bkb`: no underline at rest; on hover a theme-colour line draws in from the left.
- Photo rows are always full (no empty slot in the last row). Every photo group opens as a slideshow (arrows, swipe, Esc).
- Every video is a clickable panel that opens the full-screen player.
- 3D colours realistic and easy on the eye.

## Privacy (hard rules, never break them)
- NEVER publish the NID, family or personal documents, the phone number, or the home address. Map: Dhaka at city level only.
- Transcripts and marksheets: "on request", never shown.
- Public certificates: roll, registration and serial numbers, parents' names and date of birth covered with a frosted-glass blur before upload.
- Blur the faces of study participants. Do not show other people's faces without permission (third-party event photos carry a credit line).
- Client names stay hidden on the freelance list (`checks/content_check.py` knows the names, as hashes). Files named with his roll number are not shown.
- No unlicensed or third-party images. Journal figures only under CC BY 4.0 with credit.
- Never handle his passwords, tokens or logins. He signs in himself.
- Sensitive files on his computer that must never be opened or uploaded: `github-recovery-codes.txt`, `kaggle.json`, NID PDFs.
