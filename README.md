# yufandu.com

Personal site of Yufan Du. No framework, no theme — one JSON file, one template,
one Python script.

```
data/content.json      ← ALL site content lives here (papers, news, bio, …)
site/template.html     ← the single-page design (铅字与铜 / letterpress & copper)
site/build.py          ← renders template + JSON → public/
site/admin/            ← hidden editing desk, served at yufandu.com/admin/
site/assets/           ← fonts, portrait, favicon
site/uploads/          ← paper PDFs (+ optional cv.pdf, auto-linked if present)
```

## Updating content

Three equivalent ways, pick whichever is closest:

1. **The composing room** — open [yufandu.com/admin/](https://yufandu.com/admin/)
   (or type `chip` anywhere on the homepage). Paste a fine-grained GitHub PAT
   once (repo-scoped, *Contents: read and write*); add papers/news via forms or
   edit the raw JSON. "Commit & publish" pushes to `main` and the site rebuilds
   in about a minute.
2. **GitHub web UI** — edit `data/content.json` directly on github.com.
3. **Locally** — edit the JSON, `python3 site/build.py`, commit, push.

Deployment is the `build-deploy.yml` Action: every push to `main` builds
`public/` and publishes it to GitHub Pages (custom domain `yufandu.com`).

## Local preview

```
python3 site/build.py && python3 -m http.server -d public 8000
```

## History

The previous Hugo Blox site is preserved on the `legacy-hugo` branch.
