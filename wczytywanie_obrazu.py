import numpy as np
import os
import matplotlib.pyplot as plt
import struct
import subprocess
import logging


def IHDR(file_path):    
    with open(file_path, 'rb') as f:
        # wczytuję sygnaturę png
        signature = f.read(8)   # 8 pierwszych bajtów pliku PNG w celu sprawdzenia, czy plik jest zgodny z formatem PNG
        print(signature)
        if signature.startswith(b'\x89PNG\r\n\x1a\n'):
            print("Obraz PNG")
        else:
            raise ValueError("To nie jest plik PNG.")
        # Odczytanie kolejnych chunków i interpretacja informacji
        
        length_chunk = f.read(4)    #read() czyta kolejne x bajtów z pliku
        chunk_type = f.read(4)
        chunk_data = f.read(struct.unpack('>I', length_chunk)[0])
        

        if chunk_type == b'IHDR':
            width, height = struct.unpack('>II', chunk_data[:8])
            bit_depth, color_type, compression, filter_type, interlace = struct.unpack('BBBBB', chunk_data[8:])
            print("Szerokość:", width)
            print("Wysokość:", height)
            print("Głębia bitowa:", bit_depth)
            print("Rodzaj koloru:", color_type)
            print("metoda filtracji", filter_type)
            print("metoda splotu", interlace)


def PLTE(file_path):
    with open(file_path, "rb") as zdj:
        
        chunk_base = [0]*4
        chunk_base[0] = b'\x50'
        chunk_base[1] = b'\x4c'
        chunk_base[2] = b'\x54'
        chunk_base[3] = b'\x45'
        
        byte = zdj.read(1)
        while byte:
            print(byte)
            if byte == chunk_base[0]:
                byte = zdj.read(1)
                if byte == chunk_base[1]:
                    byte = zdj.read(1)
                    if byte == chunk_base[2]:
                        byte = zdj.read(1)
                        if byte == chunk_base[3]:
                            print("Wczytano PLTE")
                            break
            else:
                print("szukaj dalej")

            byte = zdj.read(1)
                            
        print(byte)
        #znaleziono PLTE. Teraz wczytujemy
        zdj.seek(-4,1)  #przesuniecie wskaźnika o 4 w lewo (z powrotem)
        chunk_plte = zdj.read(4)
        print(chunk_plte)
        
        chunk_length = struct.unpack('>I', chunk_plte)[0]  # rozpakować pierwsze 4 bajty

        if chunk_plte == b'PLTE':
            chunk_data = zdj.read(chunk_length)
            # każdy z 3 kolejnych bajtów zalicza się do koloru
            colors = [struct.unpack('BBB', chunk_data[i:i+3]) for i in range(0, len(chunk_data), 3)]
            print("Color palette:")
            for i, color in enumerate(colors):
                print(f"Color {i+1}: R={color[0]}, G={color[1]}, B={color[2]}")
            return

        




def load_picture(path):
    sunflower = plt.imread(path)
    plt.imshow(sunflower)
    plt.show()
    return sunflower


def main():
    path = "zdjecia/slonecznik.png"
    
    sunflower = load_picture(path)
    IHDR(path)
    
    #PLTE(path)

    


main()
