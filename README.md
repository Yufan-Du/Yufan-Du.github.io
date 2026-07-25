# yufandu.com

Personal site of Yufan Du. Hand-built static site — no framework, no theme.

```
data/content.json      ← site content
site/template.html     ← the single-page design
site/build.py          ← renders template + JSON → public/
site/assets/           ← fonts, images, favicon
site/uploads/          ← paper PDFs
```

Every push to `main` triggers the `build-deploy.yml` Action, which builds
`public/` and publishes it to GitHub Pages.

## Local preview

```
python3 site/build.py && python3 -m http.server -d public 8000
```

The previous Hugo site is preserved on the `legacy-hugo` branch.
