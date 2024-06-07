import struct
import os
import random
import sys
import zlib


def SieveOfEratosthenes(n):
    prime = [True for i in range(n + 1)]
    prime_good = []
    p = 2
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1
    for p in range(2, n + 1):
        if prime[p]:
            prime_good.append(p)
    return prime_good

first_primes_list = SieveOfEratosthenes(20)
def nBitRandom(n):
    return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)


def getLowLevelPrime(n):
    while True:
        prime_candidate = nBitRandom(n)
        for dzielnik in first_primes_list:
            if prime_candidate % dzielnik == 0:
                break
        else:
            return prime_candidate


def isMillerRabinPassed(miller_rabin_candidate):
    maxDivisionByTwo = 0
    evenComponent = miller_rabin_candidate - 1
    while evenComponent % 2 == 0:
        evenComponent >>= 1
        maxDivisionByTwo += 1
    assert (2 ** maxDivisionByTwo * evenComponent == miller_rabin_candidate - 1)

    def trialComposite(round_tester):
        if pow(round_tester, evenComponent, miller_rabin_candidate) == 1:
            return False
        for i in range(maxDivisionByTwo):
            if pow(round_tester, 2 ** i * evenComponent, miller_rabin_candidate) == miller_rabin_candidate - 1:
                return False
        return True

    numberOfRabinTrials = 128
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, miller_rabin_candidate)
        if trialComposite(round_tester):
            return False
    return True


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
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
    offset = 8  # sygnatura o rozmiarze 8 bitów
    while offset < len(file_content):
        chunk_length = struct.unpack('!I', file_content[offset:offset + 4])[0]
        chunk_type = file_content[offset + 4:offset + 8]
        chunk_data = file_content[offset + 8:offset + 8 + chunk_length]
        chunk_crc = file_content[offset + 8 + chunk_length:offset + 12 + chunk_length]
        chunks.append((chunk_type, chunk_data, chunk_crc))
        offset += 12 + chunk_length
    return chunks


def szyfrowanie_danych(data, public_key):
    e, n = public_key
    zaszyfrowane_dane = b''
    blok_danych = 10  # aby szyfrowało paczkami

    for i in range(0, len(data), blok_danych):
        block = data[i:i + blok_danych]
        block_int = int.from_bytes(block, 'big')
        zaszyfrowane_dane_int = pow(block_int, e, n)
        zaszyfrowany_blok = zaszyfrowane_dane_int.to_bytes((zaszyfrowane_dane_int.bit_length() + 7) // 8, 'big')
        zaszyfrowane_dane += zaszyfrowany_blok
    return zaszyfrowane_dane


def tworzenie_zaszyfrowanego_png(signature, zaszyfrowane_chunki, path_zapis):
    with open(path_zapis, 'wb') as f:
        f.write(signature)
        for chunk in zaszyfrowane_chunki:
            chunk_type, chunk_data, chunk_crc = chunk
            f.write(struct.pack('!I', len(chunk_data)))
            f.write(chunk_type)
            f.write(chunk_data)
            f.write(chunk_crc)


def deszyfrowanie_danych(data, private_key):
    d, n = private_key
    odszyfrowane_dane = b''
    blok_danych = 10  # aby szyfrowało paczkami

    for i in range(0, len(data), blok_danych):
        block = data[i:i + blok_danych]
        block_int = int.from_bytes(block, 'big')
        odszyfrowane_dane_int = pow(block_int, d, n)
        odszyfrowany_blok = odszyfrowane_dane_int.to_bytes((odszyfrowane_dane_int.bit_length() + 7) // 8, 'big')
        odszyfrowane_dane += odszyfrowany_blok
    return odszyfrowane_dane


def decrypt_png_file(signature, chunks, private_key, output_file_path):
    odszyfrowane_chunki = []
    for chunk in chunks:
        chunk_type, chunk_data, chunk_crc = chunk
        if chunk_type == b'IDAT':
            odszyfrowane_dane = deszyfrowanie_danych(chunk_data, private_key)
            crc_input = chunk_type + odszyfrowane_dane
            new_crc = zlib.crc32(crc_input) & 0xffffffff
            odszyfrowane_chunki.append((chunk_type, odszyfrowane_dane, struct.pack('!I', new_crc)))
        else:
            odszyfrowane_chunki.append(chunk)
    tworzenie_zaszyfrowanego_png(signature, odszyfrowane_chunki, output_file_path)


def main(args):
    first_primes_list = SieveOfEratosthenes(350)

    p = q = 0
    while True:
        prime_candidate = getLowLevelPrime(100)
        if isMillerRabinPassed(prime_candidate):
            p = prime_candidate
            break

    while True:
        prime_candidate = getLowLevelPrime(100)
        if isMillerRabinPassed(prime_candidate):
            q = prime_candidate
            break

    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g, _, _ = extended_gcd(e, phi)
    while g != 1:
        e = random.randrange(2, phi)
        g, _, _ = extended_gcd(e, phi)

    d = mod_inverse(e, phi)
    print(f"Public key: ({e}, {n})")
    print(f"Private key: ({d}, {n})")

    public_key = (e, n)
    private_key = (d, n)

    folder = "zdjecia"
    path = os.path.join(folder, args[1])

    file_content = read_png_file(path)
    signature = file_content[:8]
    chunks = parse_chunks(file_content)

    print(f"Data chunks before encryption:")
    for chunk in chunks:
        print(chunk[0], len(chunk[1]), chunk[1][:10])  # Print first 10 bytes for verification

    zaszyfrowane_chunki = []
    for chunk in chunks:
        chunk_type, chunk_data, chunk_crc = chunk
        if chunk_type == b'IDAT':
            zaszyfrowane_dane = szyfrowanie_danych(chunk_data, public_key)
            crc_input = chunk_type + zaszyfrowane_dane
            new_crc = zlib.crc32(crc_input) & 0xffffffff
            zaszyfrowane_chunki.append((chunk_type, zaszyfrowane_dane, struct.pack('!I', new_crc)))
        else:
            zaszyfrowane_chunki.append(chunk)

    print(f"Data chunks after encryption:")
    for chunk in zaszyfrowane_chunki:
        print(chunk[0], len(chunk[1]), chunk[1][:10])  # Print first 10 bytes for verification

    path_RSA_png_save = os.path.join('zaszyfrowane', 'dice_RSA.png')
    os.makedirs('zaszyfrowane', exist_ok=True)
    tworzenie_zaszyfrowanego_png(signature, zaszyfrowane_chunki, path_RSA_png_save)

    print("Encrypted file created:", path_RSA_png_save)

    decrypt_output_path = os.path.join('odszyfrowane', 'dice_RSA_decrypted.png')
    os.makedirs('odszyfrowane', exist_ok=True)
    decrypt_png_file(signature, zaszyfrowane_chunki, private_key, decrypt_output_path)

    print("Decrypted file created:", decrypt_output_path)

    odszyfrowane_file_content = read_png_file(decrypt_output_path)
    odszyfrowane_chunks = parse_chunks(odszyfrowane_file_content)

    print(f"Data chunks after decryption:")
    for chunk in odszyfrowane_chunks:
        print(chunk[0], len(chunk[1]), chunk[1][:10])  # Print first 10 bytes for verification


if __name__ == "__main__":
    main(sys.argv)


