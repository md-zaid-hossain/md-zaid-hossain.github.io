# UPDATING · ওয়েবসাইট আপডেট করার নিয়ম · How to update the website

ওয়েবসাইট = **লেখা** (`content/*.yml`) + **ছবি, ভিডিও, 3D, CV** (`media/`)। তিনটা পথের যেকোনোটা দিয়ে এই দুই জায়গায় পরিবর্তন করলেই GitHub Actions নিজে check করে, build করে, প্রায় ২ মিনিটে সাইটে তুলে দেয়।

The website = **text** (`content/*.yml`) + **pictures, clips, 3D models and the CV** (`media/`). Change these two places by any of the three ways below; GitHub Actions then checks, builds and publishes the site in about 2 minutes.

| | পথ · Way | কখন ভালো · Best for |
|---|---|---|
| ১ | Claude-কে বলা · Ask Claude | নতুন project page, certificate blur, Home-এর সারাংশ, EV page, design বদল · new project pages, certificate blur, Home summaries, the EV page, design changes |
| ২ | Pages CMS (browser) | ছোট লেখা বদল, gallery-তে ছবি, নতুন certificate, paper · quick text edits, photos, certificates, papers |
| ৩ | GitHub Desktop (হাতে) | একসাথে অনেক ফাইল, offline কাজ · many files at once, offline work |

---

## প্রতিবার শুরুতে · Every time, first

নিজের কম্পিউটারে কিছু বদলানোর আগে `git pull` দিন (GitHub Desktop-এ **Fetch origin** → **Pull**), যাতে Pages CMS বা Claude-এর বদল আপনার কাছে আসে। · Before changing anything on your computer, run `git pull` (GitHub Desktop: Fetch origin → Pull) so changes made in Pages CMS or by Claude reach you.

## সবার আগে · First, always (privacy)

- NID, পারিবারিক কাগজ, ফোন নম্বর, বাসার ঠিকানা কখনো না। · Never the NID, family papers, phone number or home address.
- Certificate তোলার আগে roll, registration, serial নম্বর, বাবা-মায়ের নাম, জন্মতারিখ ঢেকে দিন (frosted blur)। পথ ১-এ Claude এটা করে দেয়। · Cover roll, registration and serial numbers, parents' names and date of birth before uploading a certificate. Way 1: Claude does it for you.
- Transcript, marksheet দেখানো হবে না ("on request")। · Transcripts and marksheets are never shown.
- Client-এর নাম না; অন্য মানুষের মুখ অনুমতি ছাড়া না; অন্যের তোলা ছবিতে credit লাইন। · No client names; no other people's faces without permission; credit line on third-party photos.
- ফোনের ছবিতে জায়গার তথ্য (GPS location) থাকে: upload-এর আগে সরান (ফোনের share-এ "location" বন্ধ করুন, বা পথ ১)। check এটা ধরলে build থামে, কিন্তু ছবি repo-তে চলে যায়, তাই আগেই সরান। · Phone photos carry the place they were taken (GPS): remove it before upload (turn location off when sharing, or way 1). The check stops the build, but the photo would already be in the repo.
- লেখায় em dash (—) বা en dash (–) না, আর "/" বা "+" shorthand না ("and", "or", "with" লিখুন)। · No em or en dash, no "/" or "+" shorthand in text.

ভুল হলে `checks/content_check.py` build থামিয়ে দেয় আর কোন ফাইলে কী সমস্যা তা লিখে দেয়। · If something breaks a rule, `checks/content_check.py` stops the build and names the file and the problem.

---

## পথ ১ · Way 1: Claude-কে বলা · Ask Claude

**একবার সেটআপ · One-time setup:** Claude desktop app-এ repo-র folder (GitHub Desktop দিয়ে clone করা) connect করুন, বা Claude Code-এ repo খুলুন। Claude নিজে `CLAUDE.md` পড়ে নিয়ম জেনে নেয়। · Connect the repo folder (cloned with GitHub Desktop) in the Claude desktop app, or open it in Claude Code. Claude reads `CLAUDE.md` for the rules.

