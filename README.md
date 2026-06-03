# Grenadier OBD2 — Alpha Tester Signup

Static signup page hosted on GitHub Pages, with a Cloudflare Worker proxy that forwards submissions to BetterStack.

## Repo structure

```
docs/                   ← GitHub Pages root
  index.html            ← signup form
  assets/
    AppIcon-1024.png    ← app icon (used in form header + favicon)
worker/
  worker.js             ← Cloudflare Worker source
  wrangler.toml         ← Worker config (update yourdomain.com)
harvest_testers.py      ← pull signups from BetterStack as CSV
```

## 1 · GitHub Pages

1. Push this repo to GitHub.
2. In **Settings → Pages**, set source to `main` branch, root `/`.
3. Set custom domain to `signup.alpha-grenadier-obd2.perlan.net`.
4. In Cloudflare DNS, add a **CNAME** record:
   - Name: `signup.alpha-grenadier-obd2`
   - Target: `dieterreuter.github.io`
   - Proxy: **DNS only** (grey cloud) — GitHub Pages needs this for SSL.

## 2 · Cloudflare Worker

```bash
cd worker
npm install -g wrangler        # if not already installed
wrangler login

# Set your BetterStack source token as a secret (never commit it)
wrangler secret put BETTERSTACK_TOKEN

# Edit wrangler.toml — replace yourdomain.com with your real domain
# Then deploy:
wrangler deploy
```

The Worker will be reachable at `https://log.perlan.net`.

## 3 · Connect form → Worker

In `index.html`, update the one constant at the bottom:

```js
const WORKER_URL = 'https://log.perlan.net';
```

## 4 · Harvest signups

```bash
export BETTERSTACK_TOKEN=your_token
python harvest_testers.py                  # prints CSV to stdout
python harvest_testers.py -o testers.csv   # saves to file
```
