//Oblicz iloczyn dwóch liczb naturalnych

LOOP:
POB     PRODUCT
DOD     A
LAD     PRODUCT
POB     B
ODE     ONE
SOZ     END
LAD     B
SOB     LOOP

END:
POB     PRODUCT
STP

ONE:    RST 1
A:      RST 6
B:      RST 3
PRODUCT:   RST 0
