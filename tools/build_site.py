#!/usr/bin/env python3
"""Generator strony Firewisp Studio (statyczny, bez zależności poza PIL).

Źródła:  src/index.html (dwujęzyczny master z data-l), src/privacy.html, src/products.json, assets/
Wyniki:  index.html (EN) · pl/index.html (PL) · <slug>/index.html · pl/<slug>/index.html
         privacy/index.html · pl/prywatnosc/index.html · 404.html · sitemap.xml · robots.txt
         assets/og/<slug>.jpg (obrazki OG) · press/<slug>-press-kit.zip

Jedna stała SITE_URL — po zakupie domeny zmienić tylko ją i uruchomić ponownie.
Uruchomienie: python3 tools/build_site.py   (z katalogu repo)
"""
from __future__ import annotations
import json, os, re, io, zipfile, html as H
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = 'https://tomaszmatusiak-stack.github.io/firewisp-studio'
LANGS = ('en', 'pl')
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr', 'use', 'path', 'circle', 'stop', 'rect'}

# ───────────────────────── usuwanie drugiego języka ─────────────────────────
class _Stripper(HTMLParser):
    """Zbiera zakresy [start, end) elementów z data-l != lang (z zagnieżdżeniem)."""
    def __init__(self, raw: str, lang: str):
        super().__init__(convert_charrefs=False)
        self.raw, self.lang = raw, lang
        self.lines = [0]
        for i, ch in enumerate(raw):
            if ch == '\n': self.lines.append(i + 1)
        self.ranges: list[tuple[int, int]] = []
        self.skip_start: int | None = None
        self.depth = 0
    def off(self) -> int:
        l, c = self.getpos(); return self.lines[l - 1] + c
    def handle_starttag(self, tag, attrs):
        if self.skip_start is not None:
            if tag not in VOID: self.depth += 1
            return
        a = dict(attrs)
        if 'data-l' in a and a['data-l'] != self.lang and tag not in VOID:
            self.skip_start = self.off(); self.depth = 1
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if self.skip_start is None: return
        self.depth -= 1
        if self.depth == 0:
            end = self.raw.index('>', self.off()) + 1
            self.ranges.append((self.skip_start, end)); self.skip_start = None

def strip_lang(raw: str, lang: str) -> str:
    p = _Stripper(raw, lang); p.feed(raw); p.close()
    out, pos = [], 0
    for s, e in p.ranges:
        out.append(raw[pos:s]); pos = e
    out.append(raw[pos:])
    s = ''.join(out)
    s = re.sub(r' data-l="(en|pl)"', '', s)
    s = re.sub(r'\n[ \t]*\n[ \t]*\n', '\n\n', s)
    return s

# ───────────────────────── ścieżki względne ─────────────────────────
ATTR_RE = re.compile(r'\b(href|src|poster|imagesrcset|srcset)="([^"]*)"')
def _is_rel(u: str) -> bool:
    return not (u.startswith(('http://', 'https://', '#', 'mailto:', 'data:', '/', '../', '//')) or u == '')
def rebase(doc: str, prefix: str) -> str:
    def one(m):
        attr, val = m.group(1), m.group(2)
        if attr in ('imagesrcset', 'srcset'):
            parts = []
            for cand in val.split(','):
                cand = cand.strip(); url, _, desc = cand.partition(' ')
                parts.append((prefix + url if _is_rel(url) else url) + ((' ' + desc) if desc else ''))
            return f'{attr}="{", ".join(parts)}"'
        return f'{attr}="{prefix + val if _is_rel(val) else val}"'
    return ATTR_RE.sub(one, doc)

# ───────────────────────── nagłówek SEO ─────────────────────────
def seo_head(path_en: str, path_pl: str, lang: str, title: str, desc: str, og_image: str, og_type='website') -> str:
    me = path_en if lang == 'en' else path_pl
    return '\n'.join([
        f'<link rel="canonical" href="{SITE_URL}/{me}">',
        f'<link rel="alternate" hreflang="en" href="{SITE_URL}/{path_en}">',
        f'<link rel="alternate" hreflang="pl" href="{SITE_URL}/{path_pl}">',
        f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{path_en}">',
        f'<meta property="og:type" content="{og_type}">',
        '<meta property="og:site_name" content="Firewisp Studio">',
        f'<meta property="og:title" content="{H.escape(title)}">',
        f'<meta property="og:description" content="{H.escape(desc)}">',
        f'<meta property="og:url" content="{SITE_URL}/{me}">',
        f'<meta property="og:image" content="{SITE_URL}/{og_image}">',
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        f'<meta property="og:locale" content="{"en_US" if lang == "en" else "pl_PL"}"><meta property="og:locale:alternate" content="{"pl_PL" if lang == "en" else "en_US"}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{H.escape(title)}">',
        f'<meta name="twitter:description" content="{H.escape(desc)}">',
        f'<meta name="twitter:image" content="{SITE_URL}/{og_image}">',
    ])

