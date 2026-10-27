# Redesign v3 — „Cinematic Dark Indie” (gałąź `redesign-v3`, 2026-10-21)

Wykonanie promptu „Firewisp Studio — Complete Website Redesign” z mockupem. Strona główna przebudowana od zera (`index.html`, `assets/site.css`), `privacy.html` bez zmian poza wspólnym CSS, gry w `play/*` nietknięte.

## Co zostało zachowane
- Trasy do gier (`play/sushi-rush/`, `play/bog-night/`, `play/whirlpick/`, `play/turniej/`), link do Kropli w App Store, link do GitHuba, e-mail kontaktowy.
- Dwujęzyczność: ten sam mechanizm `data-l="en|pl"` + `localStorage` (`fw-lang`), domyślnie EN, PL z przeglądarki lub przełącznika.
- Formularz beta: ten sam endpoint Supabase (`beta_signups`, klucz publiczny tylko INSERT), pole-pułapka, walidacja, stany: wysyłanie / sukces / zły adres / błąd serwera / brak sieci, PL i EN. Dodany stan „Zapisuję…”.
- Meta SEO/OG, ikony, preload fontu, ścieżki względne pod `/firewisp-studio/`.
- Pętle wideo Sushi Rush i Bog Night (start w kadrze, pauza poza nim, poster przy reduced-motion).

## Decyzje, w których mockup odbiega od prawdy i co zrobiono zamiast
| Element mockupu | Dlaczego nie | Co jest |
|---|---|---|
| Kot-maskotka Sushi Rush, chłopiec w kapturze z latarnią | nie istnieją w grach | karty złożone z prawdziwych assetów: hostessa + logo + tło menu Sushi Rush; Kuba + logo + tło „długiej nocy” z Bog Night |
| „12K+ played · 98% positive”, „10K+ downloads · 4.9 rating” | brak takich danych | tagi kategorii zamiast liczb |
| paski postępu 40 % / 80 % / 30 % | brak danych o postępie | etykiety statusu: W recenzji / W budowie / Przeglądarka |
| hello@firewisp.studio, ikony Discord/X/Instagram/YouTube | nie istnieją | tomasz.matusiak@post.pl, GitHub |
| „Bog Night — a short, atmospheric adventure” | to lane defense, 36 nocy | opis zgodny z grą |
| „Whirlpick — in review” bez przeglądarki | wersja web istnieje | przycisk „Wypróbuj w przeglądarce” + tag „iPhone · w recenzji” |
| „Iskra — focus app, 30 %” | w budowie, bez daty | „W budowie”, maskotka = ikona apki |
| Fraunces | — | pobrana za zgodą Tomasza (21.10), self-hosted: `assets/fonts/fraunces-latin(.ext).woff2`, variable opsz/wght, 125 kB |

## Tło atmosferyczne
Hero: `assets/hero-bg.webp` (1920×1280, 117 kB) + wariant 1280 px — to scena menu Bog Night (noc nad bagnem, chata, latarnie, księżyc), własny asset studia, przyciemniony gradientami CSS. Dziewięć „ogników” to elementy `<i>` animowane CSS-em tylko w hero; `prefers-reduced-motion` je wyłącza. Reszta strony: gradienty granat → butelkowa zieleń, bez dużych ilustracji.

## Interakcje (wszystkie działają)
- Segmenty w hero (Wyróżnione / Do grania / W drodze): przewijają do sekcji, stan synchronizowany ze scroll-spy.
- Karuzela: strzałki, kropki, klik w boczną kartę, strzałki klawiatury (region z `tabindex`), Enter = otwórz aktywny produkt, przesunięcie palcem (pointer events).
- Filtry „Do grania teraz”: Wszystko / Gry / Aplikacje / Przeglądarka / Telefon; link „Aplikacje” w nawigacji ustawia filtr i przewija.
- Nawigacja: podkreślenie aktywnej sekcji (scroll-spy), menu mobilne, Escape zamyka.
- Hover kart: uniesienie, jaśniejsza krawędź, skala grafiki 1.03–1.04; przyciski: uniesienie 2 px + poświata.

## Nowe pliki w `assets/`
`hero-bg.webp`, `hero-bg-1280.webp`, `card-sushi.webp`, `card-bog.webp`, `card-kropla.webp`, `thumb-sushi-bg.webp`, `thumb-kropla.webp`, `thumb-pendulum.webp`, `thumb-whirlpick.webp` (razem ≈ 620 kB). Źródła: `mobile/sushi-rush/assets/{scene,ui}`, `play/bog-night/assets/build/{bg,characters,logo}`, zrzuty sklepowe Kropli, Pendulum i Whirlpick.

## Sprawdzone
Konsola bez błędów; 1440 / 1280 / 1024 / 375 px; brak przewijania poziomego na 375 px; strona prywatności działa z nowym CSS; filtr ukrywa karty; karuzela zmienia pozycje; PL/EN.

