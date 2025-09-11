//Przeszukaj tablicę w poszukiwaniu wartości określonej w oddzielnej zmiennej i zapisz indeks jej pierwszego wystąpienia.
//Użyj dodatkowej zmiennej do oznaczenia końca tablicy.

NEXT: POB ARRAY
       SOM END_OF_ARRAY
       ODE SEARCHED
       SOZ FOUND      
L1:     
      POB INDEX
      DOD ONE
      LAD INDEX
        POB NEXT
        DOD ONE
        LAD NEXT
        SOB NEXT  

      
FOUND:  STP

END_OF_ARRAY: STP 

SEARCHED: RST 7
INDEX: RST 1
ONE: RST 1 
CharValue: RST -1  // dodatkowa zmienna
ARRAY: RST 1
RST 2
RST 2
RST 7
RST -1  // koniec tablicy