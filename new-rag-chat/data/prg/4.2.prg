// Wyszukiwanie największej liczby w tablicy o znanej długości
start:  pob jeden      // indeks i ustawiony na 1
        ład i          // będziemy startować od drugiego elementu
        pob tab        // max = tab[ 0 ]
        ład max
        pob n          // ale, ale, może tablica 1-elementowa
        ode i
        soz gotowe
dalej:  pob pobtab     // wyznacza właściwą postać rozkazu
        dod i         
        ład pobti      // i zpisuje w odpowiednie miejsce
pobti:  rpa            // tmp = Tab[ i ]
        ład tmp
        pob max        // czy nowy element nie jest większy od max
        ode tmp
        som nowe       // jeśli tak to czas zmienić max
inc:    pob i          // inkrementacja i
        dod jeden
        ład i
        ode n          // oraz sprawdzenie, czy to nie koniec
        soz gotowe
        sob dalej
nowe:   pob tmp        // max = tmp
        ład max
        sob inc
gotowe: pob max        // pobranie wyniku do AK
        stp
tmp:    rpa
i:      rpa            // indeks aktualnego elementu
jeden:  rst 1          // przydatne stałe
max:    rpa
pobtab: pob tab        // kod rozkazy POB tab
n:      rst 7          // długość tablicy
tab:    rst 6          // i wreszcie sama tablica
        rst 5
        rst 4
        rst 3
        rst 2
        rst 1
        rst 8
        rst 7