//Program do obliczania NWD dwóch liczb
loopWhile: POB A
           ODE B
           SOZ Koniec
           SOM bWieksze
           £AD A
           SOB loopWhile

bWieksze: POB B
          ODE A
          £AD B
          SOB loopWhile

Koniec: DOD B
        £AD A
        POB A
        STP

A: rst 48
B: rst 18