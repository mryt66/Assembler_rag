// Obliczanie liczby wystąpień określonej wartości w N-elementowej tablicy bajtów
start:  pob zero       // indeks i ustawiony na 0
        ład i          // 
dalej:  pob pobtab     // wyznacza właściwą postać rozkazu
        dod i         
        ład pobti      // i zpisuje w odpowiednie miejsce
pobti:  rpa            // Tab[ i ]
        ode wz
        soz zwiększ
inc:    pob i          // inkrementacja i
        dod jeden
        ład i
        ode n          // oraz sprawdzenie, czy to nie koniec
        soz gotowe
        sob dalej
zwiększ: pob ile       // kolejny element znaleziony 
        dod jeden
        ład ile
        sob inc
gotowe: pob ile        // pobranie wyniku do AK
        stp
tmp:    rpa
i:      rpa            // indeks aktualnego elementu
jeden:  rst 1          // przydatne stałe
zero:   rst 0
wz:     rst 3
ile:    rst 0
pobtab: pob tab        // kod rozkazy POB tab
n:      rst 7          // długość tablicy
tab:    rst 6          // i wreszcie sama tablica
        rst 3
        rst 4
        rst 3
        rst 2
        rst 1
        rst 3
        rst 3