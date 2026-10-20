# Redesign report — branch `redesign` (2026-10-20)

Not pushed, not merged, not deployed. `main` untouched.

## Commits
1. Phase 1: redesign audit (docs/redesign-audit.md), self-hosted Manrope subsets
2. Phase 2: design system (tokens, type scale, components) in assets/site.css; real product imagery and OG image
3. Phase 3: new header, hero, product showcase (bento + teasers), about, beta, footer; privacy page on shared stylesheet
4. Phase 4: polish — hero and showcase fixes on narrow screens, wrap-safe hero facts, mobile composition
5. Phase 5: validation notes (this file)

## What changed
- **System:** one stylesheet `assets/site.css` with CSS custom properties (color, type scale, spacing, radius, elevation, motion). Single family Manrope (variable 200–800), self-hosted woff2 in `assets/fonts/` with latin + latin-ext subsets (Polish diacritics verified). Google Fonts removed. Base components: `.btn` (+primary/quiet), `.tag` (live/soon/dev), `.link`, `.meta`, `.lead`.
- **Header:** sticky, translucent, 64 px; brand mark + wordmark; nav Games / Apps / About / Beta; EN/PL switch (44 px targets); mobile menu button with `aria-expanded`/`aria-controls`, Escape closes, links close.
- **Hero:** editorial split; headline "Small games. Big personality." (PL: "Małe gry. Duża osobowość."), accent on one word, lead, two CTAs, three facts. Right: real Sushi Rush gameplay frame in a tilted phone, logo overlapping, "Playable now" tag. On narrow screens the logo is dropped and the phone stands alone (the logo appears in the card below).
- **Showcase:** "Available now" bento — Sushi Rush (8/12, art + menu frame + logo, Play now + beta link) and Kropla (4/12, two real App Store screenshots, Download on the App Store). "In development" — three deliberately different teasers: Pendulum (store screenshot rising from the bottom, night palette), Whirlpick (rotated screenshot, violet), Iskra (typographic composition with icon + "2027", no gameplay shown).
- **About:** "Independent by design." — two-column editorial text + numbered value list with hairlines (no cards).
- **Beta:** kept the working Supabase form; now a two-column band with the privacy link; honeypot + validation unchanged.
- **Footer:** four columns (brand, products, studio, contact) + bottom line; only existing links (App Store, GitHub repo, privacy, e-mail).
- **Privacy page:** same system; EN/PL; per-app policy links verified (all 200).
- **Meta:** description (EN + PL), Open Graph + Twitter card with generated `assets/og.jpg` (1200×630), theme-color, favicon, apple-touch-icon; `lang` updates with the switcher, `<title>` per language.
- **Images:** webp, explicit width/height, `loading="lazy"` below the fold, hero image `fetchpriority="high"`.
- **Motion:** IntersectionObserver reveals (once, 320 ms), hover lifts, phone nudges; everything disabled under `prefers-reduced-motion`; no animated backgrounds (the old particle canvas is gone).

## Design decisions
- **Type:** Manrope. Geometric but warm, excellent Polish diacritics, one family covers display (weight 500, tight tracking) and UI. Hierarchy from scale and spacing, not from bold everywhere.
- **Palette:** near-black ink (#0b0c10) with three layered surfaces, warm off-white text, one amber accent (#f3a35a) kept from the previous brand, plus per-product accents (sushi coral, kropla blue, pendulum gold, whirlpick violet, iskra amber) used sparingly as backgrounds in the teasers.
- **Hero concept:** the product is the hero — a real gameplay frame on a tilted phone, with the headline doing the talking. No illustration, no gradient blob.

## Product inventory as implemented
| Product | Status | CTA | Imagery |
|---|---|---|---|
| Sushi Rush: Merge Kitchen | Available · browser | Play now → `play/sushi-rush/`; "Get the mobile beta" → #beta | own logo + bg, real gameplay frame and menu frame (trailer recordings) |
| Kropla | Available · App Store (Android in testing) | Download on the App Store | two real App Store screenshots (today, dark mode) |
| Pendulum: Rope Swing | In review (iPhone) | Coming soon · join the beta | real store screenshot |
| Whirlpick | In review (iPhone) | Coming soon · join the beta | real store screenshot |
| Iskra | In development (2027) | none (text) | app icon only; typographic composition |

## Discrepancies and resolutions
See `docs/redesign-audit.md` §"Discrepancies". Summary: repo had no screenshots for Kropla/Pendulum/Whirlpick → added the apps' own real store screenshots (not stock, not invented); no social accounts → footer shows e-mail + GitHub only; headline replaced per prompt; font limited to the allowed list (Manrope).

## Validation
- **Lint/build:** the project has no lint or build scripts (static HTML/CSS). HTML validated by inspection; CSS loads without console errors.
- **Base path:** served locally at `http://localhost:5190/firewisp-studio/` (symlink mirroring GitHub Pages). All relative asset paths, `play/sushi-rush/` and `privacy.html` resolve.
- **Links:** every external link returns 200 (App Store, GitHub repo, four legal pages). Local assets all exist.
- **Language:** switcher works, `lang` and `<title>` update, choice persists across reload (localStorage), default from browser language.
- **Viewports:** 320, 375, 768, 1024, 1440 — `scrollWidth == innerWidth` in both EN and PL (no horizontal overflow). Mobile menu opens/closes with correct `aria-expanded`.
- **Browser testing:** performed in the desktop app's built-in browser (Chromium): screenshots inspected at 375 (PL), 768 (EN), 1024 (PL) and 1440; fixes applied after inspection (hero composition, facts separators, Sushi card phone/logo overlap). Screenshots were not saved to the repository.

## Known issues / next steps
- The desktop app's preview pane shows only the top ~645 px of an emulated 812 px viewport, so full-height mobile screenshots were verified by measurement (DOM rects) rather than pixels below that line.
- `play/sushi-rush/` is a 62 MB Flutter build committed to the repo; consider moving large builds to releases or an asset host before the repo grows.
- Kropla screenshots are in Polish (the app's primary market); English ones can be swapped in when exported.
- Fonts: the Manrope subsets come from Google's served files (latin, latin-ext) — a locally subset copy with `pyftsubset` would be slightly smaller.
