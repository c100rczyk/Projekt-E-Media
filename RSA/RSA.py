import numpy as np
import math 
import os
import random

path_to_png = "images/type_3.png"



# Generowanie dużych liczb pierwszych
'''
Trial division method:
Metoda testuje czy LICZBA jest podzielna przez jakąkolwiek liczbę całkkowitą mniejszą od   sqrt( LICZBA )
jeśli nie ma takiej liczby, to znaczy że LICZBA jest pierwsza.

'''

# losowanie dużej liczby int
number = 79

test_primaly = np.sqrt(number)

print(int(test_primaly))
podzielna = False

for i in range(2,int(test_primaly)):
    if(number / i == int(number/i)):
        podzielna = True
    
if(podzielna == False):
    print(f"Liczba {number} jest liczbą pierwszą")

if(podzielna == True):
    print(f"Liczba {number} nie jest liczbą pierwszą")


#____________________________________________________________
'''
OPIS
Poprzeni algorytm jest bardzo niewydajny i nie sprawdzimy nim czy wylosowana bardzo duża
liczba jest liczbą pierwszą.

aby znaleźć duże liczby pierwsze będziemy korzystać z metod które dają nam duże
prawdopodobieństwo znalezienia liczby pierwszej.

Mając dwie duże liczby pierwsze, p i q , obliczamy moduł RSA jako  n = p*q
Im większy rozmiar modułu, tym większy poziom bezpieczeństwa. 

Jeśli moduł ma rozmiar 2048 bitów
to generowane liczby muszą mieć długość 1024 bity.

'''
#___________________________________________________________
"""
JAK generujemy dużą liczbę pierwszą (o określonym rozmiarze bitowym):

1. Wybrać losową liczbę o zadanym rozmiarze bitowym
2. Sprawdzenie czy wybrana liczba nie jest podzielna przez kilka pierwszych liczb pierwszych (są wstępnie wygenerowane).
3. Zastosuj pewną liczbę iteracji (test pierwszości Rabina Millera) w oparciu o akcepltowalny poziom błędów
    w celu otrzymania liczby która prawdopodobnie jest liczbą pierwszą.

"""

"stworzenie listy ,,pierszych,, liczb pierwszych, począwszy od najmniejszych"
def SieveOfEratosthenes(n):
 
    # Create a boolean array
    # "prime[0..n]" and initialize
    #  all entries it as true.
    # A value in prime[i] will
    # finally be false if i is
    # Not a prime, else true.
    prime = [True for i in range(n+1)]
    prime_good = []
    p = 2
    while (p * p <= n):
 
        # If prime[p] is not
        # changed, then it is a prime
        if (prime[p] == True):
 
            # Update all multiples of p
            for i in range(p * p, n+1, p):
                prime[i] = False
        p += 1
 
    # Print all prime numbers
    for p in range(2, n+1):
        if prime[p]:
            print(p)
            prime_good.append(p)
    return prime_good
 
first_primes_list = SieveOfEratosthenes(20)
print(first_primes_list)



def nBitRandom(n):
    # Zwracam losową liczbę z zakresu (2**(n-1)+1  do 2**n - 1)    (będzie to dodatkowo liczba nieparzysta)
    return (random.randrange(2**(n-1)+1, 2**n-1))


"test podzielności niskiego poziomu"
def getLowLevelPrime(n):

    while True:
        prime_candidate = nBitRandom(n)

        for dzielnik in first_primes_list:
            if prime_candidate % dzielnik == 0:
                break
            else:
                return prime_candidate
    

#liczba pierwsza po testach niskiego poziomu
liczba_pierwsza = getLowLevelPrime(20)
print(liczba_pierwsza)
        

#______________________________________________________________________
"""
Testy wysokiego poziomu liczb pierwszych

"""
