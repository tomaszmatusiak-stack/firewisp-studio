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
| Fraunces | brak pliku w repo, pobranie wymaga zgody | systemowy serif (Iowan Old Style / Palatino / Georgia / Noto Serif); podmiana na Fraunces = dwa pliki woff2 w `assets/fonts/` i jedna linia `--font-display` |

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
