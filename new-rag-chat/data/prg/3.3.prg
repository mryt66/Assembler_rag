// Obliczanie wartoœci wyznacznika macierzy 2 x 2 przy wykorzystaniu podprogramu mno¿enia
// a11 * a22 - a12 * a21
start:  pob a12	// a12 * a21
        dns
        pob a21
        dns
        sdp mnoz
        ³ad s
        pob a11	// a11 * a22
        dns
        pob a22
        dns
        sdp mnoz
        ode s	// a11 * a22 - a12 * a21
        ³ad s
        stp        
a11:    rst 5	// elementy macierzy a
a12:    rst 4
a21:    rst 1
a22:    rst 2
s:      rst 0	// zmienna pomocnicza
// mno¿enie liczb ca³kowitych x i y
// liczby przekazane przez stos, wynik zwracany w akumulatorze
mnoz:   pzs
        ³ad œlad
        pzs
        ³ad y
        som neg
        pzs
        ³ad x
        sob next
neg:    pob zero 	// jeœli mno¿nik ujemny - zamieñ znaki argumentów
        ode y
        ³ad y
        pzs
        ³ad x
        pob zero
        ode x
        ³ad x         
next:   pob œlad	// œlad od razu na stos aby potem nie zapomnieæ
        dns
        pob zero
        ³ad wynik
petla:  pob y	// dekrementacja mno¿nika
        ode jeden
        ³ad y
        som ready	// gdy mno¿nik ujemny - koniec
        pob wynik	// mno¿enie przez wielokrotne dodawanie mno¿nej x
        dod x
        ³ad wynik
        sob petla
ready:  pob wynik
        pwr
œlad:   rpa	// miejsce na œlad
x:      rpa		// mno¿na
y:      rpa		// mno¿nik
wynik:  rpa	// wynik musi byæ zainicjowany w kodzie wartoœci¹ 0
zero:   rst 0
jeden:  rst 1