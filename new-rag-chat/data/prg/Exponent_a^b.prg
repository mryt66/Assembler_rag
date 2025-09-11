//Program do obliczenia wyra¿enia a^b
       POB A
       £AD Add_counter
       ODE jeden
       £AD A_Ode_Jeden 
       POB B
       £AD B_przechowanie       
              
petla: POB B
       ODE jeden
       SOZ koniec
       £AD B
       POB A
       £AD A_przechowanie
       
funkcja: POB Add_counter
         ODE jeden 
         SOZ counter_zero
         £AD Add_counter
         POB A_przechowanie
         DNS
         POB A
         DNS
         SDP mnozenie
         PZS
         £AD A
         SOB funkcja
          
mnozenie: PZS
          £AD pointer
          PZS
          £AD A_podprogram
          PZS
          £AD A_stos
          POB A_podprogram
          DOD A_stos
          DNS
          POB pointer
          DNS
          PWR
          
counter_zero: POB Add_counter
              DOD A_Ode_Jeden
              £AD Add_counter
              SOB petla
                       
koniec: POB A
        STP
A: rst 10
Add_counter: rst 0
A_przechowanie: rpa
A_stos: rpa
A_podprogram: rpa
A_Ode_Jeden: rpa
B: rst 2
B_przechowanie: rpa
jeden: rst 1
pointer: rpa