**কীভাবে বলবেন (উদাহরণ) · What to say (examples):**
- "Gallery-তে নতুন album: BUET FabLab workshop, Nov 2026। ছবি `D:\Photos\Workshop` folder-এ।" · "New gallery album: BUET FabLab workshop, Nov 2026. Photos are in `D:\Photos\Workshop`."
- "নতুন project যোগ করো: `D:\CAD\Conveyor` folder-এ STEP, render আর photo আছে।" · "Add a new project from `D:\CAD\Conveyor` (STEP, renders, photos)."
- "এই certificate যোগ করো, private নম্বরগুলো blur করে।" · "Add this certificate with the private numbers blurred."
- "নতুন paper published হয়েছে, DOI: …" · "A new paper is out, DOI: …"
- "CV-তে নতুন job যোগ করে PDF আবার বানাও।" · "Add the new job to the CV and print the PDF again."

Claude পরিবর্তন করে, check চালায়, আপনাকে দেখায়; আপনি ok বললে commit আর push করে (অথবা আপনি GitHub Desktop-এ **Push** চাপুন)। · Claude makes the change, runs the checks and shows you; after your ok it commits and pushes (or you press **Push** in GitHub Desktop).

---

## পথ ২ · Way 2: Pages CMS (browser-এ form)

**একবার সেটআপ · One-time setup**
1. `app.pagescms.org` খুলুন → **Sign in with GitHub** (আপনি নিজে sign in করবেন)। · Open `app.pagescms.org` → **Sign in with GitHub** (you sign in yourself).
2. Pages CMS-কে repo `md-zaid-hossain.github.io`-তে access দিন। · Give Pages CMS access to the repo.
3. Repo বাছুন, branch `main`। বাঁদিকে Projects, Gallery, Awards, Research, Experience, Site settings দেখাবে। · Pick the repo, branch `main`. The sidebar shows Projects, Gallery, Awards and certificates, Research, Experience, Site settings.

**সাধারণ নিয়ম · General:** form-এ বদলান → **Save** → এটাই commit। ২ মিনিট পর সাইটে দেখুন। ধূসর বা লুকানো ঘর (key, id) বদলাবেন না। · Edit the form → **Save** (that is the commit). Check the site after 2 minutes. Leave hidden fields (key, id) alone.

**Recipe: gallery-তে ছবি · Add photos to the gallery**
1. Gallery → chapter → album খুলুন (বা **Add** দিয়ে নতুন album)। · Open the album (or **Add** a new one).
2. Photos → **Add** → **Picture** → upload। নাম ছোট হাতের অক্ষর আর dash: `bracu-session-6.jpg`। · Photos → Add → Picture → upload. Name: small letters and dashes.
3. Caption লিখুন; Crop focus সাধারণত `50% 45%`। · Write a caption; crop focus is usually `50% 45%`.
4. ছবির সংখ্যা এমন রাখুন যেন শেষ সারি ভরা থাকে (৩, ৪, ৬, ৮ …)। · Keep the count so the last row is full (3, 4, 6, 8 …).
5. অন্যের তোলা ছবি হলে Photo credit লিখুন: `Photos: <নাম>`। · Third-party photos: fill Photo credit.

**Recipe: নতুন certificate · New certificate**
1. আগে ছবির private অংশ blur করুন (পথ ১ সহজ)। · Blur the private parts first (way 1 is easiest).
2. Awards and certificates → সঠিক group → Certificates → **Add**: code, name, issuer, date (`22 JUN 2025`), picture, verify link। · Pick the group → Certificates → Add: code, name, issuer, date, picture, verify link.

**Recipe: নতুন paper · New paper**
Research → Published papers → **Add**: title, authors, journal, year, DOI, abstract। In progress থেকে পুরোনো entry সরিয়ে দিন। Home page-এর paper তালিকা আর সংখ্যা Claude-কে বলে বদলান (ওগুলো code-এ)। · Research → Published → Add; remove the old entry from In progress. The Home page list and counts live in code: ask Claude.

**Recipe: নতুন project · New project**
নতুন project page-এর জন্য পথ ১ সবচেয়ে ভালো: Claude STEP থেকে 3D turntable, GLB আর render বানায়। Pages CMS-এ পুরোনো project-এর লেখা, ছবি, facts বদলান। · For a new project page use way 1 (Claude makes the 3D turntable, GLB and renders from the STEP files). Use Pages CMS to edit existing projects.

**Recipe: নতুন CV · New CV**
Site settings → CV (PDF) → নতুন PDF upload করুন (নাম একই রাখুন: `Md_Zaid_Hossain_CV.pdf`)। · Upload the new PDF with the same name.

