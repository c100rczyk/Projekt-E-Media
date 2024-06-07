import numpy as np
import math 
import os
import sys
import random
import struct

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
to generowane liczby muszą mieć długość 1024 bity (bo są dwie liczby 2*1024).

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

    # Stworzenie tablicy true/false
    # Wszystkie liczby pierwsze są true
    prime = [True for i in range(n+1)]
    prime_good = []
    p = 2   # 2 jest najmniejszą liczbą pierwszą
    while (p * p <= n):
 
        # If prime[p] is not
        # changed, then it is a prime
        if (prime[p] == True):
 
            # jeśli p jest liczbą pierwszą , ustawiamy wszystkie
            # jej wielokrotności jako nie pierwsze (False)
            for i in range(p * p, n+1, p):
                prime[i] = False    
        p += 1
 
    # wszystkie liczby pierwsze
    for p in range(2, n+1):
        if prime[p]:
            prime_good.append(p)
    return prime_good
 
first_primes_list = SieveOfEratosthenes(20)
# print(first_primes_list)



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
# liczba_pierwsza = getLowLevelPrime(20)
# print(liczba_pierwsza)
        

#______________________________________________________________________
"""
Testy wysokiego poziomu liczb pierwszych

Jeśli wprowadzona wartość przejdzie pojedynczą iterację Rabina Millera, prawdopodobieństwo że liczba 
jest pierwsza wynosi 75%.
"""


def isMillerRabinPassed(miller_rabin_candidate):
    "Uruchomienie 20 iteracji"
    maxDivisionByTwo = 0
    evenComponent = miller_rabin_candidate - 1

    while evenComponent % 2 == 0:
        evenComponent >>= 1
        maxDivisionByTwo += 1
    assert(2**maxDivisionByTwo * evenComponent == miller_rabin_candidate - 1)

    def trialComposite(round_tester):
        if pow(round_tester, evenComponent, miller_rabin_candidate) == 1:
            return False
        for i in range(maxDivisionByTwo):
            if pow(round_tester, 2**i * evenComponent, miller_rabin_candidate) == miller_rabin_candidate - 1:
                return False
        return True
    
    numberOfRabinTrials = 128            # błąd niepewności wynosi 1 / (2^20)

    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, miller_rabin_candidate)
        if trialComposite(round_tester):
            return False
    return True


#TWORZENIE KLUCZY______________________________________________________________________________________________

