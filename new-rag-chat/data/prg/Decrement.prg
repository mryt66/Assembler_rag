//Zdekrementuj wszystkie elementy w tablicy
//liczba elementów w tablicy jest określona w osobnej zmiennej
//ROZMIAR: RST 3 //liczba elementów: 3
//TABLICA: RST 1
//RST 2
//RST 3


TABLE_SIZE: POB     SIZE
            ODE     ONE
            SOM     END
            LAD     SIZE

SUB: POB     ARRAY
     ODE     ONE

WHERE: LAD     ARRAY

L1: POB     SUB
    DOD     ONE
    LAD     SUB
    POB     WHERE
    DOD     ONE
    LAD     WHERE
    SOB     TABLE_SIZE
           
END: STP

ONE:    RST 1
SIZE:   RST 2
ARRAY:  RST 1
        RST 2
        RST 3
        RST 4
        RST 5
        RST 6
