// Obliczanie iloczynu dwu liczb naturalnych x i y
petla:  pob y	// dekrementacja mnożnika
        ode jeden
        ład y
        som ready	// gdy mnożnik ujemny - koniec
        pob wynik	// mnożenie przez wielokrotne dodawanie mnożnej x
        dod x
        ład wynik
        sob petla
ready:  pob wynik
        stp
x:      rst 3		// mnożna
y:      rst 2		// mnożnik
wynik:  rst 0	// wynik musi być zainicjowany w kodzie wartością 0
jeden:  rst 1