def lang_switch(lang: str, other_url: str) -> str:
    """Przełącznik EN/PL jako linki (osobne adresy); wybór zapisywany w localStorage dla gier."""
    en = '<a href="%s" lang="en" aria-current="%s" data-set-lang="en">EN</a>' % (other_url if lang == 'pl' else '#', 'page' if lang == 'en' else 'false')
    pl = '<a href="%s" lang="pl" aria-current="%s" data-set-lang="pl">PL</a>' % (other_url if lang == 'en' else '#', 'page' if lang == 'pl' else 'false')
    return f'<div class="lang" role="group" aria-label="Language / Język">{en}<span class="sep" aria-hidden="true">/</span>{pl}</div>'

LANG_JS = '''<script>
  // język strony = adres (/ = EN, /pl/ = PL); wybór zapisany dla gier; na "/" pierwsza wizyta z polską przeglądarką idzie do /pl/
  (function(){ var L=document.documentElement.lang; try{ localStorage.setItem('fw-lang', L); }catch(e){}
    document.querySelectorAll('[data-set-lang]').forEach(function(a){ a.addEventListener('click', function(){ try{ localStorage.setItem('fw-lang', a.dataset.setLang); sessionStorage.setItem('fw-lang-chosen','1'); }catch(e){} }); });
  })();
</script>'''
REDIRECT_JS = '''<script>
  (function(){ try{ if (location.search.indexOf('lang=')>=0 || sessionStorage.getItem('fw-lang-chosen')) return; var s=localStorage.getItem('fw-lang'); var pl = s ? s==='pl' : (navigator.language||'').toLowerCase().indexOf('pl')===0; if (pl) location.replace('pl/' + location.hash); }catch(e){} })();
</script>'''
# Analityka bez cookies: GoatCounter (konto Tomasza, nazwa 'firewisp'); count.js pomija localhost. Zmiana nazwy = tylko tutaj.
GOATCOUNTER = 'https://firewisp.goatcounter.com/count'
ANALYTICS_JS = f'<script data-goatcounter="{GOATCOUNTER}" async src="https://gc.zgo.at/count.js"></script>'
HEAD_LANG_JS = '''<script>try{{localStorage.setItem('fw-lang','{lang}');}}catch(e){{}}</script>'''

# ───────────────────────── strona główna ─────────────────────────
def build_index(master: str):
    for lang in LANGS:
        doc = strip_lang(master, lang)
        depth = 0 if lang == 'en' else 1
        prefix = '../' * depth
        doc = rebase(doc, prefix)
        doc = doc.replace('<html lang="en">', f'<html lang="{lang}">')
        title = 'Firewisp Studio' if lang == 'en' else 'Firewisp Studio'
        desc = ('Firewisp Studio — small games and useful apps, independently crafted in Poland. Play Sushi Rush and Bog Night free in your browser; Kropla on the App Store.' if lang == 'en'
                else 'Firewisp Studio — małe gry i przydatne aplikacje, tworzone niezależnie w Polsce. Zagraj w Sushi Rush i Bog Night w przeglądarce; Kropla w App Store.')
        # stare meta OG/twitter/description z mastera → nowe
        doc = re.sub(r'<meta name="description"[^>]*>\n', '', doc)
        doc = re.sub(r'<meta (property="og:[^"]*"|name="twitter:[^"]*")[^>]*>(<meta property="og:image:height"[^>]*>)?\n?', '', doc)
        head = f'<meta name="description" content="{H.escape(desc)}">\n' + seo_head('', 'pl/', lang, 'Firewisp Studio — Small games. Big personality.' if lang == 'en' else 'Firewisp Studio — Małe gry. Dużo charakteru.', desc, 'assets/og.jpg')
        doc = doc.replace('<meta name="theme-color"', head + '\n<meta name="theme-color"', 1)
        # przełącznik języka → linki
        doc = re.sub(r'<div class="lang" role="group"[^>]*>.*?</div>', lang_switch(lang, '../' if lang == 'pl' else 'pl/'), doc, count=1, flags=re.S)
        # stary skrypt języka (setLang/DESC) zostaje nieszkodliwy; dokładamy nasz
        doc = doc.replace('<head>', '<head>\n' + ((REDIRECT_JS + '\n') if lang == 'en' else '') + HEAD_LANG_JS.format(lang=lang), 1)
        doc = doc.replace('</head>', ANALYTICS_JS + '\n</head>', 1)
        doc = doc.replace('</body>', LANG_JS + '\n</body>')
        # nawigacja: Prywatność → nowe adresy
        doc = doc.replace(f'href="{prefix}privacy.html"', f'href="{prefix}privacy/"' if lang == 'en' else 'href="prywatnosc/"')
        out = ROOT / ('index.html' if lang == 'en' else 'pl/index.html')
        out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc, encoding='utf-8')
        print('index', lang, out.relative_to(ROOT))