**Recipe: নতুন চাকরি বা role · New job or role**
Experience → Work → **Add**: start (`JUL 2026`), end (খালি = এখন), role, organisation, place, what I do। · Experience → Work → Add (empty end = now).

Education আর routine form-এ নেই; ওগুলো পথ ১ বা ৩। · Education and routines are not in the editor: use way 1 or 3.

---

## পথ ৩ · Way 3: GitHub Desktop (হাতে ফাইল বদল)

**একবার সেটআপ · One-time setup**
1. Repo-টা আপনার কম্পিউটারে `D:\Profile_Portfolio\md-zaid-hossain.github.io`-এ আছে (README-র প্রথম push-এর ধাপ)। অন্য কম্পিউটারে: GitHub Desktop → **File → Clone repository**। · The repo is at `D:\Profile_Portfolio\md-zaid-hossain.github.io` (README, first push). On another computer: GitHub Desktop → File → Clone repository.
2. লেখা বদলানোর জন্য VS Code (ফ্রি) ভালো: YAML-এর ভুল রঙে দেখায়। · Use VS Code (free) to edit; it colours YAML mistakes.
3. চাইলে push-এর আগে নিজে check আর preview: `pip install pyyaml pillow`, তারপর `python checks/content_check.py` আর `python build/build.py --serve` (http://localhost:8000)। · Optional: `pip install pyyaml pillow`, then `python checks/content_check.py` and `python build/build.py --serve` to preview at http://localhost:8000.

**প্রতিবার · Every time**
1. GitHub Desktop-এ **Fetch origin** → **Pull** (Pages CMS বা Claude-এর বদল নামিয়ে নিন)। · **Fetch origin** → **Pull** first (gets changes made in Pages CMS or by Claude).
2. ছবি `media/<page>/`-এ রাখুন, যেমন `media/gallery/d3-1.jpg`। · Put files in `media/<page>/`.
3. `content/<page>.yml`-এ লিখুন, পাশের entry কপি করে বদলান। · Edit `content/<page>.yml`: copy a neighbouring entry and change it.
4. GitHub Desktop-এ বাঁদিকে বদলগুলো দেখুন → নিচে Summary লিখুন (যেমন `Gallery: workshop album`) → **Commit to main** → **Push origin**। · Review the changes → write a summary → **Commit to main** → **Push origin**.
5. GitHub-এ repo → **Actions**-এ সবুজ টিক মানে সাইট আপডেট; লাল ক্রস হলে খুলে দেখুন কোন ফাইলে কী সমস্যা। · Green tick in **Actions** = live; a red cross names the file and the problem.

**YAML-এর তিনটা নিয়ম · Three YAML rules**
- indent শুধু space দিয়ে (Tab না), প্রতি স্তরে ২টা। · Indent with spaces only (no Tab), 2 per level.
- তালিকার প্রতিটা item `- ` দিয়ে শুরু। · Each list item starts with `- `.
- লেখায় `:` বা `#` থাকলে পুরোটা quote-এ: `caption: 'Panel: FabLab network'`। · Put text with `:` or `#` in quotes.

**উদাহরণ: gallery-তে একটা ছবি · Example: one gallery photo**
```yaml
    photos:
    - image: media/gallery/d2-6.webp
      caption: The BUET FabLab team at the booth
      focus: 50% 45%
```

---

## কিছু ভুল হলে · If something goes wrong
- সাইট বদলায়নি: Actions-এ build চলছে কিনা দেখুন; ২ মিনিট পর browser-এ Ctrl+F5। · Not updated: check Actions, then reload with Ctrl+F5.
- লাল ক্রস: log-এর শেষ লাইনগুলো Claude-কে দেখান, অথবা নিজে ঠিক করুন। · Red cross: show the last log lines to Claude or fix them yourself.
- পুরোনো অবস্থায় ফেরা: GitHub Desktop → History → commit-এ right click → **Revert changes in commit** → Push। · Undo: History → right-click the commit → **Revert changes in commit** → Push.
- Pages CMS আর GitHub Desktop দুইটায় একই ফাইল একসাথে বদলাবেন না; আগে Pull করুন। · Never edit the same file in Pages CMS and on your computer at once; Pull first.
