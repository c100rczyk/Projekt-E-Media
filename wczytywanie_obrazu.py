import numpy as np
import os
import matplotlib.pyplot as plt
import struct


# def read_png_header(file_path):
#     with open(file_path, 'rb') as f:
#         # Wczytanie sygnatury PNG
#         signature = f.read(8)

#         # Odczytanie kolejnych chunków i interpretacja informacji
#         while True:
#             length_chunk = f.read(4)
#             chunk_type = f.read(4)
#             chunk_data = f.read(struct.unpack('>I', length_chunk)[0])
#             crc = f.read(4)

#             if chunk_type == b'IHDR':
#                 width, height = struct.unpack('>II', chunk_data[:8])
#                 bit_depth, color_type, compression, filter_type, interlace = struct.unpack('BBBBB', chunk_data[8:])
#                 print("Szerokość:", width)
#                 print("Wysokość:", height)
#                 print("Głębia bitowa:", bit_depth)
#                 print("Rodzaj koloru:", color_type)
#                 # Możesz odczytać więcej informacji na temat innych pól, jeśli są potrzebne
#                 break

def read_png_metadata(file_path):    #dane zczytane z nagłówka zdjęcia
    with open(file_path, 'rb') as f:
        # wczytuję sygnaturę png
        signature = f.read(8)   # 8 pierwszych bajtów pliku PNG w celu sprawdzenia, czy plik jest zgodny z formatem PNG
        print(signature)
        if signature.startswith(b'\x89PNG\r\n\x1a\n'):
            print("Obraz PNG")
        else:
            raise ValueError("To nie jest plik PNG.")
        # Odczytanie kolejnych chunków i interpretacja informacji
        while True:
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
                # Możesz odczytać więcej informacji na temat innych pól, jeśli są potrzebne
                break


def load_picture(path):
    sunflower = plt.imread(path)
    plt.imshow(sunflower)
    plt.show()
    return sunflower


def main():
    path = "zdjecia/slonecznik.png"
    sunflower = load_picture(path)
    (height, width, color) = sunflower.shape    #zebranie metadanych
    read_png_metadata(path)

    


main()