# ───────────────────────── prywatność ─────────────────────────
def build_privacy(master: str):
    for lang in LANGS:
        doc = strip_lang(master, lang)
        path_en, path_pl = 'privacy/', 'pl/prywatnosc/'
        depth = 1 if lang == 'en' else 2
        prefix = '../' * depth
        doc = rebase(doc, prefix)
        doc = doc.replace('<html lang="en">', f'<html lang="{lang}">')
        title = 'Privacy — Firewisp Studio' if lang == 'en' else 'Prywatność — Firewisp Studio'
        desc = 'Privacy notice for the Firewisp Studio website and beta list.' if lang == 'en' else 'Informacja o prywatności strony Firewisp Studio i listy beta.'
        doc = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', doc)
        doc = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{H.escape(desc)}">', doc)
        doc = doc.replace('<meta name="theme-color"', seo_head(path_en, path_pl, lang, title, desc, 'assets/og.jpg') + '\n<meta name="theme-color"', 1)
        doc = re.sub(r'<div class="lang" role="group"[^>]*>.*?</div>', lang_switch(lang, '../pl/prywatnosc/' if lang == 'en' else '../../privacy/'), doc, count=1, flags=re.S)
        # linki do strony głównej z poziomu języka
        home = prefix if lang == 'en' else '../'
        doc = doc.replace(f'href="{prefix}./"', f'href="{home}"').replace(f'href="{prefix}./#', f'href="{home}#')
        doc = doc.replace('<head>', '<head>\n' + HEAD_LANG_JS.format(lang=lang), 1)
        doc = doc.replace('</head>', ANALYTICS_JS + '\n</head>', 1)
        doc = doc.replace('</body>', LANG_JS + '\n</body>')
        out = ROOT / (path_en if lang == 'en' else path_pl) / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc, encoding='utf-8')
        print('privacy', lang)
    (ROOT / 'privacy.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=privacy/"><link rel="canonical" href="%s/privacy/"><title>Privacy — Firewisp Studio</title><a href="privacy/">Privacy</a>' % SITE_URL, encoding='utf-8')

# ───────────────────────── strony produktów ─────────────────────────
def t(d: dict, lang: str) -> str:
    v = d.get(lang) if isinstance(d, dict) else d
    return v if v is not None else d.get('en', '')

