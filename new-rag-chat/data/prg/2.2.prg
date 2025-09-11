// „Odwracanie” tablicy o znanej długości (ABC › CBA )
start:  pob zero      // inicjalizacja indeksów i i j
        ład i
        pob n
        ode jeden
        ład j
dalej:  pob pobtab    // ustalenie właściwej postaci
        dod i         // rozkazów pob i ład
        ład pobti
        pob pobtab
        dod j
        ład pobtj
        pob ładtab
        dod i
        ład ładti
        pob ładtab
        dod j
        ład ładtj
pobti:  rpa           // tu zaczyna się właściwa zamiana
        ład tmp       // konieczne użycie zmiennej tymczasowej
pobtj:  rpa           // Tab[ i ] = Tab[ j ]
ładti:  rpa
        pob tmp       // Tab[ j ] = tmp
ładtj:  rpa
        pob i         // przesunięcie indeksów
        dod jeden     // i o jeden w dół
        ład i
        pob j         // j o jeden w górę
        ode jeden
        ład j       
        pob i         // pętla wykonywana dalej jeśli
        ode j         // i < j
        som dalej     // w przeciwnym razie koniec
        stp            
i:      rst 0
j:      rpa
jeden:  rst 1          // przydatne stałe
zero:   rst 0
tmp:    rpa            // tymczasowa zmienna
pobtab: pob tab        // kody rozkazów POB tab i ŁAD tab
ładtab: ład tab
n:      rst 6          // długość tablicy
tab:    rst 6          // i wreszcie sama tablica
        rst 5
        rst 4
        rst 3
        rst 2
        rst 1
        rst 8
        rst 7