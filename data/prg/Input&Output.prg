//Program do pracy na We/Wy. Czyta znaki wprowadzone przez u¿ytkownika i po
//przyjœciu czwartego znaku '$' wypisuje on wszystkie wpisane znaki 'M' i 'O'
loop: WPR 1
      ODE dolar
      SOZ iter
      DOD dolar
      ODE duz_K
      SOM loop
      DOD duz_K
      ODE duz_P
      SOM przedzial
      SOZ przedzial 
      SOB loop
przedzial: DOD duz_P  
dodTab: £AD tab       
        POB dodTab
        DOD jeden
        £AD dodTab
        POB rozm_tab
        DOD jeden
        £AD rozm_tab
        SOB loop
iter: POB n_dol
      ODE jeden
      £AD n_dol
      SOZ wypiszKoniec
      SOB loop
wypiszKoniec: POB endl
              WYP 2
              POB rozm_tab
              SDP WRITE
              POB endl
              WYP 2
              POB rozm_tab
              £AD rozm_tab_temp
loop2: POB rozm_tab_temp
       ODE jeden
       £AD rozm_tab_temp
       SOZ iterM                     
przejscieTab: POB tab
              ODE duz_M
              SOZ licznikM
              DOD duz_M
              ODE duz_O
              SOZ licznikO
              DOD duz_O
              SOB przejscieTab2
licznikM: POB n_M
          DOD jeden
          £AD n_M
          SOB przejscieTab2
licznikO: POB n_O
          DOD jeden
          £AD n_O
          SOB przejscieTab2                
przejscieTab2: POB przejscieTab
               DOD jeden
               £AD przejscieTab
               SOB loop2               
iterM: POB n_M
       £AD iteracja                          
wypiszM:     POB iteracja
             ODE jeden
             £AD iteracja
             SOM koniecLinii
             POB duz_M
             WYP 2
             POB spacja
             WYP 2
             SOB wypiszM
koniecLinii: POB endl
             WYP 2
             POB n_O
             £AD iteracja 
wypiszO: POB iteracja
         ODE jeden
         £AD iteracja
         SOM koniec
         POB duz_O
         WYP 2
         POB spacja
         WYP 2
         SOB wypiszO             
koniec: stp          

WRITE: £AD liczba
       POB Zero
       DNS
       POB liczba
       SOM Abs
Posit: DZI St10
       MNO St10
       £AD tmp
       POB liczba
       ODE tmp
       DOD Znak0
       DNS
       POB tmp
       DZI St10
       SOZ Koncz
       £AD liczba
       SOB Posit
Abs: POB Minus
     WYP 2
     POB Zero
     ODE liczba
     £AD liczba
     SOB Posit
Koncz: PZS
       SOZ Wracaj
       WYP 2
       SOB Koncz
Wracaj: PWR

duz_K: rst 'K'
duz_P: rst 'P'
duz_M: rst 'M'
duz_O: rst 'O'
zero: rst 0
jeden: rst 1
St10: rst 10
n_dol: rst 4
n_M: rst 0
n_O: rst 0
dolar: rst '$'
Minus: RST '-'
Znak0: rst '0'
spacja: rst ' '
endl: rst 10
tmp: rpa
liczba: rpa
iteracja: rpa
rozm_tab_temp: rst 0
rozm_tab: rst 0
tab: rpa