# Redesign audit — Firewisp Studio (branch `redesign`, 2026-10-20)

## Stack
Static site, no build step, no lint, no package manager: `index.html` (single file: CSS + JS inline), `privacy.html`, `assets/` (webp icons + Sushi Rush art), `play/sushi-rush/` (Flutter web build, ~62 MB, base href `/firewisp-studio/play/sushi-rush/`). Hosted on GitHub Pages from `main`, base path `/firewisp-studio/`. i18n: duplicated nodes with `data-l="en|pl"`, toggled by JS, choice stored in `localStorage` (`fw-lang`), default from `navigator.language`. Fonts loaded from Google Fonts (to be replaced: must be self-hosted). Beta form posts to Supabase REST (anon insert) — functional, must be kept.

## Product inventory (from the repository)
| Product | Status in repo | Platform | Link | Imagery in repo | PL/EN |
|---|---|---|---|---|---|
| Sushi Rush: Merge Kitchen | playable now (browser) | web (stores: "soon") | `play/sushi-rush/` | `assets/sushi-logo.webp`, `assets/sushi-bg.webp`, `assets/icon-sushi-rush.webp` | yes |
| Kropla | App Store (live) | iPhone; Android "in testing" (no link) | https://apps.apple.com/app/id6805807230 | `assets/icon-kropla.webp` only | yes |
| Pendulum | coming soon, "iPhone: in review" | iPhone | none | `assets/icon-pendulum.webp` | yes |
| Whirlpick | coming soon, "iPhone: in review" | iPhone | none | `assets/icon-whirlpick.webp` | yes |
| Iskra | in development, "2027" | — | none | `assets/icon-firewisp.webp` | yes |

Other content to keep: beta list form (Supabase), three principles ("no ads / no tracking / no dark patterns"), privacy page (PL/EN) with links to per-app policies on `tomaszmatusiak-stack.github.io/legal/…`, contact e-mail, footer.

## Weaknesses of the current design
- Hero is the generic "text left, decoration right" with an animated particle canvas (an animated background; prompt forbids it).
- Products are an identical card grid; every status looks the same; no real product imagery beyond icons; Sushi Rush art appears once.
- Typography: three families (display grotesque + body + mono), bold headlines everywhere; hierarchy comes from weight, not scale/spacing.
- No mobile navigation (nav links simply hidden under 720 px); language switch is the only interactive element in the header.
- Google Fonts dependency (external request, no self-hosting).
- No entrance motion, no reduced-motion nuance beyond hiding the canvas; images without explicit dimensions (layout shift); no Open Graph image sized for sharing; no `lang`-specific meta.
- Privacy page styled separately from the main page (duplicated tokens).

## Discrepancies between the prompt and the repository
1. **Kropla "real screenshots or previews"**: the repo has only the icon. Real App Store screenshots exist in the app's own project (`mobile/kropla/ios/appstore`); they are the studio's own assets, not stock, so they are added to `assets/` in Phase 3. Same for Pendulum and Whirlpick (their store screenshots) and a real gameplay frame of Sushi Rush from the trailer recording. Nothing is invented.
2. **"Available now / In development" grouping**: repo statuses map cleanly: available = Sushi Rush (browser), Kropla (App Store); in development = Pendulum, Whirlpick ("in review"), Iskra ("2027").
3. **Social links**: the repo has none (only e-mail and GitHub Pages host). Footer gets e-mail + privacy + product links only; the GitHub repository link is added because it exists and is public.
4. **Hero copy**: prompt fixes "Small games. Big personality."; the repo's current headline is replaced (headline is copy, not a product fact).
5. **Font choice**: prompt restricts to Inter/Geist/Manrope/Plus Jakarta Sans; chosen: Manrope (variable, self-hosted, latin + latin-ext subsets).
6. **Kropla privacy claim** ("everything stays on your phone"): supported by the existing repo copy and the app's own policy; kept.
