//Oblicz potęgowanie dwóch liczb naturalnych

POB Final
DOD Num1
LAD Final

POB Num2
SOZ end_exp_one

POB Num1
SOZ end_exp_zero

Main_exp:
POB Num2
ODE one
SOZ end_exp
LAD Num2

//Poniższy program mnoży dwie liczby
Main_product:
POB Num1
LAD N1
POB Final
LAD N2
//Sprawdzanie licznika
POB N2
SOZ end
SOM Negative
LAD Counter

//Sprawdzanie wyniku mnożenia
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

//Jeżeli licznik jest ujemny, zmień wartości licznika i wyniku mnożenia
Negative: 
LAD Product
LAD First_Prdct
POB N1
SOZ end
LAD Counter

SOB loop

end: 
POB Product
LAD Final
SOB Main_exp
//Koniec mnożenia

end_exp:
POB Final
STP

end_exp_one:
POB one
STP

end_exp_zero:
POB zero
STP


One: RST 1
N1: RST 0
N2: RST 0
First_Prdct: RPA
Counter: RPA
Product: RPA
//Dla Mnożenia

Num1: RST 5
Num2: RST 0
Final: RST 0
zero: RST 0