def product_html(p: dict, lang: str, products: list[dict]) -> str:
    depth = 1 if lang == 'en' else 2
    pre = '../' * depth
    home = pre if lang == 'en' else '../'          # strona główna w tym języku
    other = f'../pl/{p["slug"]}/' if lang == 'en' else f'../../{p["slug"]}/'
    path_en, path_pl = f'{p["slug"]}/', f'pl/{p["slug"]}/'
    L = lambda k: t(p[k], lang) if k in p else ''
    name = p['name']; title = f'{name} — Firewisp Studio'
    desc = L('tagline')
    tags = ''.join(f'<span class="tag {c}">{t(txt, lang)}</span>' for c, txt in p['status'])
    shots = ''.join(f'<figure class="shot"><img src="{pre}{s["src"]}" width="{s["w"]}" height="{s["h"]}" alt="{H.escape(t(s["alt"], lang))}" loading="lazy" decoding="async"></figure>' for s in p['shots'])
    feats = ''.join(f'<li><strong>{t(f["t"], lang)}</strong><span>{t(f["d"], lang)}</span></li>' for f in p['features'])
    facts = ''.join(f'<div class="fact"><dt>{t(f["k"], lang)}</dt><dd>{t(f["v"], lang)}</dd></div>' for f in p['facts'])
    ctas = []
    for c in p['cta']:
        href = c['href']
        if href.startswith('play/') or href.startswith('assets/'): href = pre + href
        elif href == '#beta': href = home + '#beta'
        cls = 'btn btn-primary' if c.get('primary') else 'btn'
        ctas.append(f'<a class="{cls}" href="{href}">{t(c["label"], lang)} <svg class="ico arrow"><use href="#i-arrow"/></svg></a>')
    cta_html = ''.join(ctas)
    beta_note = L('beta_note')
    policy = p.get('privacy')
    policy_html = (f'<a class="link" href="{policy}">{"Privacy policy of the app" if lang == "en" else "Polityka prywatności aplikacji"}</a>' if policy
                   else f'<a class="link" href="{home}{"privacy/" if lang == "en" else "prywatnosc/"}">{"Privacy (browser version)" if lang == "en" else "Prywatność (wersja w przeglądarce)"}</a>')
    press_zip = f'{pre}press/{p["slug"]}-press-kit.zip'
    others = [q for q in products if q['slug'] != p['slug']]
    other_cards = ''.join(f'<a class="mini" href="{home}{q["slug"]}/" style="--c: {q["color"]}"><img src="{pre}{q["icon"]}" width="44" height="44" alt=""><span><b>{q["name"]}</b><small>{t(q["kind"], lang)}</small></span></a>' for q in others)
    nav = {'en': ('Games', 'Apps', 'About', 'Beta'), 'pl': ('Gry', 'Aplikacje', 'O studiu', 'Beta')}[lang]
    labels = {'en': ('Screens', 'What you do', 'Facts', 'Press kit', 'Icon, screenshots and a short description, in one zip.', 'Download', 'More from the studio', 'Join the beta', '← Firewisp Studio', 'Skip to content'),
              'pl': ('Ekrany', 'Co tu robisz', 'Fakty', 'Materiały prasowe', 'Ikona, zrzuty i krótki opis w jednym zipie.', 'Pobierz', 'Więcej ze studia', 'Zapisz się na betę', '← Firewisp Studio', 'Przejdź do treści')}[lang]
    hero_art = f'<img src="{pre}{p["hero"]}" width="{p["hero_w"]}" height="{p["hero_h"]}" alt="" fetchpriority="high" decoding="async">'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
{HEAD_LANG_JS.format(lang=lang)}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
{seo_head(path_en, path_pl, lang, title, desc, f'assets/og/{p["slug"]}.jpg')}
<meta name="theme-color" content="#07131B">
<link rel="icon" href="{pre}{p["icon"]}" type="image/webp">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="preload" href="{pre}assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{pre}assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/site.css">
<link rel="stylesheet" href="{pre}assets/product.css">
{ANALYTICS_JS}
</head>
<body class="product" style="--c: {p["color"]}">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="i-arrow" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 10h12M11 5l5 5-5 5"/></symbol><symbol id="i-down" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 3v11M5 9l5 5 5-5M4 17h12"/></symbol></svg>
<a class="skip" href="#main">{labels[9]}</a>
<header class="site-header">
  <div class="container header-row">
    <a class="brand" href="{home}" aria-label="Firewisp Studio"><img src="{pre}assets/icon-firewisp.webp" alt="" width="30" height="30"><span>Firewisp <i>Studio</i></span></a>
    <nav class="nav" id="nav" aria-label="Main">
      <a href="{home}#games">{nav[0]}</a><a href="{home}#games">{nav[1]}</a><a href="{home}#about">{nav[2]}</a><a href="{home}#beta">{nav[3]}</a>
    </nav>
    <div class="header-actions">{lang_switch(lang, other)}<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav"><span class="sr-only">Menu</span><svg class="bars" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M3 6h14M3 10h14M3 14h14"/></svg><svg class="x" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M5 5l10 10M15 5L5 15"/></svg></button></div>
  </div>
