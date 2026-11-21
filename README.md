# md-zaid-hossain.github.io

Portfolio of Md. Zaid Hossain · Industrial Engineer · https://md-zaid-hossain.github.io

```
content/        text and lists, one YAML file per page (projects: one file each)
media/          pictures, clips, 3D models and the CV, one folder per page
build/          build.py (content + media -> dist/), site_src/ (the page builders), assets/ (fonts, site.js, favicon)
checks/         content_check.py (privacy and text rules), dashinv.py and widths.py (checks on the built site)
cv-source/      cv.html and pdf.js for the one-page CV
tools/          make_pages_yml.py (writes .pages.yml for the Pages CMS editor)
.pages.yml      Pages CMS editor forms (app.pagescms.org)
.github/        deploy.yml: check, build and publish on every push to main
CLAUDE.md       rules for Claude sessions
UPDATING.md     how to update the site (Bangla and English)
```

Local preview: `pip install pyyaml pillow` then `python3 build/build.py --serve` and open http://localhost:8000
