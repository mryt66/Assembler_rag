//Iloczyn 2 liczb naturalnych

Main:
//Ustalenie wartości licznika
POB N2
SOZ end
SOM Negative
LAD Counter

//Ustalenie wartości iloczynu
POB N1
SOZ end
LAD Product
LAD First_Prdct

loop:
POB Counter
ODE One
LAD Counter
SOZ end

POB Product
DOD First_Prdct
LAD Product

SOB loop

//Jeśli licznik jest ujemny, zmień wartości licznika i iloczynu
Negative: 
LAD Product
LAD First_Prdct
POB N1
SOZ end
LAD Counter

SOB loop

end: 
POB Product
STP

One: RST 1
N1: RST 4
N2: RST 10
First_Prdct: RPA
Counter: RPA
Product: RPA

 
