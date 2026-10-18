# inqerio.com

The website is plain HTML and CSS in `site/`: upload that folder to any static host.

- Rebuild after changing the privacy policy or terms (`src/shared/legal.ts`), the brand (`src/shared/brand.ts`),
  prices or plan contents (top of `scripts/build-website.mjs`) or the styles (`website/site.css`):

  ```bash
  npm run website
  ```

- Pages: `/` home, `/pricing/`, `/privacy/`, `/terms/`, `/refunds/`, `/contact/`, `/thanks/` (where Stripe sends
  people after paying: `CHECKOUT_SUCCESS_URL`), and `404.html`.
- No cookies, analytics or scripts. Fonts and logos are served from the site itself.

## Publishing on GitHub Pages

The site is published from the repository `codesculpt/inqerio-website` (public). `site/` holds `CNAME`
(`inqerio.com`) and `.nojekyll`, which GitHub Pages needs.

First time, in Git Bash from the project folder:

```bash
cd website/site
git init -b main
git add -A
git commit -m "inqerio.com website"
git remote add origin https://github.com/codesculpt/inqerio-website.git
git push -u origin main
```

Then on GitHub: the repository's **Settings → Pages**: Source **Deploy from a branch**, branch `main`, folder
`/ (root)`, Save. Custom domain `inqerio.com`, Save; tick **Enforce HTTPS** once it is offered.

At your domain registrar (leave the Resend records alone: `send`, `resend._domainkey`, `_dmarc`):

- four `A` records for host `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  (remove any other `@` A record, such as a parking page)
- `CNAME` for host `www`: `codesculpt.github.io`

To update the site later: `npm run website`, then in `website/site`: `git add -A`, `git commit -m "Update"`,
`git push`. (`npm run website` rewrites the files but keeps the `.git` folder.)
