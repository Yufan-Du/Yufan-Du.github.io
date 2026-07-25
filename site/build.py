#!/usr/bin/env python3
"""Render data/content.json + site/template.html -> public/.

No dependencies beyond the standard library. Run from repo root:
    python3 site/build.py
"""
import html
import json
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "public"

NEWS_VISIBLE = 6  # newest items shown; the rest collapse under <details>


def esc(s):
    return html.escape(s, quote=True)


def month_label(ym):
    """'2026-06' -> 'Jun 2026'"""
    d = datetime.strptime(ym, "%Y-%m")
    return d.strftime("%b %Y")


def render_links(meta):
    items = [("email", "mailto:" + meta["email"])]
    for key in ("scholar", "github", "linkedin"):
        if meta.get(key):
            items.append((key, meta[key]))
    items.append(("cv", "uploads/cv.pdf")) if (SITE / "uploads" / "cv.pdf").exists() else None
    return "\n".join(
        f'<a href="{esc(url)}"{" rel=me" if key != "email" else ""}>{key}</a>'
        for key, url in items
    )


def render_role_line(about):
    return (
        f'{esc(about["role"])} · <a href="{esc(about["affiliationUrl"])}">{esc(about["affiliation"])}</a>'
        f' · <a href="{esc(about["labUrl"])}">{esc(about["lab"])}</a>, advised by'
        f' <a href="{esc(about["advisorUrl"])}">Prof. {esc(about["advisor"])}</a>'
    )


def render_news(news):
    news = sorted(news, key=lambda n: n["date"], reverse=True)
    lis = [
        f'    <li><time datetime="{esc(n["date"])}">{month_label(n["date"])}</time><span>{n["text"]}</span></li>'
        for n in news
    ]
    if len(lis) <= NEWS_VISIBLE:
        return "\n".join(lis)
    head = "\n".join(lis[:NEWS_VISIBLE])
    tail = "\n".join(lis[NEWS_VISIBLE:])
    n_more = len(lis) - NEWS_VISIBLE
    return (
        head
        + f'\n  </ul>\n  <details><summary class="more">{n_more} older items</summary><ul class="news">\n'
        + tail
        + "\n  </ul></details>\n  <ul hidden>"
    )


def render_authors(authors, me):
    parts = []
    for a in authors:
        star = a.endswith("*")
        name = a.rstrip("*")
        h = esc(name)
        if name == me:
            h = f"<b>{h}</b>"
        parts.append(h + ("*" if star else ""))
    return ", ".join(parts)


def render_publications(pubs, me):
    pubs = sorted(pubs, key=lambda p: (-int(p["year"]), p["venue"]))
    any_star = any(a.endswith("*") for p in pubs for a in p["authors"])
    out, year_open = [], None
    for p in pubs:
        if p["year"] != year_open:
            if year_open is not None:
                out.append("    </div>\n  </div>")
            out.append(
                f'  <div class="pubyear">\n    <div class="y">{p["year"]}</div>\n    <div>'
            )
            year_open = p["year"]
        title = esc(p["title"])
        if p.get("pdf"):
            title = f'<a href="{esc(p["pdf"])}">{title}</a>'
        meta = [f'<span>{esc(p["venue"])}</span>']
        if p.get("area"):
            meta.append(f'<span class="area">{esc(p["area"])}</span>')
        if p.get("award"):
            meta.append(f'<span class="award">{esc(p["award"])}</span>')
        if p.get("pdf"):
            meta.append(f'<a href="{esc(p["pdf"])}">pdf</a>')
        out.append(
            f'      <article class="pub">\n'
            f'        <h3 class="t">{title}</h3>\n'
            f'        <p class="a">{render_authors(p["authors"], me)}</p>\n'
            f'        <p class="m">{"".join(meta)}</p>\n'
            f"      </article>"
        )
    if year_open is not None:
        out.append("    </div>\n  </div>")
    if any_star:
        out.append('  <p class="eqnote">* equal contribution</p>')
    return "\n".join(out)


def render_education(edu):
    return "\n".join(
        f'        <li><time>{esc(e["years"])}</time>'
        f'<span><span class="deg">{esc(e["degree"])}</span> · '
        f'<span class="sch">{esc(e["school"])}</span></span></li>'
        for e in edu
    )


def render_route(words):
    """words joined by animated wires; staggered delays make one signal relay
    left-to-right: word-wave -> wire-pulse -> word-wave -> ... -> ending via."""
    if not words:
        return ""
    cycle, step = 9.0, 0.62
    parts, i = [], 0
    for k, w in enumerate(words):
        parts.append(f'<span class="w" style="--cycle:{cycle}s;--d:{i*step:.2f}s">{esc(w)}</span>')
        i += 1
        last = k == len(words) - 1
        cls = "wire term" if last else "wire"
        parts.append(f'<span class="{cls}" style="--cycle:{cycle}s;--d:{i*step:.2f}s" aria-hidden="true"></span>')
        i += 1
    return ('<div class="route" role="img" aria-label="research path: '
            + esc(" to ".join(words)) + '">' + "".join(parts) + "</div>")


