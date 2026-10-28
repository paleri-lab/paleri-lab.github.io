#!/usr/bin/env python3
"""Add a paper to data/publications.yml from its DOI.

Usage:
    python3 scripts/add_doi.py 10.1029/2022JD037138 [--featured]

Fetches the title, authors, journal and year from Crossref and inserts a new entry at the
top of the list. Lab members listed in LAB_MEMBERS are bolded. Check the entry afterwards:
Crossref metadata is sometimes incomplete (e.g. missing volume or pages).
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

LAB_MEMBERS = ["Paleri"]  # family names to bold; add students as they join
PUBS = Path(__file__).resolve().parent.parent / "data" / "publications.yml"
TYPES = {"journal-article": "article", "book-chapter": "chapter", "posted-content": "preprint",
         "proceedings-article": "conference"}


def fetch(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "paleri-lab-site (mailto:paleri@tamu.edu)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["message"]


def initials(given):
    parts = re.split(r"[\s.]+", given or "")
    return " ".join(p[0] + "." for p in parts if p)


def author_list(authors):
    names = []
    for a in authors:
        name = f"{a.get('family', '')}, {initials(a.get('given'))}".strip(", ")
        if a.get("family") in LAB_MEMBERS:
            name = f"**{name}**"
        names.append(name)
    return ", ".join(names)


def q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", args[0].strip())
    text = PUBS.read_text()
    if doi.lower() in text.lower():
        sys.exit(f"{doi} is already in {PUBS.name}")
    m = fetch(doi)
    year = (m.get("published-print") or m.get("published-online") or m.get("issued"))["date-parts"][0][0]
    venue = (m.get("container-title") or [m.get("publisher", "")])[0]
    extra = ", ".join(x for x in [m.get("volume"), m.get("page")] if x)
    entry = [
        f"- title: {q(' '.join(m['title'][0].split()))}",
        f"  authors: {q(author_list(m.get('author', [])))}",
        f"  venue: {q(venue + (', ' + extra if extra else ''))}",
        f"  year: {year}",
        f"  type: {TYPES.get(m.get('type'), 'article')}",
        f"  doi: {q(doi)}",
    ]
    if "--featured" in sys.argv:
        entry.append("  featured: true")
    # insert before the first existing entry so the list stays newest-first
    i = text.find("\n- ")
    text = text[: i + 1] + "\n".join(entry) + "\n\n" + text[i + 1 :] if i >= 0 else text.rstrip() + "\n\n" + "\n".join(entry) + "\n"
    PUBS.write_text(text)
    print("Added:\n" + "\n".join(entry))


if __name__ == "__main__":
    main()
