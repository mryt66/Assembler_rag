// Potêgowanie a^b z wykorzystaniem podprogramu mno¿enia
start:  pob b	// jeœli wyk³adnik równy 0 - nic nie trzeba robiæ
        ode jeden
        som jest
        ³ad b	// w ka¿dym przebiegu pêtli wyk³adnik jest zmniejszany
        pob a	// mno¿enie podstawy przez dotychczasowy wynik
        dns
        pob s
        dns
        sdp mnoz
        ³ad s
        sob start	// powtarzamy a¿ wyk³adnik równy 0
jest:   pob s	// wynik znaleziony
        stp
a:      rst 5	// podstawa
b:      rst 3	// wyk³adnik
s:      rst 1	// wynik zainicjowany wartoœci¹ 1
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