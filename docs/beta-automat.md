# Automat listy beta (4.11.2026)

Zero ręcznej wysyłki. Tester zapisuje się na stronie, resztę robi system:

| Kiedy | Co | Skąd treść |
|---|---|---|
| do 10 min po zapisie | **mail powitalny**: linki do gier w przeglądarce + aktywne linki testów dla jego platform i apek | `welcomeMail()` |
| gdy w `beta_links` pojawi się aktywny link pasujący do testera | **mail „ruszył test”** (TestFlight / Play) z instrukcją i „co testować” | `linkMail()` |
| 5 dni po powitaniu (`SURVEY_DAYS`) | **mail z ankietą**: link `/feedback/?t=TOKEN` (EN) lub `/pl/opinia/?t=TOKEN` (PL) | `surveyMail()` |
| kliknięcie „wypisz mnie” | `unsubscribed_at`, żadnych kolejnych maili | RPC `beta_unsubscribe` |

Język z kolumny `lang` zapisu (pl → polski, reszta → angielski). Każdy mail ma stopkę z linkiem wypisania i nagłówek `List-Unsubscribe`.

## Elementy

- **Baza** (osobny projekt Supabase `firewisp-studio` pod stronę, decyzja 5.11.2026: lista marketingowa studia nie może leżeć w backendzie zaparkowanej apki Firewisp, bo gdy `iskra` się zapauzowała, padł formularz na stronie; migracja `mobile/firewisp/supabase/migrations/20261104120000_beta_mailer.sql`, poprzedzona migracją `beta_signups` z 20.10):
  `beta_signups` + kolumny `token`, `welcome_sent_at`, `survey_sent_at`, `unsubscribed_at`;
  `beta_links` (app, platform web/ios/android, url, tytuły PL/EN, „co testować”, `active`);
  `beta_link_sent` (kto który link dostał); `beta_feedback` (ankieta); `beta_mail_log` (każda wysyłka i błąd).
  RPC dla strony (anon + token, bez odczytu tabel): `beta_context`, `beta_feedback_submit`, `beta_unsubscribe`.
- **Funkcja brzegowa** `beta-mailer` (`mobile/firewisp/supabase/functions/beta-mailer/index.ts`): trzy przebiegi (powitanie, linki, ankieta), max 40 maili na wywołanie, po błędzie Resend 6 h przerwy dla tej osoby i rodzaju maila, `MAIL_ALLOWLIST` do testów na własnym adresie.
- **Cron**: `cron.schedule('beta-mailer', '*/10 * * * *')` woła funkcję przez `pg_net`; adres funkcji (`beta_mailer_url`) i sekret (`beta_mailer_secret`) czyta z Vault, więc migracja nie zna identyfikatora projektu.
- **Strona ankiety**: `src/feedback.html` → `feedback/` (EN) i `pl/opinia/` (PL), `noindex`, poza sitemap. Pięć pytań: apka, czy zainstalowano, ocena 1–5, co się podobało, co przeszkadzało, polecenie.

## Wdrożenie (jednorazowo)

Warunki: nowy projekt `firewisp-studio` utworzony w dashboardzie (Tomasz; organizacja ta sama, Frankfurt, Free), konto Resend z zweryfikowaną domeną `firewispstudio.com` (rekordy SPF/DKIM w home.pl), klucz API Resend.

```bash
cd ~/claude/mobile/firewisp && supabase link --project-ref NOWY_REF
cd ~/claude/mobile/firewisp && MAIL_ALLOWLIST=tomasz.matusiak@post.pl ./tool/beta_mailer_deploy.sh re_KLUCZ "Firewisp Studio <hello@firewispstudio.com>" https://firewispstudio.com
```

Po wdrożeniu podmienić adres projektu i klucz anonimowy w `src/index.html` i `src/feedback.html` (stałe `SB_URL`, `SB_KEY`), przebudować stronę. Stary projekt `iskra` zostaje zapauzowany; tabela `beta_signups` tam ma zero prawdziwych zapisów, nic nie migrujemy.

Pierwsze uruchomienie z `MAIL_ALLOWLIST` = tylko adres Tomasza dostaje maile (test na własnym zapisie ze strony). Gdy maile wyglądają dobrze: to samo polecenie bez `MAIL_ALLOWLIST=` (ustawia pustą listę = wszyscy).

## Obsługa na co dzień (SQL w dashboardzie)

- Nowy test ruszył (TestFlight zatwierdzony / ścieżka w Play gotowa): `update beta_links set active = true where id = …;` albo `insert into beta_links (app, platform, url, title_pl, title_en, hint_pl, hint_en, active) values (…)`. W ciągu 10 min pasujący testerzy dostają mail.
- Po domenie: `update beta_links set url = replace(url, 'https://tomaszmatusiak-stack.github.io/firewisp-studio', 'https://firewispstudio.com') where platform = 'web';` (stare adresy i tak przekierowują 301).
- Odpowiedzi: `select s.email, f.* from beta_feedback f join beta_signups s on s.id = f.signup_id order by f.created_at desc;`
- Co poszło: `select * from beta_mail_log order by created_at desc limit 50;` Cron: `select * from cron.job_run_details order by start_time desc limit 10;`

## Ograniczenia, o których trzeba pamiętać

- **Android**: link testu zamkniętego w Play działa tylko, gdy adres testera jest na liście w Play Console (listy adresów nie da się uzupełniać przez API). Dopóki ścieżka Kropli używa listy adresów, link `kropla/android` zostaje `active = false`. Wyjście: grupa Google z otwartym dołączaniem jako źródło testerów (dwa kroki dla testera, instrukcja w mailu to uwzględnia) albo ręczne dopisanie adresów raz na kilka dni.
- **iOS**: publiczny link TestFlight Sushi Rush (`V8ehNnvF`) aktywny od startu: Beta App Review zatwierdzony 3.11.2026, strona dołączenia odpowiada 200 (sprawdzone 5.11).
- Resend free: 100 maili dziennie, 3000 miesięcznie; funkcja wysyła max 40 na przebieg.
- Apple i Google nie zdradzają, kto faktycznie zainstalował, więc ankieta idzie do każdego zapisanego; pierwsze pytanie to „udało się zainstalować?”.
- Projekt Supabase na planie Free pauzuje się po 7 dniach bez ruchu; heartbeat z GitHub Actions nie uchronił `iskra` przed pauzą 4.11 (przyczyna nieustalona). Nowy projekt dopisać do `.github/workflows/supabase-heartbeat.yml` w repo firewisp i obserwować przez pierwsze 2 tygodnie, czy cron co 10 min wystarcza.
