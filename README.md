<div align="center">

# PyGames

Zestaw gier karcianych i losowych napisanych w Pythonie

<img src="assets/pyvegas.png" alt="PyVegas / PyVegas baner" width="700" />

</div>

## Spis treści
- [Wprowadzenie](#wprowadzenie)
- [Zaimplementowanie funkcjonalności](#zaimplementowane-funkcjonalności)
- [Intrukcja uruchomienia (KROK PO KROKU)](#intrukcja-uruchomienia-krok-po-kroku)
- [Struktura plików](#struktura-plików)
- [Autorzy i podział zadań](#autorzy-i-podział-zadań)
- [Źródła](#źródła)

## Wprowadzenie

PyVegas to projekt powstały w ramach studiów informatycznych realizowany w Pythonie, którego celem jest stworzenie jednej, prostej aplikacji zbierającej kilka mini-gier w jednym miejscu. Program udostępnia wspólne **menu główne**, z którego można uruchomić wybraną grę, śledzić przebieg rozgrywki i w każdej chwili wrócić do wyboru kolejnej pozycji.

Projekt został zaprojektowany w sposób **modułowy**: każda gra posiada własną logikę w katalogu `games/`, natomiast elementy współdzielone (np. nawigacja, obsługa wejścia, wspólne komponenty) są wydzielone do `core/`. Dodatkowo repozytorium zawiera katalog `assets/` przeznaczony na zasoby wykorzystywane w grach (np. grafiki, dźwięki, czcionki). Taka struktura ułatwia rozwój projektu oraz dodawanie kolejnych gier bez przebudowy całej aplikacji.

Aktualnie w zestawie znajdują się m.in.:
- **Blackjack** - klasyczna gra karciana przeciwko krupierowi,
- **Crash** - gra losowa oparta o rosnący mnożniki i decyzję o wypłacie w odpowiednim momencie.

## Zaimplementowane funkcjonalności

- **Menu główne aplikacji** - uruchomienie programu, wybór dostępnej gry oraz wyjście z aplikacji.
- **Modułowa budowa projektu** - logika gier znajduje się w `games/`, a elementy wspólne (menu, obsługa wejścia) w `core/`.
- **Obsługa zasobów** - wykorzystanie plików z katalogu `assets/` (np. grafiki, dźwięki, czcionki - zależnie od gry).
- **Blackjack:**
  - rozdawanie kart graczowi i krupierowi
  - zliczanie punktów oraz rozstrzyganie wyniku rundy (wygrana/przegrana/remis)
  - podstawowe akcje gracza w trakcie rundy (np. dobierz/pasuj - zgodnie z zasadami gry)
- **Crash:**
  - mechanika rosnącego mnożnika, który w losowym momencie "crashuje"
  - możliwość wypłaty przed crashem oraz obliczanie wygranej na podstawie aktualnego mnożnika
- **Komunikaty i stan rozgrywki** - prezentowanie wyniku, informacji o aktualnym stanie oraz możliwość rozpoczęcia kolejnej rundy.

## Intrukcja uruchomienia (KROK PO KROKU)

Aby projekt zadziałał poprawnie na komputerze trzeba wykonać następujące kroki w terminalu:

- Sklonować repozytorium przy pomocy polecenia:
  `git clone https://github.com/apaternoga/pygames.git`
- Wejść do folderu pygames:
  `cd pygames`
- Pobrać wszystkie brakujące zasoby:
  `pip install -r requirements.txt`
- Uruchomić grę:
  `python main.py`

## Struktura plików

- **main.py** - punkt wejścia projektu (uruchamia aplikację i startuje gry)
- **games/** - implementacje gier (logika poszczególnych mini-gier)
- **core/** - wspólne elementy projektu (menu, obsługa wejścia)
- **assets/** - zasoby (grafiki, dźwięki, czcionki)
- **requirements.txt** - zależności do instalacji przez pip
- **INSTRUKCJA.txt** - dodatkowa instrukcja, opis działania
- **CREDITS.txt** - źródła
- **LICENSE** - licencja projektu

## Autorzy i podział zadań

- **Adrian Paternoga** - Blackjack
- **Adam Zalewski** - Crash
- **Filip Liskowski** - README
- **Miłosz Kiedrzyński** - 
- **Patryk Iżbicki** - 
- **Borys Kaczka** - 

## Źródła
