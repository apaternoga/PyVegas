<div align="center">
<h1>PyGames</h1>

<p >Zestaw gier karcianych i losowych napisanych w Pythonie</p>
</div>

<h2>Spis tresci</h2>

<h2>Wprowadzenie</h2>

<h2>Zaimplemetowane funkcjonalności</h2>
<ul>
<li><b>Menu główne aplikacji</b> - uruchomienie programu, wybór dostępnej gry oraz wyjście z aplikacji.</li>
<li><b>Modułowa budowa projektu</b> - logika gier znajduje się w <code>games/</code>, a elementy wspólne (menu, obsługa wejścia) w <code>core/</code>.</li>
<li><b>Obsługa zasobów</b> - wykorzystanie plików z katalogu <code>assets/</code> (np. grafiki, dźwięki, czcionki - zależnie od gry).</li>
<li><b>Blackjack:</b>
<ul>
<li>rozdawanie kart graczowi i krupierowi</li>
<li>zliczanie punktów oraz rozstrzyganie wyniku rundy (wygrana/przegrana/remis)</li>
<li>podstawowe akcje gracza w trakcie rundy (np. dobierz/pasuj - zgodnie z zasadami gry)</li>
</ul>
</li>
<li><b>Crash:</b>
<ul>
<li>mechanika rosnącego mnożnika, który w losowym momencie "crashuje"</li>
<li>możliwość wypłaty przed crashem oraz obliczanie wygranej na podstawie aktualnego mnożnika</li>
</ul>
</li>
<li><b>Komunikaty i stan rozgrywki</b> - prezentowanie wyniku, informacji o aktualnym stanie oraz możliwość rozpoczęcia kolejnej rundy.</li>
</ul>

<h2>Intrukcja uruchomienia (KROK PO KROKU)</h2>
<p>Aby projekt zadziałał poprawnie na komputerze trzeba wykonać następujące kroki w terminalu:</p>
<ul>
<li>Sklonować repozytorium przy pomocy polecenia:<br /><code>git clone https://github.com/apaternoga/pygames.git</code></li>
<li>Wejść do folderu pygames:<br /><code>cd pygames</code></li>
<li>Pobrać wszystkie brakujące zasoby:<br /><code>pip install -r requirements.txt</code></li>
<li>Uruchomić grę:<br /><code>python main.py</code></li>
</ul>

<h2>Struktura plików</h2>
<ul>
<li><b>main.py</b> - punkt wejścia projektu (uruchamia aplikację i startuje gry)</li>
<li><b>games/</b> - implementacje gier (logika poszczególnych mini-gier)</li>
<li><b>core/</b> - wspólne elementy projektu (menu, obsługa wejścia)</li>
<li><b>assets/</b> - zasoby (grafiki, dźwięki, czcionki)</li>
<li><b>requirements.txt</b> - zależności do instalacji przez pip</li>
<li><b>INSTRUKCJA.txt</b> - dodatkowa instrukcja, opis działania</li>
<li><b>CREDITS.txt</b> - źródła </li>
<li><b>LICENSE</b> - licencja projektu</li>
</ul>

<h2>Autorzy i podział zadań</h2>
<ul>
<li><b>Adrian Paternoga</b> - Blackjack</li>
<li><b>Adam Zalewski</b> - Crash</li>
<li><b>Filip Liskowski</b> - README</li>
<li><b>Miłosz Kiedrzyński</b> - </li>
<li><b>Patryk Iżbicki</b> - </li>
</ul>

<h2>Źródła</h2>

<h2>Licencja</h2>