def render_experience(exp):
    lis = []
    for e in sorted(exp, key=lambda e: e["start"], reverse=True):
        span = month_label(e["start"]) + " – " + (month_label(e["end"]) if e.get("end") else "now")
        org = f'<a href="{esc(e["orgUrl"])}">{esc(e["org"])}</a>' if e.get("orgUrl") else esc(e["org"])
        lis.append(
            f'    <li><time>{esc(span)}</time><div>'
            f'<span class="r">{esc(e["role"])}</span> · <span class="o">{org}, {esc(e["location"])}</span>'
            f'<div class="n">{esc(e["note"])}</div></div></li>'
        )
    return "\n".join(lis)


def render_projects(projects):
    lis = []
    for p in projects:
        name = f'<a href="{esc(p["url"])}">{esc(p["name"])}</a>' if p.get("url") else esc(p["name"])
        lis.append(
            f'    <li><span class="pn">{name}</span> — <span class="pd">{p["note"]}</span></li>'
        )
    return "\n".join(lis)


def render_jsonld(c):
    meta, about = c["meta"], c["about"]
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": meta["name"],
            "url": "https://yufandu.com/",
            "image": "https://yufandu.com/assets/portrait.jpg",
            "jobTitle": about["role"],
            "affiliation": {"@type": "Organization", "name": about["affiliation"]},
            "alumniOf": "Peking University",
            "sameAs": [u for u in (meta.get("github"), meta.get("linkedin"), meta.get("scholar")) if u],
        },
        separators=(",", ":"),
    )


def render_map_page(c):
    script = c["footer"].get("visitorsMapScript", "")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Visitor map — {esc(c['meta']['name'])}</title><meta name="robots" content="noindex">
<style>body{{font-family:Georgia,serif;background:#faf7f1;color:#211d19;max-width:44rem;margin:3rem auto;padding:0 1.2rem}}
a{{color:#a2542c}}</style></head>
<body><p><a href="../">&larr; back</a></p><h1>Visitor map</h1>
<div><script type="text/javascript" id="mapmyvisitors" src="{esc(script)}"></script></div>
</body></html>"""


def main():
    c = json.loads((ROOT / "data" / "content.json").read_text())
    tpl = (SITE / "template.html").read_text()
    me = c["meta"]["highlightAuthor"]

    about_paras = "\n".join(f"      <p>{p}</p>" for p in c["about"]["paragraphs"])
    interests = "Interests: " + " · ".join(f"<em>{esc(i)}</em>" for i in c["about"]["interests"])

    portraits = c["about"].get("portraits", [])
    for p in portraits:
        for ext in (".jpg", ".webp"):
            f = SITE / "assets" / (Path(p["img"]).name + ext)
            assert f.exists(), f"portrait missing: {f}"

    repl = {
        "{{TITLE}}": esc(c["meta"]["title"]),
        "{{DESCRIPTION}}": esc(c["meta"]["description"]),
        "{{JSONLD}}": render_jsonld(c),
        "{{NAME}}": esc(c["meta"]["name"]),
        "{{ROLE_LINE}}": render_role_line(c["about"]),
        "{{LINKS}}": render_links(c["meta"]),
        "{{PORTRAITS}}": json.dumps(portraits, separators=(",", ":")),
        "{{ABOUT_PARAGRAPHS}}": about_paras,
        "{{INTERESTS}}": interests,
        "{{EDUCATION}}": render_education(c["about"]["education"]),
        "{{ROUTE}}": render_route(c.get("route", [])),
        "{{NEWS}}": render_news(c["news"]),
        "{{PUBLICATIONS}}": render_publications(c["publications"], me),
        "{{EXPERIENCE}}": render_experience(c["experience"]),
        "{{PROJECTS}}": render_projects(c["projects"]),
        "{{YEAR}}": str(date.today().year),
        "{{COLOPHON}}": esc(c["footer"]["colophon"]),
    }
    out = tpl
    for k, v in repl.items():
        assert k in out, f"placeholder {k} missing from template"
        out = out.replace(k, v)
    leftovers = [t for t in ("{{", "}}") if t in out]
    assert not leftovers, "unreplaced placeholders remain"

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "index.html").write_text(out)
    (OUT / "CNAME").write_text("yufandu.com\n")
    (OUT / ".nojekyll").write_text("")
    (OUT / "map").mkdir()
    (OUT / "map" / "index.html").write_text(render_map_page(c))
    shutil.copytree(SITE / "assets", OUT / "assets")
    shutil.copytree(SITE / "uploads", OUT / "uploads")
    if (SITE / "admin").exists():
        shutil.copytree(SITE / "admin", OUT / "admin")
    # data/content.json is served too, so the admin panel can load it same-origin
    (OUT / "data").mkdir()
    shutil.copy(ROOT / "data" / "content.json", OUT / "data" / "content.json")
    print(f"built {OUT} ({sum(f.stat().st_size for f in OUT.rglob('*') if f.is_file()) // 1024} KB)")


if __name__ == "__main__":
    sys.exit(main())
