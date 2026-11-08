# You Are Not Only the Observer

An illustrated essay by Merary Rodríguez.

## Maintain and preview

Use Python 3.10 or newer. The build and text verifier use the standard library.

```sh
python3 build.py
python3 verify.py
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000/`. The checked-in production directory is `docs/`.

- `essay.md` is the canonical essay. `source-integrity.json` records its approved SHA-256. Change that lock only when an author-approved canonical revision is ready.
- `template.html` contains the page structure and source notes. `build.py` renders the canonical text into `docs/index.html`. Make HTML changes in the template and regenerate the output.
- `docs/styles.css` and `docs/journey.css` contain the styles. `docs/script.js` and `docs/journey.js` control the scroll and reduced-motion behavior. WebP images and fonts live under `docs/assets/`.
- Before committing a release, rebuild, run the text verifier, and review the diff to `docs/`. Regenerate the inventory with `python3 release_manifest.py`. Use `python3 release_manifest.py --check` to detect inventory or byte changes.

See [ATTRIBUTION.md](ATTRIBUTION.md) for credits and license information.

## Proposed GitHub Pages deployment

The proposed standalone project is `Meraryr/you-are-not-only-the-observer`. The steps below apply after the owner authorizes deployment.

1. Create a new empty repository under `Meraryr`. A public repository is the proposed setup for Pages on GitHub Free. Confirm the name is available at creation.
2. Extract the source ZIP. From its repository root, run the build, verifier, and manifest check. Commit the release files to `main` and push them to the new repository.
3. In the new repository, open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select **main** and **/docs**, then save.
4. Wait for the Pages deployment to complete. Open the URL GitHub reports. The expected project address is `https://meraryr.github.io/you-are-not-only-the-observer/`. Check the directory URL, `index.html`, the scroll reveals, keyboard navigation, and the references disclosure.
5. For maintenance, rebuild and verify before pushing updated `docs/` files. Pages redeploys changes from the configured source.

GitHub documentation for [branch publishing](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) and [Pages availability](https://docs.github.com/en/pages/quickstart). The `.nojekyll` marker is included in `docs/`. The publish root contains only the generated page, site scripts and styles, images, fonts, and the font notice. Recovery editions are archived separately.
