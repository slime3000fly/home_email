# Skrypt do tworzenia konta Home.pl

## Skrypt ma na celu automatyzację procesu tworzenia nowego konta e-mail na platformie Home.pl. Zadaniem skryptu jest:

    1. Skopiowanie pliku Markdown (MD) o nazwie test.md.
    2. Zmiana nazwy skopiowanego pliku na podstawie imienia i nazwiska wprowadzonego przez użytkownika.
    3. Odczytanie loginu z pliku JSON o nazwie .pass.json.
    4. Zamiana wprowadzonego imienia i nazwiska na styl, który jest używany w loginie.
    5. Zmiana loginu, hasła i imienia w pliku MD.
    6. Logowanie do panelu Home.pl.
    7. Nawigacja do sekcji tworzenia nowego konta e-mail.
    8. Ustawienia domeny, generowanie hasła i wprowadzenie danych.
    9. Zapisanie hasła do zmiennej.
    10. Zamknięcie przeglądarki.
    11. Konwersja pliku MD na PDF.

## Użyte biblioteki

    - docx - do obsługi plików Word.
    - md2pdf - do konwersji plików Markdown na PDF.
    - selenium - do automatyzacji interakcji z przeglądarką.

## Funkcje w skrypcie

    - skopiuj_i_zmien_nazwe(plik_wejsciowy, nowa_nazwa)
        Skopiuje plik i zmieni jego nazwę na nową. Zwróci nową nazwę pliku.

    - open_json()
        Otworzy plik JSON z hasłem i wczyta login. Zwróci login lub None, jeśli brak informacji.

    - zamien_na_styl(text)
        Zamieni tekst na styl używany w loginach (małe litery, podkreślenia, brak polskich znaków).

    - zmien_login_w_md(sciezka_do_pliku_md, nowy_login)
        Zmieni login w pliku MD.

    - zmien_haslo_w_md(sciezka_do_pliku_md, haslo)
        Zmieni hasło w pliku MD.

    - zmien_imie_nazwisko(sciezka_do_pliku_md, imie_nazwisko)
        Zmieni imię i nazwisko w pliku MD.

    - stworz_skrzynke_home(login)
        Stworzy nową skrzynkę e-mail na platformie Home.pl.

    - Główna część skryptu:
        - Wczytanie imienia i nazwiska od użytkownika.
        - Zmiana nazwy pliku MD na podstawie imienia i nazwiska.
        - Zmiana loginu, hasła i imienia w pliku MD.
        - Logowanie do Home.pl i tworzenie nowej skrzynki e-mail.
        - Konwersja pliku MD na PDF.

## Instrukcja użycia

    1. Uruchom skrypt i podaj imię i nazwisko oraz hasło do konta administatora, gdy zostaniesz o to poproszony.
    2. Skrypt skopuje plik test.md, zmieni nazwę na podstawie imienia i nazwiska, a następnie wczyta login z pliku JSON.
    3. Zmieni login, hasło i imię w pliku MD.
    4. Zaloguje się do panelu Home.pl, stworzy nową skrzynkę e-mail i zapisze hasło.
    5. Zmieni hasło w pliku MD i przekonwertuje plik MD na PDF.

## Wymagania

    - Biblioteka docx - zainstaluj za pomocą pip install python-docx.

    - Biblioteka md2pdf - zainstaluj za pomocą pip install md2pdf.

    - Biblioteka selenium - zainstaluj za pomocą pip install selenium.

    Wymagany jest zainstalowany przeglądarkowy sterownik Chrome (ChromeDriver) dostępny pod adresem: https://googlechromelabs.github.io/chrome-for-testing/

## UWAGA

    Pamiętaj, aby bezpiecznie przechowywać plik JSON z loginem.
    Skrypt jest dostosowany do obsługi przeglądarki Chrome i może wymagać dostosowania, jeśli używasz innej przeglądarki.
    Skrypt korzysta z funkcji headless dla przeglądarki Chrome (uruchamia się w tle).

