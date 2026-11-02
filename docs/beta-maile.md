# Maile do listy beta (do czasu automatu po domenie: wysyła Tomasz z własnej skrzynki)

Adresy: Supabase → projekt `iskra` → tabela `beta_signups` (kolumny: email, ios, android, apps, lang). Wysyłać w języku z kolumny `lang`; w polu UDW (BCC), nigdy w DW.

## 1. Mail powitalny (po zapisie)

**Temat PL:** Jesteś na liście beta Firewisp Studio
**Temat EN:** You're on the Firewisp Studio beta list

PL:
```
Cześć,

dzięki za zapis. Jestem Tomasz, robię gry i apki jako Firewisp Studio, sam, w Polsce.

Już dziś możesz zagrać w przeglądarce:
– Sushi Rush: https://tomaszmatusiak-stack.github.io/firewisp-studio/play/sushi-rush/
– Bog Night: https://tomaszmatusiak-stack.github.io/firewisp-studio/play/bog-night/
– Turniej: https://tomaszmatusiak-stack.github.io/firewisp-studio/play/turniej/

Testy na telefon: Android przez Google Play (dostaniesz link do dołączenia, zadziała tylko z adresem Twojego konta Google), iPhone przez TestFlight (publiczny link). Napiszę, gdy ruszy test na Twoją platformę, kilka maili w roku, bez newslettera.

Jeśli coś nie działa albo masz pomysł, po prostu odpisz na ten mail. Żeby się wypisać, odpisz „stop”.

Tomasz
```

EN:
```
Hi,

thanks for signing up. I'm Tomasz, I make games and apps as Firewisp Studio, on my own, in Poland.

You can already play in the browser:
– Sushi Rush: https://tomaszmatusiak-stack.github.io/firewisp-studio/play/sushi-rush/
– Bog Night: https://tomaszmatusiak-stack.github.io/firewisp-studio/play/bog-night/
– Turniej: https://tomaszmatusiak-stack.github.io/firewisp-studio/play/turniej/

Phone tests: Android through Google Play (you'll get a join link; it only works with the e-mail of your Google account), iPhone through TestFlight (a public link). I'll write when a test opens for your platform, a few e-mails a year, no newsletter.

If something breaks or you have an idea, just reply. To leave the list, reply "stop".

Tomasz
```

## 2. Mail „ruszył test na Androida” (po założeniu testu zamkniętego w Play)

**Temat PL:** [Nazwa apki] na Androida: test zamknięty czeka na Ciebie
**Temat EN:** [App name] for Android: the closed test is open

PL:
```
Cześć,

ruszył test zamknięty [Nazwa apki] w Google Play. Twój adres jest już na liście testerów, więc wystarczy:
1. otworzyć ten link na telefonie: [LINK Z KONSOLI PLAY]
2. kliknąć „Zostań testerem”,
3. zainstalować apkę ze sklepu jak każdą inną.

Co testować: [2–3 zdania z sekcji „co testować”]. Każda uwaga jest cenna, nawet „nie rozumiem, co mam tu zrobić”. Odpisz na ten mail.

Ważne: Google liczy, że tester ma apkę przez 14 dni. Nie trzeba jej używać codziennie, wystarczy nie odinstalować.

Tomasz
```

EN:
```
Hi,

the closed test of [App name] on Google Play is open. Your address is on the tester list, so:
1. open this link on your phone: [LINK FROM PLAY CONSOLE]
2. tap "Become a tester",
3. install the app from the store like any other.

What to test: [2–3 sentences]. Every remark helps, even "I don't get what to do here". Just reply to this e-mail.

One thing: Google counts a tester as active when the app stays installed for 14 days. You don't have to use it daily, just don't uninstall it.

Tomasz
```

## 3. Mail „TestFlight” (gdy Apple zatwierdzi betę)

**Temat PL:** [Nazwa apki] na iPhone'a: link do TestFlight
**Temat EN:** [App name] for iPhone: your TestFlight link

PL:
```
Cześć,

beta [Nazwa apki] na iPhone'a jest gotowa. Zainstaluj aplikację TestFlight z App Store (darmowa, od Apple), potem otwórz ten link na telefonie: [PUBLICZNY LINK TESTFLIGHT]

Co testować: [2–3 zdania]. Uwagi możesz wysłać prosto z TestFlight (zrzut ekranu → „Udostępnij opinię”) albo odpisać tutaj.

Tomasz
```

EN:
```
Hi,

the [App name] beta for iPhone is ready. Install the TestFlight app from the App Store (free, by Apple), then open this link on your phone: [PUBLIC TESTFLIGHT LINK]

What to test: [2–3 sentences]. You can send feedback straight from TestFlight (screenshot → "Share feedback") or reply here.

Tomasz
```

## 4. Automat (po domenie)
Funkcja brzegowa Supabase `beta-welcome` odpalana webhookiem bazy po INSERT do `beta_signups`, wysyłka przez Resend z `beta@firewispstudio.com`, treść = mail 1 w języku z `lang`. Do zrobienia w godzinę po podpięciu domeny i weryfikacji nadawcy w Resend.

## 5. Mail „Pendulum jest w App Store” (wysyłka do całej listy, bez względu na platformę; Android dostaje go jako informację)

**Temat PL:** Pendulum: Rope Swing jest już w App Store
**Temat EN:** Pendulum: Rope Swing is out on the App Store

PL:
```
Cześć,

pierwsza gra Firewisp Studio jest w App Store: Pendulum: Rope Swing. Jeden palec, lina, sto poziomów w dziesięciu światach i jeden poziom dnia, ten sam dla wszystkich.
https://apps.apple.com/pl/app/pendulum-rope-swing/id6805826905

Start za darmo (światy 1–3 i poziom dnia), jeden zakup odblokowuje resztę. Bez reklam.

Jeśli zagrasz, jedna prośba: napisz mi, na którym poziomie było najtrudniej i czy coś Cię zirytowało. To trafia prosto do następnej wersji. Ocena w App Store też bardzo pomaga.

Następna w kolejce jest beta Sushi Rush na telefon. Napiszę, gdy ruszy.

Tomasz
```

EN:
```
Hi,

the first Firewisp Studio game is on the App Store: Pendulum: Rope Swing. One thumb, a rope, a hundred levels across ten worlds and one daily run that everyone plays the same day.
https://apps.apple.com/app/id6805826905

Free to start (worlds 1–3 and the daily run), one purchase unlocks the rest. No ads.

If you play it, one favour: tell me which level was the hardest and whether anything annoyed you. That goes straight into the next version. A rating on the App Store helps a lot too.

Next up is the Sushi Rush phone beta. I'll write when it opens.

Tomasz
```
