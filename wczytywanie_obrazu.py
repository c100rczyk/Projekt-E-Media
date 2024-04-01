import struct
from fft import spectrum
from anonimizacja import new_image_without_adds
import sys
import os

def IHDR(chunk_data, chunk_type, length, crc):    
    width, height, bit_depth, color_type, compression, filter_type, interlace = struct.unpack('>IIBBBBB', chunk_data)
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")
    print(f"Width: {width} Height: {height} Bit depth: {bit_depth} Color type: {color_type} Compression: {compression} Filter type: {filter_type} Interlace: {interlace}")
    print("Crc:", crc)

def PLTE(chunk_data, chunk_type, length, crc):
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")
    palette_size = length // 3  
    palette = []
    for _ in range(palette_size):
        rgb = struct.unpack('BBB', chunk_data[:3])
        chunk_data = chunk_data[3:]
        palette.append(rgb)

    for i, rgb in enumerate(palette):
        print(f"Entry {i+1}: RGB{rgb}")
    print("Crc:", crc)

def cHRM(chunk_data, chunk_type, length, crc):
    values = struct.unpack('>8I', chunk_data[:32])

    white_point_x = values[0] / 100000
    white_point_y = values[1] / 100000
    white_point_z = 1 - white_point_x - white_point_y

    red_point_x = values[2] / 100000
    red_point_y = values[3] / 100000
    red_point_z = 1 - red_point_x - red_point_y

    green_point_x = values[4] / 100000
    green_point_y = values[5] / 100000
    green_point_z = 1 - green_point_x - green_point_y

    blue_point_x = values[6] / 100000
    blue_point_y = values[7] / 100000
    blue_point_z = 1 - blue_point_x - blue_point_y
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")

    print(f"White point:\n"
          f"x: {white_point_x}"
          f" y: {white_point_y}"
          f" z: {white_point_z}")

    print(f"Red point:\n"
          f"x: {red_point_x}"
          f" y: {red_point_y}"
          f" z: {red_point_z}")

    print(f"Green point:\n"
          f"x: {green_point_x}"
          f" y: {green_point_y}"
          f" z: {green_point_z}")

    print(f"Blue point:\n"
          f"x: {blue_point_x}"
          f" y: {blue_point_y}"
          f" z: {blue_point_z}")
    print("Crc:", crc)

def gAMA(chunk_data, chunk_type, length, crc): 
    gamma_value = struct.unpack('>I', chunk_data)[0]
    if(gamma_value == 0):
        raise ValueError("Error: gamma value can not equal to 0")
    
    gamma = gamma_value / 100000
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")
    print(f"Gamma: {gamma:.5f}\n") 
    print("Crc:", crc)
        
def tIME(chunk_data, chunk_type, length, crc):
    year, month, day, hour, minute, second = struct.unpack('>HBBBBB', chunk_data)
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")
    print(f"Ostatnia modyfikacja: {year}/{month}/{day} {hour}:{minute}:{second}\n")
    print("Crc:", crc)
     
def iTxt_tEXt_zTXt(chunk_data, chunk_type, length, crc):
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    text = chunk_data.decode('utf-8')
    print("Data:")
    print(text)
    print("Crc:", crc)

def IDAT(chunk_data, chunk_type, length, crc):
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")
    print("Crc:", crc)

def IEND(chunk_data, chunk_type, length, crc):
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")
    print("Crc:", crc)

def main(args):
    folder = "zdjecia"
    path = ""
    anonim_path = ""

    if(args[2] == 'show'):
        path = os.path.join(folder, args[1])
    elif(args[2] == 'anonim'):
        path = os.path.join(folder, args[1])
        anonim_path = os.path.join(folder, "anonim_"+ args[1])
    else:
        raise ValueError("Dostepne mozliwosci: /interpreter plik.py image.png show   lub  /interpreter plik.py image.png anonim")

    if(args[2] == 'show'):
        chunk_types = [b'IHDR', b'PLTE', b'cHRM', b'gAMA', b'tIME', b'IDAT', b'IEND']
        textual_chunk_types = [b'iTXt', b'tEXt', b'zTXt']
        i = 1

        with open(path, "rb") as f:
            signature = f.read(8)

            if not signature.startswith(b'\x89PNG\r\n\x1a\n'):
                raise ValueError("It is not a PNG file.")
            else:
                while True:
                    length_bytes = f.read(4)    # 1 część chunku : 4 bajty długości (określa jak duża jest zawartość 3 części)
                    if len(length_bytes) != 4:
                        break
                    
                    length = struct.unpack('>I', length_bytes)[0]
                    chunk_type = f.read(4)      # 2 część chunku : 4 bajty typu (name)
                    chunk_data = f.read(length) # 3 część chunku : length bajtów zawartości data      
                    crc_bytes = f.read(4)       # 4 część chunku : 4 bajty 
                    crc_int = struct.unpack('>I', crc_bytes)[0]
                    crc_bytes = crc_int.to_bytes(4, byteorder='big') 
                    crc = ' '.join(f'{b:02x}' for b in crc_bytes)
                    
                    if chunk_type in chunk_types:
                        print(f"Chunk #{i}")
                        i += 1
                        if chunk_type == b'IHDR':
                            IHDR(chunk_data, chunk_type, length, crc)
                        elif chunk_type == b'PLTE':
                            PLTE(chunk_data, chunk_type, length, crc)
                        elif chunk_type == b'cHRM':
                            cHRM(chunk_data, chunk_type, length, crc)
                        elif chunk_type == b'gAMA':
                            gAMA(chunk_data, chunk_type, length, crc)
                        elif chunk_type == b'IDAT':
                            IDAT(chunk_data, chunk_type, length, crc)
                        elif chunk_type == b'IEND':
                            IEND(chunk_data, chunk_type, length, crc)
                        else: 
                            tIME(chunk_data, chunk_type, length, crc)
                        print("---------------------------------")

                    elif chunk_type in textual_chunk_types:
                        print(f"Chunk #{i}")
                        i += 1
                        iTxt_tEXt_zTXt(chunk_data, chunk_type, length, crc)   
                        print("---------------------------------")
        
        spectrum(path)
    if(args[2] == 'anonim'):
        new_image_without_adds(path, anonim_path)
    
#main()
if __name__ == "__main__":
    main(sys.argv)

# /bin/python3 wczytywanie_obrazu.py zdjęcie.png show/anonim



