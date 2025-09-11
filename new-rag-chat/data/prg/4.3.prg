// Sprawdzanie czy dana liczba n jest liczb¹ pierwsz¹ z wykorzystaniem podprogramu reszty z dzielenia
// zwraca -1 gdy liczba pierwsza
// 0 - jeœli nie
         pob d	// dopóki d < n powtarzaj
start:  ode n
        som test	// d >= n zatem liczba pierwsza
        pob minus1
        stp
test:   pob n	// oblicza n % d
        dns
        pob d
        dns
        sdp mod
        soz nie	// jeœli n % d == 0 => liczba n nie jest pierwsza
        pob d	// jeœli n % d > 0 sprawdzaj dla kolejnego dzielnika d
        dod jeden
        ³ad d
        sob start
nie:    stp        
d:      rst 2	// sprawdzanie zaczynamy od podzielnika 2
n:      rst 7	// sprawdzana liczba
jeden:  rst 1
// obliczanie reszty z dzielenia liczb naturalnych x % y
// liczby przekazane przez stos, wynik zwracany w akumulatorze
// gdy y < 1 zwraca -1
// gdy x < 0 zwraca -1
mod:    pzs
        ³ad œlad
        pzs
        ³ad y
        som negy
        soz negy
        pzs
        som negx
znowu:  ode y	// powtarza odejmowanie a¿ w akumulatorze bêdzie liczba ujemna
        som jest
        sob znowu
jest:   dod y	// aby znaleŸæ resztê trzeba dodaæ dzielnik
        ³ad x	// reszta znaleziona
        pob œlad	// nie wolno zapomnieæ o œladzie
        dns
        pob x
        pwr
negy:   pzs   	// koniecznie pobierz x ze stosu
negx:   pob œlad	// teraz zapisz tam œlad
        dns
        pob minus1	// wynikiem jest -1
        pwr
œlad:   rpa
x:      rpa
y:      rpa
minus1: rst -1