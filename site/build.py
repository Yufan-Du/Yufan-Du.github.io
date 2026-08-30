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
    labels = {"scholar": "google scholar"}
    for key in ("scholar", "github", "linkedin"):
        if meta.get(key):
            items.append((labels.get(key, key), meta[key]))
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
    for seq, p in enumerate(pubs):
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
        quip = ""
        if p.get("quip"):
            conf, _, yr = p["venue"].rpartition(" ")
            lot = f"LOT YFD-{int(yr) % 100:02d}{chr(65 + seq % 26)}·{conf.upper().replace(' ', '')}"
            quip = (
                f'\n        <p class="q"><span class="lot">{esc(lot)}</span> — {esc(p["quip"])}</p>'
            )
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
            f'        <p class="m">{"".join(meta)}</p>{quip}\n'
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


def render_now_page(c):
    now = c.get("now", {})
    items = "\n".join(f'      <li>{i}</li>' for i in now.get("items", []))
    name = esc(c["meta"]["name"])
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Now — {name}</title>
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<style>
@font-face {{ font-family:'Newsreader'; font-style:normal; font-weight:200 800; font-display:swap;
  src:url('../assets/newsreader-var.woff2') format('woff2'); }}
@font-face {{ font-family:'Newsreader'; font-style:italic; font-weight:200 800; font-display:swap;
  src:url('../assets/newsreader-var-italic.woff2') format('woff2'); }}
:root {{ --paper:#faf7f1; --ink:#211d19; --ink-soft:#57504a; --ink-faint:#8d857c;
  --hairline:#e3dcd2; --copper:#a2542c;
  --serif:'Newsreader','Iowan Old Style',Georgia,serif;
  --mono:ui-monospace,'SF Mono',Menlo,Consolas,monospace; }}
@media (prefers-color-scheme: dark) {{ :root {{ --paper:#191512; --ink:#eae3d8; --ink-soft:#b3a99c;
  --ink-faint:#7d746a; --hairline:#322b25; --copper:#d18f62; }} }}
body {{ margin:0; background:var(--paper); color:var(--ink); font-family:var(--serif);
  font-size:clamp(16.5px,1vw + 12px,18.5px); line-height:1.62; }}
.page {{ max-width:38rem; margin:0 auto; padding:clamp(2rem,8vh,4.5rem) 1.2rem 3rem; }}
a {{ color:inherit; text-decoration:underline;
  text-decoration-color:color-mix(in srgb, var(--copper) 45%, transparent);
  text-underline-offset:2.5px; }}
a:hover {{ color:var(--copper); }}
.crumb {{ font-family:var(--mono); font-size:.72rem; letter-spacing:.06em; }}
.crumb a {{ text-decoration:none; color:var(--ink-faint); }}
.crumb a:hover {{ color:var(--copper); }}
h1 {{ font-weight:560; font-size:2.1rem; margin:1rem 0 .2rem; }}
.stamp {{ font-family:var(--mono); font-size:.68rem; letter-spacing:.1em; color:var(--ink-faint);
  text-transform:uppercase; margin-bottom:1.8rem; }}
.stamp b {{ color:var(--copper); font-weight:400; }}
ul {{ list-style:none; margin:0; padding:0; }}
li {{ padding:.55rem 0 .55rem 1.4rem; position:relative; }}
li::before {{ content:'●'; position:absolute; left:.15rem; top:.95em; font-size:.5em; color:var(--copper); }}
.foot {{ margin-top:2.5rem; padding-top:1rem; border-top:1px solid var(--hairline);
  font-family:var(--mono); font-size:.68rem; color:var(--ink-faint); font-style:italic; }}
</style></head>
<body><div class="page">
  <p class="crumb"><a href="../">&larr; yufandu.com</a></p>
  <h1>Now</h1>
  <p class="stamp">what I'm doing these days · updated <b>{esc(now.get("updated", ""))}</b></p>
  <ul>
{items}
  </ul>
  <p class="foot">This is a <a href="https://nownownow.com/about">now page</a>. It changes when life does.</p>
</div></body></html>"""


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
    (OUT / "now").mkdir()
    (OUT / "now" / "index.html").write_text(render_now_page(c))
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