## v3.1 — poprawki UI (2026-10-21)
- Wspólna struktura kart (`.pcard`, `.ncard`): ciało = kolumna flex, `min-width: 0`, status w osobnym wierszu `.status` nad tytułem, CTA dociągnięte do dołu (`margin-top: auto`), równe wysokości w rzędzie z gridu.
- Plakietki `.tag`: stała wysokość 28 px, `white-space: nowrap`, `flex: none`, semantyka: `live` (zielony, dostępne), `review` (bursztyn, „Recenzja App Store”), `dev` (stonowany niebieski, w budowie), `soon` (neutralny).
- Pendulum: pełny tytuł, status „App Store review” + „iPhone” w osobnym wierszu. Whirlpick: opis zgodny z aplikacją (koło losowania), statusy „Przeglądarka” + „Recenzja App Store”, miniatura = całe koło z wskaźnikiem (kadr kwadratowy 800×800, kadruje się w pionie i poziomie).
- Mobile: wysokość karuzeli dopasowana do karty (bez pustki), mniejszy podpis karty, kropki karuzeli z polem dotyku 28 px, logo Sushi nie dotyka ramki telefonu, widoczny focus na chipach/segmentach/strzałkach.
- Sprawdzone w przeglądarce: 1600, 1440, 1280, 1024, 768, 390, 360 px — brak przewijania poziomego, karty w rzędzie równe (547 px / 451 px na desktopie), plakietki 28 px (boczne karty karuzeli są skalowane ×0,86, stąd 24–26 px), filtry i karuzela działają, konsola czysta. Formularz beta bez zmian w logice.

## v3.2 — podstrony, /pl/, SEO (2026-10-22)
- Generator `tools/build_site.py` (bez zależności poza PIL): master `src/index.html` i `src/privacy.html` (dwujęzyczne, `data-l`) → `index.html` (EN) i `pl/index.html` (PL) przez usunięcie elementów drugiego języka; `src/products.json` → `<slug>/` i `pl/<slug>/` dla 7 produktów; `privacy/` i `pl/prywatnosc/` (stary `privacy.html` = przekierowanie); `404.html`; `sitemap.xml` (23 adresy); `robots.txt`; `assets/og/<slug>.jpg`; `press/<slug>-press-kit.zip`.
- Każda strona: `canonical`, `hreflang` en/pl/x-default, OG/Twitter per strona, `lang` w HTML. Przełącznik EN/PL to linki między adresami; wybór zapisany w localStorage dla gier; na `/` pierwsza wizyta z polską przeglądarką idzie do `/pl/` (pomijane przy `?lang=` i po świadomym wyborze).
- Podstrony: hero z artem, statusy, CTA (graj / sklep / beta), zrzuty, „Co tu robisz”, fakty, link do polityki apki (repo legal) albo prywatności strony, press kit, inne produkty. Styl `assets/product.css`.
- `SITE_URL` w generatorze: po zakupie domeny zmienić i uruchomić ponownie.
- Braki: Turniej ma tylko ekran startowy (klik w kanwę Fluttera nie działa w panelu), Sushi Rush bez zrzutu „level complete”; zrzuty z telefonu uzupełnią.

## v3.3 — formularz beta v2 (2026-10-27)
- Formularz: e-mail + obowiązkowy wybór telefonu (iPhone / Android, oba dozwolone) + opcjonalna lista apek (zwinięta, puste = wszystkie). Po zaznaczeniu Androida pojawia się podpowiedź o adresie konta Google (Play wpuszcza testera tylko po tym adresie). Komunikat sukcesu mówi, że link przyjdzie mailem, gdy ruszy test na daną platformę.
- Baza `beta_signups` (projekt iskra): nowe kolumny `ios`, `android`, `apps text[]`, `consent`; migracja w `mobile/firewisp/supabase/migrations/20261027120000_beta_signups_v2.sql`. Anon dalej ma tylko INSERT, 409 (duplikat) = sukces.
- Treści maili (powitalny, zaproszenie Play, zaproszenie TestFlight, PL/EN) w `docs/beta-maile.md`; do czasu domeny wysyłka ręczna z UDW, potem Resend + funkcja brzegowa.
- Sprawdzone: 1280 i 375 px bez przewijania poziomego, wysyłka testowa trafiła do bazy z `android=true, apps={sushi-rush,turniej}`, walidacja braku platformy, wiersze testowe usunięte (lista pusta, 0 realnych zapisów).

## v3.4 — analityka bez cookies (2026-10-27)
- GoatCounter (`https://firewisp.goatcounter.com/count`, skrypt z gc.zgo.at) na wszystkich stronach generowanych, w muszlach gier `play/*` i w szablonach (`tools/flutter_splash.py`, `mobile/bog-night/index.html`). Nazwa w jednym miejscu: `GOATCOUNTER` w `tools/build_site.py`. count.js nie liczy localhost.
- Polityka prywatności (EN/PL) opisuje licznik: brak cookie, brak IP, strona + źródło + ekran + przeglądarka + kraj. Stopka: „Bez ciasteczek i reklam" zamiast „i śledzenia".
- Konto GoatCounter zakłada Tomasz (kod `firewisp`); do tego czasu żądania do licznika wracają błędem i nic się nie zapisuje.
