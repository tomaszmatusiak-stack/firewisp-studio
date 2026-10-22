#!/usr/bin/env python3
"""Ramka strony + ekran ładowania dla gier Fluttera w przeglądarce (play/<gra>/), wersja v3 (styl strony studia).

  flutter_splash.py <katalog_projektu> --title ... --tagline-en ... --tagline-pl ... [--logo <ścieżka w assets>] [--bg #hex] [--accent #hex] [--landscape] [--description ...]

Nadpisuje web/index.html i web/flutter_bootstrap.js.
- Pasek u góry („← Firewisp Studio”, tytuł gry, pełny ekran, schowaj); schowany = mały przycisk powrotu w rogu.
  Na niskich ekranach (telefon poziomo) pasek startuje schowany. Wybór pamiętany w localStorage `fw-bar`.
- Gra renderuje się w <div id="game"> (hostElement), więc pasek nie zasłania UI gry.
- Splash: tło nocy jak na stronie, logo gry (albo tytuł w Fraunces), pasek postępu liczony z realnego pobierania
  main.dart.js i właściwego wariantu CanvasKit (chromium albo pełny, ten sam, który zaraz weźmie loader Fluttera).
- Fonty: ../../assets/fonts/ (self-hosted na stronie), z zapasem systemowym.
"""
import argparse, pathlib, html

ap = argparse.ArgumentParser()
ap.add_argument('dir'); ap.add_argument('--title', required=True)
ap.add_argument('--tagline-en', required=True); ap.add_argument('--tagline-pl', required=True)
ap.add_argument('--logo', default=''); ap.add_argument('--bg', default='#07131B'); ap.add_argument('--accent', default='#FF8A43')
ap.add_argument('--landscape', action='store_true'); ap.add_argument('--description', default='')
a = ap.parse_args()
web = pathlib.Path(a.dir) / 'web'
T = html.escape(a.title)
logo_html = f'<img class="logo" src="{a.logo}" alt="">' if a.logo else f'<div class="logo-text">{T}</div>'
rot = ('<p class="hint" data-l="en">Best played with the phone turned sideways.</p>'
       '<p class="hint" data-l="pl">Najlepiej gra się z telefonem obróconym bokiem.</p>') if a.landscape else ''
FLAME = ('<svg viewBox="0 0 100 140" aria-hidden="true"><defs><linearGradient id="fg" x1="0" x2="0" y1="0" y2="1">'
         '<stop offset="0" stop-color="#FFC25A"/><stop offset=".45" stop-color="#FF9A3E"/><stop offset="1" stop-color="#FF5A3C"/></linearGradient></defs>'
         '<path fill="url(#fg)" d="M50 0C68 25 100 48 100 92c0 27-22 48-50 48S0 119 0 92C0 48 32 25 50 0z"/>'
         '<circle cx="35" cy="86" r="11" fill="#fff"/><circle cx="65" cy="86" r="11" fill="#fff"/>'
         '<circle cx="37" cy="88" r="5.5" fill="#2A1A12"/><circle cx="67" cy="88" r="5.5" fill="#2A1A12"/>'
         '<path d="M38 106q12 10 24 0" stroke="#2A1A12" stroke-width="4" fill="none" stroke-linecap="round"/></svg>')

index = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <base href="$FLUTTER_BASE_HREF">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
  <meta name="description" content="{html.escape(a.description or a.tagline_en)}">
  <meta name="theme-color" content="{a.bg}">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black">
  <meta name="apple-mobile-web-app-title" content="{T}">
  <meta property="og:title" content="{T} — Firewisp Studio">
  <meta property="og:description" content="{html.escape(a.description or a.tagline_en)}">
  <link rel="apple-touch-icon" href="icons/Icon-192.png">
  <link rel="icon" type="image/png" href="favicon.png"/>
  <title>{T}</title>
  <link rel="manifest" href="manifest.json">
  <style>
    @font-face {{ font-family: "Fraunces"; src: url("../../assets/fonts/fraunces-latin-ext.woff2") format("woff2"); font-weight: 300 900; font-display: swap; unicode-range: U+0100-02BA, U+1E00-1EFF; }}
    @font-face {{ font-family: "Fraunces"; src: url("../../assets/fonts/fraunces-latin.woff2") format("woff2"); font-weight: 300 900; font-display: swap; unicode-range: U+0000-00FF, U+2000-206F; }}
    @font-face {{ font-family: "Manrope"; src: url("../../assets/fonts/manrope-latin-ext.woff2") format("woff2"); font-weight: 200 800; font-display: swap; unicode-range: U+0100-02BA, U+1E00-1EFF; }}
    @font-face {{ font-family: "Manrope"; src: url("../../assets/fonts/manrope-latin.woff2") format("woff2"); font-weight: 200 800; font-display: swap; unicode-range: U+0000-00FF, U+2000-206F; }}
    :root {{ --bar: 48px; --night: #07131B; --cream: #F5F1E9; --muted: #AABCC5; --amber: {a.accent}; }}
    html, body {{ margin: 0; height: 100%; background: {a.bg}; overflow: hidden; }}
    body {{ display: flex; flex-direction: column; font-family: "Manrope", system-ui, -apple-system, "Segoe UI", sans-serif; }}
    #game {{ flex: 1 1 auto; min-height: 0; position: relative; }}
    #game > * {{ position: absolute; inset: 0; }}
    /* ── pasek studia ── */
    #fw-bar {{ flex: none; height: var(--bar); display: flex; align-items: center; gap: 10px; padding: 0 10px 0 6px; background: rgba(7,19,27,.92); border-bottom: 1px solid rgba(40,66,75,.7); color: var(--cream); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); transition: height .25s ease, opacity .25s ease; overflow: hidden; }}
    #fw-bar a, #fw-bar button {{ display: inline-flex; align-items: center; gap: 8px; height: 36px; padding: 0 10px; border-radius: 999px; border: 0; background: none; color: var(--muted); font: inherit; font-size: 14px; font-weight: 600; text-decoration: none; cursor: pointer; white-space: nowrap; }}
    #fw-bar a:hover, #fw-bar button:hover {{ color: var(--cream); background: rgba(255,255,255,.06); }}
    #fw-bar .brand svg {{ width: 18px; height: 25px; }}
    #fw-bar .brand b {{ font-family: "Fraunces", Georgia, serif; font-weight: 600; font-size: 16px; color: var(--cream); }}
    #fw-bar .title {{ flex: 1; text-align: center; font-family: "Fraunces", Georgia, serif; font-size: 16px; color: var(--cream); overflow: hidden; text-overflow: ellipsis; }}
    #fw-bar .ico {{ width: 18px; height: 18px; }}
    #fw-bar .fs {{ display: none; }} .has-fs #fw-bar .fs {{ display: inline-flex; }}
    body.bar-hidden #fw-bar {{ height: 0; opacity: 0; pointer-events: none; }}
    #fw-tab {{ position: fixed; left: 8px; bottom: 8px; z-index: 9; width: 36px; height: 36px; border-radius: 50%; border: 1px solid rgba(255,255,255,.18); background: rgba(7,19,27,.6); color: var(--cream); display: none; align-items: center; justify-content: center; cursor: pointer; opacity: .55; transition: opacity .2s; }}
    #fw-tab:hover {{ opacity: 1; }} #fw-tab svg {{ width: 18px; height: 18px; }}
    body.bar-hidden #fw-tab {{ display: inline-flex; }}
    @media (max-width: 520px) {{ #fw-bar .title {{ display: none; }} #fw-bar .brand b {{ font-size: 15px; }} }}
    /* ── splash ── */
    #splash {{ position: fixed; inset: 0; z-index: 10; display: grid; place-items: center; color: var(--cream); background: radial-gradient(70% 50% at 50% 60%, rgba(255,138,67,.14), transparent 70%), linear-gradient(180deg, #07131B 0%, #0B1B24 60%, #061016 100%); text-align: center; padding: 24px; box-sizing: border-box; transition: opacity .4s ease; }}
    #splash.hide {{ opacity: 0; pointer-events: none; }}
    #splash .box {{ display: grid; gap: 14px; justify-items: center; max-width: 440px; width: 100%; }}
    #splash .logo {{ width: min(280px, 70vw); height: auto; filter: drop-shadow(0 16px 30px rgba(0,0,0,.55)); }}
    #splash .logo-text {{ font-family: "Fraunces", Georgia, serif; font-size: clamp(34px, 7vw, 48px); font-weight: 600; letter-spacing: -0.01em; line-height: 1.05; }}
    #splash .tag {{ font-size: 15px; line-height: 1.5; color: var(--muted); margin: 0; max-width: 40ch; }}
    #splash .hint {{ font-size: 13px; color: #8CA1AA; margin: 0; }}
    #splash .bar {{ width: min(320px, 80vw); height: 6px; border-radius: 999px; background: rgba(255,255,255,.1); overflow: hidden; margin-top: 6px; }}
    #splash .bar i {{ display: block; height: 100%; width: 0%; background: linear-gradient(90deg, #FFAD65, var(--amber)); border-radius: 999px; transition: width .2s ease; box-shadow: 0 0 12px rgba(255,138,67,.6); }}
    #splash .st {{ font-size: 12px; color: #8CA1AA; letter-spacing: .12em; text-transform: uppercase; font-weight: 600; }}
    #splash .by {{ display: inline-flex; align-items: center; gap: 8px; margin-top: 14px; color: var(--muted); font-size: 13px; text-decoration: none; }}
    #splash .by svg {{ width: 16px; height: 22px; }} #splash .by b {{ font-family: "Fraunces", Georgia, serif; font-weight: 600; color: var(--cream); font-size: 15px; }}
    [data-l]:not([data-l-active]) {{ display: none; }}
    @media (prefers-reduced-motion: reduce) {{ #splash .bar i {{ transition: none; }} }}
  </style>
</head>
<body>
  <div id="fw-bar">
    <a class="brand" href="../../" title="Firewisp Studio">{FLAME}<b>Firewisp</b><span data-l="en">← back</span><span data-l="pl">← wróć</span></a>
    <span class="title">{T}</span>
    <button class="fs" type="button" id="fw-fs"><svg class="ico" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 8V3h5M12 3h5v5M17 12v5h-5M8 17H3v-5"/></svg><span data-l="en">Full screen</span><span data-l="pl">Pełny ekran</span></button>
    <button type="button" id="fw-hide" aria-label="Hide bar"><svg class="ico" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5-5 5 5"/></svg></button>
  </div>
  <button id="fw-tab" type="button" aria-label="Show bar"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4l-6 6 6 6"/></svg></button>
  <div id="game"></div>
  <div id="splash" role="status" aria-live="polite">
    <div class="box">
      {logo_html}
      <p class="tag" data-l="en">{html.escape(a.tagline_en)}</p>
      <p class="tag" data-l="pl">{html.escape(a.tagline_pl)}</p>
      {rot}
      <div class="bar"><i id="bar"></i></div>
      <div class="st" id="st">…</div>
      <a class="by" href="../../">{FLAME}<b>Firewisp</b> Studio</a>
    </div>
  </div>
  <script>
    (function () {{
      var pl = (navigator.language || '').toLowerCase().indexOf('pl') === 0;
      try {{ var s = localStorage.getItem('fw-lang'); if (s) pl = (s === 'pl'); }} catch (e) {{}}
      document.querySelectorAll('[data-l]').forEach(function (el) {{ el.toggleAttribute('data-l-active', el.dataset.l === (pl ? 'pl' : 'en')); }});
      // pasek: schowany na niskich ekranach (telefon poziomo), wybór użytkownika pamiętany
      var pref = null; try {{ pref = localStorage.getItem('fw-bar'); }} catch (e) {{}}
      var hidden = pref ? pref === 'hidden' : (window.innerHeight < 500);
      var setBar = function (h) {{ document.body.classList.toggle('bar-hidden', h); try {{ localStorage.setItem('fw-bar', h ? 'hidden' : 'shown'); }} catch (e) {{}} }};
      document.body.classList.toggle('bar-hidden', hidden);
      document.getElementById('fw-hide').addEventListener('click', function () {{ setBar(true); }});
      document.getElementById('fw-tab').addEventListener('click', function () {{ setBar(false); }});
      if (document.documentElement.requestFullscreen) {{
        document.documentElement.classList.add('has-fs');
        document.getElementById('fw-fs').addEventListener('click', function () {{ if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen().catch(function () {{}}); }});
      }}
      window.__fwSplash = {{
        pl: pl,
        bar: document.getElementById('bar'), st: document.getElementById('st'),
        set: function (frac, en, plt) {{ this.bar.style.width = Math.round(frac * 100) + '%'; this.st.textContent = this.pl ? plt : en; }},
        hide: function () {{ var s = document.getElementById('splash'); if (!s) return; s.classList.add('hide'); setTimeout(function () {{ s.remove(); }}, 450); }}
      }};
      window.__fwSplash.set(0.02, 'Downloading', 'Pobieranie');
    }})();
  </script>
  <script src="flutter_bootstrap.js" async></script>
</body>
</html>
'''
(web / 'index.html').write_text(index)

bootstrap = '''{{flutter_js}}
{{flutter_build_config}}

// Rozgrzewamy cache realnym pobieraniem (pasek postępu), potem standardowy loader Fluttera bierze te same pliki.
// CanvasKit z własnego hostingu; wariant „chromium” tam, gdzie Flutter sam go wybierze (ten sam test co w loaderze),
// żeby nie pobierać wasm dwa razy. Gra renderuje się w #game (pod paskiem studia).
(async function () {
  const S = window.__fwSplash;
  async function fetchProgress(url, from, to) {
    try {
      const r = await fetch(url, { cache: 'force-cache' });
      const total = +r.headers.get('content-length') || 0;
      if (!r.body || !total) { await r.arrayBuffer(); S.set(to, 'Downloading', 'Pobieranie'); return; }
      const reader = r.body.getReader(); let got = 0;
      while (true) { const { done, value } = await reader.read(); if (done) break; got += value.length; S.set(from + (to - from) * (got / total), 'Downloading', 'Pobieranie'); }
    } catch (e) { S.set(to, 'Downloading', 'Pobieranie'); }
  }
  const chromium = typeof ImageDecoder !== 'undefined' && typeof Intl.v8BreakIterator !== 'undefined' && typeof Intl.Segmenter !== 'undefined'
    && (navigator.vendor === 'Google Inc.' || navigator.userAgent.includes('Edg/'));
  await fetchProgress('main.dart.js', 0.02, 0.45);
  await fetchProgress(chromium ? 'canvaskit/chromium/canvaskit.wasm' : 'canvaskit/canvaskit.wasm', 0.45, 0.9);
  S.set(0.92, 'Starting', 'Uruchamianie');
  _flutter.loader.load({
    config: { canvasKitBaseUrl: 'canvaskit/' },
    onEntrypointLoaded: async function (engineInitializer) {
      const appRunner = await engineInitializer.initializeEngine({ hostElement: document.getElementById('game') });
      S.set(1, 'Ready', 'Gotowe');
      await appRunner.runApp();
      setTimeout(function () { S.hide(); }, 250);
    }
  });
})();
'''
(web / 'flutter_bootstrap.js').write_text(bootstrap)
print('splash v3 written:', web)
