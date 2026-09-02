# Pinnacle Digest

A code-built daily blog that turns the **Daily Accountancy Briefing** into a
dated, categorised web edition with auto-generated charts and infographics.
Static HTML, no database, no framework. Hosted free on GitHub Pages at
`https://digest.pinnacleglobalgroup.com`.

Each day: Claude reads the briefing, writes one `content/<date>.json` file, and
pushes it. GitHub builds and publishes the new edition automatically, live in a
minute or two.

## How it fits together

```
content/2026-09-02.json     <- one file per day (the day's briefing, structured)
assets/                     <- logo, favicons, styles.css
scripts/
  build.py                  <- generates the whole site into _site/
  charts.py                 <- SVG chart engine (bars, comparisons, stat tiles, gauges)
  seed_content.py           <- reference content + schema docs (the two sample days)
  new_edition.py            <- stub a blank day
.github/workflows/deploy.yml <- build + deploy on every push to main
CNAME (generated)           <- custom domain
```

The site that gets generated:

- `/` — dated archive/homepage, newest first, with a topic filter.
- `/editions/<date>/` — one full daily edition (contents, categorised stories, charts).
- `/feed.xml`, `/sitemap.xml`, `/404.html`.

## Preview it locally

```bash
python3 scripts/build.py
cd _site && python3 -m http.server 8000
# open http://localhost:8000
```

## Publishing a new day

The intended flow is that **Claude does this** each day you feed it the briefing:

1. Write `content/<YYYY-MM-DD>.json` (schema in `scripts/seed_content.py`, or
   run `python3 scripts/new_edition.py <date>` for a stub).
2. `python3 scripts/build.py` to check it renders.
3. Commit and push to `main`.

GitHub Actions rebuilds and redeploys automatically. Nothing else to do.

Content is deliberately data-only: every day is plain JSON, so the design,
charts and navigation stay consistent and you never touch HTML.

## One-time setup (GitHub + Pages + domain)

You don't have a GitHub account yet, so, in order:

1. **Create a GitHub account** at https://github.com/signup (free).
2. **Create a repository** named `pinnacle-digest` (Private is fine; Pages
   works on private repos on the free plan).
3. **Push this project** into it. From this folder:
   ```bash
   git init && git add . && git commit -m "Pinnacle Digest"
   git branch -M main
   git remote add origin https://github.com/<your-username>/pinnacle-digest.git
   git push -u origin main
   ```
   (Claude can do this step for you once the repo exists.)
4. **Turn on Pages**: repo *Settings > Pages > Build and deployment >
   Source: GitHub Actions*. The included workflow handles the rest.
5. **Custom domain** `digest.pinnacleglobalgroup.com`:
   - At your DNS provider add a `CNAME` record: host `digest` ->
     `<your-username>.github.io`.
   - The build already writes a `CNAME` file, so GitHub picks the domain up
     automatically. Tick *Enforce HTTPS* in Settings > Pages once the
     certificate is issued (a few minutes).

Want a completely different domain later (for example `dailybriefing.co`)?
Change `DOMAIN` in `scripts/build.py`, update the DNS record, and push. No
rebuild of anything else required.

## Notes

- Build has **no dependencies** beyond the Python standard library, so the
  GitHub Action is fast and cannot break on a package update. (`Pillow` is only
  needed if you ever want to regenerate favicons from the logo.)
- Dark mode, responsive layout, RSS and a print stylesheet are built in.
- No em dashes anywhere, per house style.
