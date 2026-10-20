#!/usr/bin/env python3
"""Ekran ładowania dla gier Fluttera w przeglądarce (play/<gra>/).

  flutter_splash.py <katalog_projektu> --title ... --tagline-en ... --tagline-pl ... --logo <ścieżka w assets> --bg #hex [--landscape]

Nadpisuje web/index.html i web/flutter_bootstrap.js. Pasek postępu liczy realne pobieranie
main.dart.js i canvaskit.wasm (fetch do cache), potem oddaje głos loaderowi Fluttera.
CanvasKit serwujemy z własnego hostingu (bez CDN Google).
"""
import argparse, pathlib

ap = argparse.ArgumentParser()
ap.add_argument('dir'); ap.add_argument('--title', required=True)
ap.add_argument('--tagline-en', required=True); ap.add_argument('--tagline-pl', required=True)
ap.add_argument('--logo', default=''); ap.add_argument('--bg', default='#0b0c10'); ap.add_argument('--accent', default='#f3a35a')
ap.add_argument('--landscape', action='store_true'); ap.add_argument('--description', default='')
a = ap.parse_args()
web = pathlib.Path(a.dir) / 'web'
logo_html = f'<img class="logo" src="{a.logo}" alt="">' if a.logo else f'<div class="logo-text">{a.title}</div>'
rot = ('<p class="hint" data-l="en">Best played with the phone turned sideways.</p>'
       '<p class="hint" data-l="pl">Najlepiej gra się z telefonem obróconym bokiem.</p>') if a.landscape else ''
index = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <base href="$FLUTTER_BASE_HREF">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">
  <meta name="description" content="{a.description or a.tagline_en}">
  <meta name="theme-color" content="{a.bg}">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black">
  <meta name="apple-mobile-web-app-title" content="{a.title}">
  <link rel="apple-touch-icon" href="icons/Icon-192.png">
  <link rel="icon" type="image/png" href="favicon.png"/>
  <title>{a.title}</title>
  <link rel="manifest" href="manifest.json">
  <style>
    html, body {{ margin: 0; height: 100%; background: {a.bg}; }}
    #splash {{ position: fixed; inset: 0; display: grid; place-items: center; background: {a.bg}; color: #ebe7df; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; z-index: 10; transition: opacity .35s ease; padding: 24px; box-sizing: border-box; text-align: center; }}
    #splash.hide {{ opacity: 0; pointer-events: none; }}
    #splash .box {{ display: grid; gap: 14px; justify-items: center; max-width: 420px; width: 100%; }}
    #splash .logo {{ width: min(260px, 70vw); height: auto; filter: drop-shadow(0 12px 24px rgba(0,0,0,.5)); }}
    #splash .logo-text {{ font-size: 32px; font-weight: 800; letter-spacing: -0.02em; }}
    #splash .tag {{ font-size: 16px; line-height: 1.45; color: #c9c4ba; margin: 0; }}
    #splash .hint {{ font-size: 13px; color: #8d8980; margin: 0; }}
    #splash .bar {{ width: min(320px, 80vw); height: 6px; border-radius: 999px; background: rgba(255,255,255,.12); overflow: hidden; }}
    #splash .bar i {{ display: block; height: 100%; width: 0%; background: {a.accent}; border-radius: 999px; transition: width .2s ease; }}
    #splash .st {{ font-size: 12px; color: #8d8980; letter-spacing: .06em; text-transform: uppercase; }}
    #splash .by {{ font-size: 12px; color: #6f6c66; margin-top: 10px; }}
    #splash .by a {{ color: #a8a39a; text-decoration: none; }}
    [data-l]:not([data-l-active]) {{ display: none; }}
  </style>
</head>
<body>
  <div id="splash" role="status" aria-live="polite">
    <div class="box">
      {logo_html}
      <p class="tag" data-l="en">{a.tagline_en}</p>
      <p class="tag" data-l="pl">{a.tagline_pl}</p>
      {rot}
      <div class="bar"><i id="bar"></i></div>
      <div class="st" id="st">…</div>
      <div class="by"><a href="../../">Firewisp Studio</a></div>
    </div>
  </div>
  <script>
    (function () {{
      var pl = (navigator.language || '').toLowerCase().indexOf('pl') === 0;
      try {{ var s = localStorage.getItem('fw-lang'); if (s) pl = (s === 'pl'); }} catch (e) {{}}
      document.querySelectorAll('[data-l]').forEach(function (el) {{ el.toggleAttribute('data-l-active', el.dataset.l === (pl ? 'pl' : 'en')); }});
      window.__fwSplash = {{
        pl: pl,
        bar: document.getElementById('bar'), st: document.getElementById('st'),
        set: function (frac, en, plt) {{ this.bar.style.width = Math.round(frac * 100) + '%'; this.st.textContent = this.pl ? plt : en; }},
        hide: function () {{ var s = document.getElementById('splash'); s.classList.add('hide'); setTimeout(function () {{ s.remove(); }}, 400); }}
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

// Rozgrzewamy cache realnym pobieraniem (pasek postępu), potem standardowy loader Fluttera
// bierze te same pliki z cache. CanvasKit z własnego hostingu — bez CDN Google.
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
  await fetchProgress('main.dart.js', 0.02, 0.45);
  await fetchProgress('canvaskit/canvaskit.wasm', 0.45, 0.9);
  S.set(0.92, 'Starting', 'Uruchamianie');
  _flutter.loader.load({
    config: { canvasKitBaseUrl: 'canvaskit/' },
    onEntrypointLoaded: async function (engineInitializer) {
      const appRunner = await engineInitializer.initializeEngine();
      S.set(1, 'Ready', 'Gotowe');
      await appRunner.runApp();
      setTimeout(function () { S.hide(); }, 250);
    }
  });
})();
'''
(web / 'flutter_bootstrap.js').write_text(bootstrap)
print('splash written:', web)
