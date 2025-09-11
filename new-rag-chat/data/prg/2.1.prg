// Obliczanie NWW dwu liczb naturalnych a i b
        pob a     // kopiowanie a do a1 i b do b1
        ład a1
        pob b
p1:     ład b1
pętla:  ode a1
        soz jest  // jeśli a1 = b1 - koniec obliczeń
        som zmienb // jeśli b1 < a1 należy zwiększyć b1
        pob a1     // w przeciwnym razie zwiększyć a1 dodając oryginalne a
        dod a
        ład a1
        pob b1     // przed kolejnym testem równości w AK ma być b1
        sob pętla
zmienb: pob b1     // zwiększyć b1 dodając oryginalne b
        dod b
        sob p1     // i znów testować równość
jest:   pob a1     // wynik zostawia w AK
        stp
a:      rst 6      // argumenty NWW
b:      rst 8
a1:     rpa        // zmienne przechowujące skopiowane dane
b1:     rpa