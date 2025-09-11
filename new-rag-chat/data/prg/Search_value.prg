//Przeszukaj tablicę w poszukiwaniu wartości określonej w oddzielnej zmiennej i policz liczbę wystąpień.

loop:
inst: POB array
ODE CharValue
SOZ end
DOD CharValue

//Sprawdzenie wartości w tablicy
ODE LookedForValue
SOZ OccurenceFound
SOB continue

OccurenceFound: POB occurences
                DOD one
                LAD occurences
                
continue: POB inst
          DOD one
          LAD inst
          SOB loop
          
end: POB occurences
     STP

CharValue: RST 0
ARRAY: RST -3
       RST 2
       RST 3
       RST 5
       RST 6
       RST 5
       RST 10
       RST -3
       RST 0 
LookedForValue: RST -3
occurences: RST 0
one: RST 1