</header>
<main id="main">
  <section class="p-hero container">
    <div class="p-copy">
      <a class="crumb" href="{home}">{labels[8]}</a>
      <div class="status">{tags}</div>
      <h1>{H.escape(name)}</h1>
      <p class="lead">{L('tagline')}</p>
      <p class="desc">{L('intro')}</p>
      <div class="cta">{cta_html}</div>
      {f'<p class="meta-note">{beta_note}</p>' if beta_note else ''}
    </div>
    <div class="p-art">{hero_art}</div>
  </section>
  <section class="section container">
    <div class="section-head"><div class="title"><h2>{labels[0]}</h2></div></div>
    <div class="shots {'shots-wide' if p.get('landscape') else ''}">{shots}</div>
  </section>
  <section class="section container p-grid">
    <div>
      <div class="section-head"><div class="title"><h2>{labels[1]}</h2></div></div>
      <ul class="feats">{feats}</ul>
    </div>
    <aside>
      <div class="section-head"><div class="title"><h2>{labels[2]}</h2></div></div>
      <dl class="facts">{facts}</dl>
      <p class="meta-note">{policy_html}</p>
      <div class="press">
        <h3>{labels[3]}</h3>
        <p class="desc">{labels[4]}</p>
        <a class="btn btn-sm" href="{press_zip}" download><svg class="ico"><use href="#i-down"/></svg> {labels[5]} (zip)</a>
      </div>
    </aside>
  </section>
  <section class="section container">
    <div class="section-head"><div class="title"><h2>{labels[6]}</h2></div><a class="view-all" href="{home}#beta">{labels[7]} <svg class="ico"><use href="#i-arrow"/></svg></a></div>
    <div class="minis">{other_cards}</div>
  </section>
</main>
<footer class="site-footer">
  <div class="container footer-bottom" style="margin-top:0;border-top:0;padding-top:0">
    <span>© 2026 Firewisp Studio · Tomasz Matusiak</span>
    <span><a href="{home}">{labels[8]}</a> · <a href="{home}{'privacy/' if lang == 'en' else 'prywatnosc/'}">{'Privacy' if lang == 'en' else 'Prywatność'}</a> · <a href="mailto:tomasz.matusiak@post.pl">tomasz.matusiak@post.pl</a></span>
  </div>
</footer>
{LANG_JS}
<script>
  const menuBtn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  menuBtn.addEventListener('click', () => {{ const open = nav.classList.toggle('open'); menuBtn.setAttribute('aria-expanded', String(open)); }});
  const header = document.querySelector('.site-header'); const onScroll = () => header.classList.toggle('scrolled', scrollY > 8); addEventListener('scroll', onScroll, {{ passive: true }}); onScroll();
