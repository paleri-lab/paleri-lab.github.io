# Atmospheric Boundary Layers & Turbulence Lab website

Source for the lab website, built with [Quarto](https://quarto.org) and published on GitHub Pages.
Every push to `main` rebuilds the site automatically (about 2 minutes); see **Actions** for progress.

## Three ways to edit

1. **On github.com (no install).** Open a file, click the pencil icon, edit, then **Commit changes**.
   To add a photo, open its folder (e.g. `assets/img/photos/`) and use **Add file → Upload files**.
2. **On your computer.** Clone the repo, edit in RStudio or VS Code, preview with `quarto preview`,
   then commit and push (GitHub Desktop works well).
3. **With Claude Code.** Open this folder and describe the change, e.g. "add a news post about our AGU talk".

## Where things live

| To change…                         | Edit                                   |
|------------------------------------|----------------------------------------|
| News                               | add a file in `news/` (see below)      |
| Publications                       | `data/publications.yml`                |
| People (PI bio, students, alumni)  | `data/people.yml`                      |
| Photo gallery & homepage photo strip | `data/photos.yml` + images in `assets/img/photos/` |
| Code & data cards                  | `data/code-data.yml`                   |
| Research themes and projects       | `research.qmd`                         |
| Homepage text and research cards   | `index.qmd`                            |
| Join us, Teaching                  | `join.qmd`, `teaching.qmd`             |
| Menu, site title, footer           | `_quarto.yml`                          |
| Colors and fonts                   | `assets/styles/*.scss`                 |
| Logo and browser-tab icon          | `assets/logo/`                         |

## Common recipes

**Add a news item.** Create `news/2026-11-agu-talk.qmd`:

```markdown
---
title: "Talk at AGU Fall Meeting"
date: 2026-12-10
description: "One sentence shown in the news list and on the homepage."
image: ../assets/img/photos/agu-2026.jpg   # optional
---

A paragraph or two, links, photos.
```

The four most recent items appear on the homepage automatically.

**Add a paper.** Either run

```bash
python3 scripts/add_doi.py 10.1029/2026GL012345 --featured
```

which looks the paper up on Crossref and adds it to the top of `data/publications.yml`, or copy an
existing entry in that file and edit it. Wrap lab members in `**…**` to bold them, and add new
students' family names to `LAB_MEMBERS` in `scripts/add_doi.py`. `featured: true` puts a paper
under "Recent papers" on the homepage (the first three featured papers are shown).

**Add a lab member.** Put a square photo (~600 px) in `assets/img/people/`, then add an entry to
`data/people.yml` with `group:` one of `postdoc`, `grad`, `undergrad`, `visitor` or `alumni`.

**Add a photo.** Resize to ~1600 px wide, put it in `assets/img/photos/`, and add an entry to
`data/photos.yml`. `featured: true` puts it in the homepage photo strip (first five featured).

## Preview locally

```bash
quarto preview
```

## One-time GitHub setup

Repository **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## License

Text, images and other content on this site are licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/);
see `LICENSE`. Figures reproduced from published papers remain subject to the journals' terms.
