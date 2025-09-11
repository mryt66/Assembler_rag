//zdekrementuj wszystkie elementy w tablicy
loop:
POB size
ODE one
SOM end
LAD SIZE

inst1: POB ARRAY
ODE DecrementBy
inst2: LAD ARRAY

POB inst1
DOD one
LAD inst1

POB inst2
DOD one
LAD inst2

SOB loop 

end: 
STP


SIZE: RST 8  //number of elements: 3 | liczba elementów: 3
ARRAY: RST 8
RST 10
RST 3
RST 1
RST 2
RST 3
RST 4
RST 5

DecrementBy: RST 2
one: RST 1