</script>
</body>
</html>
'''

def build_products(products: list[dict]):
    for p in products:
        for lang in LANGS:
            out = ROOT / (f'{p["slug"]}/index.html' if lang == 'en' else f'pl/{p["slug"]}/index.html')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(product_html(p, lang, products), encoding='utf-8')
        print('product', p['slug'])

# ───────────────────────── OG, press kit, sitemap, 404 ─────────────────────────
def build_og(products: list[dict]):
    from PIL import Image, ImageDraw, ImageFont
    (ROOT / 'assets/og').mkdir(parents=True, exist_ok=True)
    try:
        f_title = ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf', 74)
        f_small = ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf', 30)
        f_tag = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 26)
    except Exception:
        f_title = f_small = f_tag = ImageFont.load_default()
    for p in products:
        im = Image.new('RGB', (1200, 630)); d = ImageDraw.Draw(im)
        for y in range(630):
            k = y / 629; d.line([(0, y), (1200, y)], fill=(int(7 + 4 * k), int(19 + 8 * k), int(27 + 9 * k)))
        art = Image.open(ROOT / p['og_art']).convert('RGBA')
        ah = 520; art = art.resize((round(art.width * ah / art.height), ah), Image.LANCZOS)
        if art.width > 560: art = art.crop(((art.width - 560) // 2, 0, (art.width - 560) // 2 + 560, ah))
        mask = Image.new('L', art.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, art.width - 1, art.height - 1), 36, fill=255)
        im.paste(art, (1200 - art.width - 60, 55), mask)
        # tytuł: łamanie do szerokości 560 px, mniejszy font dla długich nazw
        name = p['name']; ft = f_title
        if d.textlength(name, font=ft) > 560:
            try: ft = ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf', 58)
            except Exception: pass
        tl, cur = [], ''
        for w in name.split():
            cand = (cur + ' ' + w).strip()
            if d.textlength(cand, font=ft) > 560 and cur: tl.append(cur); cur = w
            else: cur = cand
        if cur: tl.append(cur)
        ty = 150 - (len(tl) - 1) * 34
        for i, ln in enumerate(tl[:2]): d.text((70, ty + i * (ft.size + 8)), ln, font=ft, fill=(245, 241, 233))
        tag_y = ty + len(tl[:2]) * (ft.size + 8) + 24
        tag = t(p['tagline'], 'en')
        # zawijanie tagline do ~26 znaków/linia
        words, lines, cur = tag.split(), [], ''
        for w in words:
            if len(cur) + len(w) + 1 > 30 and cur: lines.append(cur); cur = w
            else: cur = (cur + ' ' + w).strip()
        if cur: lines.append(cur)
        for i, ln in enumerate(lines[:3]): d.text((70, tag_y + i * 40), ln, font=f_small, fill=(170, 188, 197))
        d.text((70, 540), 'FIREWISP STUDIO', font=f_tag, fill=(255, 173, 101))
        im.save(ROOT / 'assets/og' / f'{p["slug"]}.jpg', 'JPEG', quality=86, optimize=True)
    print('og images', len(products))

def build_press(products: list[dict]):
    (ROOT / 'press').mkdir(exist_ok=True)
    for p in products:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(ROOT / p['icon'], f'{p["slug"]}/icon.webp')
            for i, s in enumerate(p['shots'], 1): z.write(ROOT / s['src'], f'{p["slug"]}/screenshot-{i}.webp')
            z.write(ROOT / p['hero'], f'{p["slug"]}/key-art.webp')
            txt = (f'{p["name"]} — Firewisp Studio\n\nEN: {t(p["tagline"], "en")}\n{t(p["intro"], "en")}\n\nPL: {t(p["tagline"], "pl")}\n{t(p["intro"], "pl")}\n\n'
                   f'Page: {SITE_URL}/{p["slug"]}/\nContact: tomasz.matusiak@post.pl\n')
            z.writestr(f'{p["slug"]}/README.txt', txt)
        (ROOT / 'press' / f'{p["slug"]}-press-kit.zip').write_bytes(buf.getvalue())
    print('press kits', len(products))

def build_sitemap(products: list[dict]):
    urls = ['', 'pl/', 'privacy/', 'pl/prywatnosc/'] + [f'{p["slug"]}/' for p in products] + [f'pl/{p["slug"]}/' for p in products] + ['play/sushi-rush/', 'play/bog-night/', 'play/turniej/', 'play/pendulum/']
    today = __import__('datetime').date.today().isoformat()
    body = '\n'.join(f'  <url><loc>{SITE_URL}/{u}</loc><lastmod>{today}</lastmod></url>' for u in urls)
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n', encoding='utf-8')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /src/\nDisallow: /tools/\nSitemap: {SITE_URL}/sitemap.xml\n', encoding='utf-8')
    print('sitemap', len(urls), 'urls')

def build_404():
    doc = f'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Not found — Firewisp Studio</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="/firewisp-studio/assets/site.css"><link rel="stylesheet" href="/firewisp-studio/assets/product.css">{ANALYTICS_JS}</head>
<body class="product">
<main id="main" class="container nf">
  <p class="meta" data-l="en">404</p><p class="meta" data-l="pl">404</p>
  <h1 data-l="en">That page wandered off into the bog.</h1><h1 data-l="pl">Ta strona odeszła w bagno.</h1>
  <p class="lead" data-l="en">The address doesn't exist, or the game moved. Try one of these.</p><p class="lead" data-l="pl">Taki adres nie istnieje albo gra się przeprowadziła. Spróbuj jednego z tych.</p>
  <div class="cta">
    <a class="btn btn-primary" href="/firewisp-studio/"><span data-l="en">Studio home</span><span data-l="pl">Strona studia</span></a>
    <a class="btn" href="/firewisp-studio/play/sushi-rush/">Sushi Rush</a><a class="btn" href="/firewisp-studio/play/bog-night/">Bog Night</a><a class="btn" href="/firewisp-studio/#beta">Beta</a>
  </div>
</main>
<script>var pl=(navigator.language||'').toLowerCase().indexOf('pl')===0;try{{var s=localStorage.getItem('fw-lang');if(s)pl=(s==='pl');}}catch(e){{}}document.documentElement.lang=pl?'pl':'en';document.querySelectorAll('[data-l]').forEach(function(el){{el.toggleAttribute('data-l-active',el.dataset.l===(pl?'pl':'en'));}});</script>
</body></html>'''
    (ROOT / '404.html').write_text(doc, encoding='utf-8'); print('404')

def main():
    products = json.loads((ROOT / 'src/products.json').read_text(encoding='utf-8'))
    build_index((ROOT / 'src/index.html').read_text(encoding='utf-8'))
    build_privacy((ROOT / 'src/privacy.html').read_text(encoding='utf-8'))
    build_products(products)
    build_og(products)
    build_press(products)
    build_sitemap(products)
    build_404()

if __name__ == '__main__':
    main()
