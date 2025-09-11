// Obliczanie liczby wystąpień określonej wartości Val w N-elementowej tablicy bajtów Tab
start:     pob N
           ode jeden
           som koniec
           ład N
rozkaz:    pob Tab
           ode Val
           soz Inc
Dalej:     pob rozkaz
           dod jeden
           ład rozkaz
           sob start
koniec:    pob ile
           stp
Inc:       pob ile
           dod jeden
           ład ile
           sob Dalej
Val:       rst 3
ile:       rst 0
jeden:     rst 1
N:         rst 5
Tab:       rst 1
           rst 2
           rst 3
           rst 6
           rst 3
           rst 3                                       