# Implementacja rozszerzonego algorytmu Eulidesa
def extended_gcd(a,b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b%a, a)

    x = y1 - (b//a)*x1
    y = x1
    return gcd,x,y

# obliczanie odwrotności multiplikatywnej
def mod_inverse(e,phi):
    gcd, x, _ = extended_gcd(e,phi)
    if gcd != 1:
        raise Exception("Odwrotność nie istnieje")
    else:
        return x % phi

def read_png_file(file_path):
    with open(file_path, 'rb') as f:
        file_content = f.read()
    return file_content

def parse_chunks(file_content):
    chunks = []
    offset = 8   # sygnatura o rozmiarze 8 bitów

    while offset < len(file_content):
        chunk_length = struct.unpack('!I', file_content[offset:offset+4])[0]
        chunk_type = file_content[offset+4:offset+8]
        chunk_data = file_content[offset+8:offset+8+chunk_length]
        chunk_crc = file_content[offset+8+chunk_length : offset+12+chunk_length]
        chunks.append((chunk_type, chunk_data, chunk_crc))
        offset += 12 + chunk_length
    return chunks

def szyfrowanie_danych(data, public_key):
    e,n = public_key
    zaszyfrowane_dane = b''
    blok_danych = 245   # aby szyfrowało paczkami

    for i in range(0, len(data), blok_danych):
        block = data[i:i+blok_danych]       #wiemy że dane są w foracie bitowym
        # Przerzucam bity na Inty aby zaszyfrować
        block_int = int.from_bytes(block, 'big')
        zaszyfrowane_dane_int = pow(block_int, e, n)
        # Przerzucam inty na bity żeby zapamiętać obraz bitowy (zaszyfrowany)
        zaszyfrowany_blok = zaszyfrowane_dane_int.to_bytes(zaszyfrowane_dane_int.bit_length() + 7 //8, 'big')
        zaszyfrowane_dane += zaszyfrowany_blok
    return zaszyfrowane_dane

def tworzenie_zaszyfrowanego_png(zaszyfrowane_chunki, path_zapis):
    with open(path_zapis, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        for chunk in zaszyfrowane_chunki:
            chunk_type,chunk_data,chunk_crc = chunk
            f.write(struct.pack('!I', len(chunk_data)))
            f.write(chunk_type)
            f.write(chunk_data)
            f.write(chunk_crc)





#MAIN_______________________________________________________________________________________________________________________
def main(args):
    p = 0
    q = 0

    while True: 
        first_primes_list = SieveOfEratosthenes(350)        #trochę liczb pierwszych
        n = 10    # liczba n-bitowa
        prime_candidate = getLowLevelPrime(n)

        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            p = prime_candidate
            break
    while True: 
        first_primes_list = SieveOfEratosthenes(350)        #trochę liczb pierwszych
        n = 10   # liczba n-bitowa
        prime_candidate = getLowLevelPrime(n)

        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            q = prime_candidate
            break


    print(n, "bit prime is: ", p)
    print(n, "bit prime is: ", q)

    # Generowanie klucza publicznego:
    n = p*q
    print(f"n: {n}")

    phi = (p-1)*(q-1)   # funkcja Eulera
    print(f"phi: {phi}")

    e = random.randrange(1, phi)

    g, _,_ = extended_gcd(e,phi)
    while g != 1:
        e = random.randrange(2,phi)
        g,_,_ = extended_gcd(e,phi)

    d = mod_inverse(e,phi)

    # Klucz publiczny (e,n) i klucz prywatny (d,n)
    print(f"klucz publiczny: ({e} ,\n {n})")
    print(f"klucz prywatny : ({d},\n {n})")


    #__________________TESTY____________________________
    # Proste Testy szyfrowania i deszyfrowania

    wiadomosc_tekstowa = 12
    print(f"prawdziwa wiadomość: {wiadomosc_tekstowa}")
    c = pow(wiadomosc_tekstowa,e,n)
    print(f"zaszyfrowana wiadomość: {c}")
    m = pow(c,d,n)
    print(f"Wiadomość po zdeszyfrowaniu: {m}")


    #_________________KLUCZE____________________
    public_key = (e,n)
    private_key = (d,n)


    #____________________POBIERANIE ZDJECIA PNG_______________________________
    folder = "zdjecia"
    path = ""
    path = os.path.join(folder, args[1])

    chunk_types = [b'IHDR', b'PLTE', b'cHRM', b'gAMA', b'tIME', b'IDAT', b'IEND']
    textual_chunk_types = [b'iTXt', b'tEXt', b'zTXt']


    file_content = read_png_file(path)
    chunks = parse_chunks(file_content)

    # chunks = []
    # with open(path, 'rb') as f:
    #     signature = f.read(8)
    #     print(signature)
    #
    #     if not signature.startswith(b'\x89PNG\r\n\x1a\n'):
    #         raise ValueError("It is not a PNG file.")
    #     else:
    #         while True:
    #             length_bytes = f.read(4)  # 1 część chunku : 4 bajty długości (określa jak duża jest zawartość 3 części)
    #             if len(length_bytes) != 4:
    #                 break
    #
    #             length = struct.unpack('>I', length_bytes)[0]
    #             chunk_type = f.read(4)  # 2 część chunku : 4 bajty typu (name)
    #             chunk_data = f.read(length)  # 3 część chunku : length bajtów zawartości data
    #             crc_bytes = f.read(4)  # 4 część chunku : 4 bajty
    #             crc_int = struct.unpack('>I', crc_bytes)[0]
    #             crc_bytes = crc_int.to_bytes(4, byteorder='big')
    #             crc = ' '.join(f'{b:02x}' for b in crc_bytes)
    #             chunks.append((chunk_type, chunk_data, crc_bytes))


    'każdy chunk ma swój type,data,crc'

    print(f"niezaszyfrowany IDAT")
    for chunk in chunks:
        print(chunk[0] , len(chunk[1]))
    # WYJSCIE : b'IHDR' 5
    #           b'IDAT' 226868
    #           b'IEND' 0


    # SZYFROWANIE IDAT:
    #chunk_type, chunk_plte ,chunk_data, chunk_crc = chunks

    zaszyfrowane_chunki = []

    for chunk in chunks:
        chunk_type,chunk_data, chunk_crc = chunk
        if chunk_type == b'IDAT':
            zaszyfrowane_dane = szyfrowanie_danych(chunk_data, private_key)
            zaszyfrowane_chunki.append((chunk_type,zaszyfrowane_dane, chunk_crc))
        else:
            zaszyfrowane_chunki.append(chunk)

    print(f"zaszyfrowany IDAT")
    for chunk in zaszyfrowane_chunki:
        print(chunk[0], len(chunk[1]))

    path_RSA_png_save = os.path.join('zaszyfrowane/type_3_RSA.png')    #, args[1])
    tworzenie_zaszyfrowanego_png(zaszyfrowane_chunki, path_RSA_png_save)






if __name__ == "__main__":
    main(sys.argv)




###_________ECB____intro_____________________
"""
Electronic Code Book : to szyfr blokowy. 

Szyfr blokowy to algorytm szyfrowania, który pobiera ustalone rozmiary danych wejściowych, 
np b-bitów i ponownie tworzy zaszyfrowany tekst składający się z b-bitów.

Wrzucamy dane do zaszyfrowania. Dane są dzielone na fragmenty (b-bitowe). Fragmenty są szyfrowane,
jesli jakiś fragment jest za duży to dzielony jest na mniejsze części.

ECB jest to szyfrowanie równoległe - szybkie szyfrowanie bloków danych.
ECB jest podatny na kryptoanalizę (ze względów na powiązanie tekstu z szyfrem).

















"""





