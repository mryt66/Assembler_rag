// Obliczanie silni z n z wykorzystaniem podprogramu realizującego mnożenie liczb
start:  pob n
        ode dwa
        som jest
        pob n
        dns
        pob s
        dns
        sdp mnoz
        ład s
        pob n 
        ode jeden
        ład n
        sob start
jest:   pob s
        stp
n:      rst 1	// liczba której silnię obliczamy
s:      rst 1
dwa:    rst 2
// mnożenie liczb całkowitych x i y
// liczby przekazane przez stos, wynik zwracany w akumulatorze
mnoz:   pzs
        ład ślad
        pzs
        ład y
        som neg
        pzs
        ład x
        sob next
neg:    pob zero 	// jeśli mnożnik ujemny - zamień znaki argumentów
        ode y
        ład y
        pzs
        ład x
        pob zero
        ode x
        ład x         
next:   pob ślad	// ślad od razu na stos aby potem nie zapomnieć
        dns
        pob zero
        ład wynik
petla:  pob y	// dekrementacja mnożnika
        ode jeden
        ład y
        som ready	// gdy mnożnik ujemny - koniec
        pob wynik	// mnożenie przez wielokrotne dodawanie mnożnej x
        dod x
        ład wynik
        sob petla
ready:  pob wynik
        pwr
ślad:   rpa	// miejsce na ślad
x:      rpa		// mnożna
y:      rpa		// mnożnik
wynik:  rpa	// wynik musi być zainicjowany w kodzie wartością 0
zero:   rst 0
jeden:  rst 1