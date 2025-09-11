//Program do znalezienia minimum w podanej tablicy
POB Tablica
£AD Minimalny
POB N
£AD loop_counter
£AD powtorzenieProgramu
Pêtla: POB loop_counter
       ODE Jeden
       SOZ Powtorzenie
       £AD loop_counter
Rozkaz: POB Tablica
        £AD Element
        POB Minimalny
        ODE Element
        SOM Wiekszy
        SOZ Wiekszy
        POB Element
        £AD Minimalny
        POB Rozkaz
        DOD Jeden
        £AD Rozkaz
        SOB Pêtla
Wiekszy: POB Rozkaz
         DOD Jeden
         £AD Rozkaz
         SOB Pêtla
Powtorzenie: POB powtorzenieProgramu
             ODE Jeden
             SOZ Koniec
             £AD powtorzenieProgramu
             POB Rozkaz
             ODE Jeden
             £AD Rozkaz
             SOB Powtorzenie       
Koniec: POB Minimalny
        STP
Element: rpa        
Minimalny: rpa
Jeden: rst 1
N:   rst 5
loop_counter: rpa
powtorzenieProgramu: rpa
Tablica: rst 10
         rst -55
         rst 12
         rst -69