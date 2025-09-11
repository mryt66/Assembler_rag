//Program do pracy z przerwaniami. Wypisuje '#' do momentu przyjœcia przerwania 
//w trakcie którego wypisuje liczby.
SOB PROGRAM
SOB P1
SOB P2
SOB P3
SOB P4

PROGRAM: POB dwa
	 £AD P1counter
	 POB trzy
	 £AD i
	 POB zero
	 £AD wypisanieP1
			
loop1: POB i
       ODE jeden
       £AD i
       SOM przygP2
       POB wypisanieP1
       DOD jeden
       £AD wypisanieP1
       SOB loop1
			
przygP2: POB cztery
	 £AD P2counter
	 POB trzy
	 £AD i
	 POB zero
	 £AD wypisanieP2
			
loop2: POB i
       ODE jeden
       £AD i
       SOM przygP3
       POB wypisanieP2
       DOD dwa
       £AD wypisanieP2
       SOB loop2
				
przygP3: POB szesc
	 £AD P3counter
	 POB trzy
	 £AD i
	 POB zero
	 £AD wypisanieP3
			
loop3: POB i
       ODE jeden
       £AD i
       SOM przygP4
       POB wypisanieP3
       DOD trzy
       £AD wypisanieP3
       SOB loop3
			
przygP4: POB osiem
	 £AD P4counter
	 POB trzy
	 £AD i
	 POB zero
	 £AD wypisanieP4
			
loop4: POB i
       ODE jeden
       £AD i
       SOM przygZnak
       POB wypisanieP4
       DOD cztery
       £AD wypisanieP4
       SOB loop4		
			
przygZnak: POB hasztaq

infiLoop: WYP 2
          SOB infiLoop

koniec:	PZS
        PZS
        stp
         
P1: CZM MASKA1
    MAS 15
    DNS
    POB wypisanieP1
    £AD it1
    
wypiszP1: POB it1
	  ODE jeden
	  £AD it1
	  SOM koniecP1
	  POB nr1
	  WYP 2
	  SOB wypiszP1
						
koniecP1: POB P1counter
	  ODE jeden
	  £AD P1counter
	  SOZ koniec
          PZS
          MSK MASKA1
          PWR
			
P2: CZM MASKA2
    MAS 7
    DNS
    POB wypisanieP2
    £AD it2
    
wypiszP2: POB it2
	  ODE jeden
	  £AD it2
	  SOM koniecP2
	  POB nr2
	  WYP 2
	  SOB wypiszP2	

koniecP2: POB P2counter
	  ODE jeden
          £AD P2counter
	  SOZ koniec			
          PZS
          MSK MASKA2
          PWR
         
P3: CZM MASKA3
    MAS 3
    DNS
    POB wypisanieP3
    £AD it3

wypiszP3: POB it3
	  ODE jeden
	  £AD it3
	  SOM koniecP3
	  POB nr3
	  WYP 2
	  SOB wypiszP3			
			
koniecP3: POB P3counter
	  ODE jeden
	  £AD P3counter
	  SOZ koniec			
          PZS
          MSK MASKA3
          PWR
			
P4: CZM MASKA4
    MAS 1
    DNS	
    POB wypisanieP4
    £AD it4

wypiszP4: POB it4
	  ODE jeden
	  £AD it4
	  SOM koniecP4
	  POB nr4
	  WYP 2
	  SOB wypiszP4
			
koniecP4: POB P4counter
	  ODE jeden
	  £AD P4counter
	  SOZ koniec			
          PZS
          MSK MASKA4
          PWR			

i: RPA
it1: RPA
it2: RPA
it3: RPA
it4: RPA
MASKA1: RPA
MASKA2: RPA
MASKA3: RPA
MASKA4: RPA
P1counter: RPA
P2counter: RPA
P3counter: RPA
P4counter: RPA
wypisanieP1: RPA
wypisanieP2: RPA
wypisanieP3: RPA
wypisanieP4: RPA
hasztaq: RST 35
zero: RST 0
jeden: RST 1
dwa: RST 2
trzy: RST 3
cztery: RST 4
szesc: RST 6
osiem: RST 8
nr1: RST 49
nr2: RST 50
nr3: RST 51
nr4: RST 52