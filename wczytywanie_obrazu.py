import struct

def IHDR(chunk_data, chunk_type, length):    
    width, height, bit_depth, color_type, compression, filter_type, interlace = struct.unpack('>IIBBBBB', chunk_data)
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")
    print(f"Width: {width} Height: {height} Bit depth: {bit_depth} Color type: {color_type} Compression: {compression} Filter type: {filter_type} Interlace: {interlace}")

def PLTE(chunk_data, chunk_type, length):
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

def cHRM(chunk_data, chunk_type, length):
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

def gAMA(chunk_data, chunk_type, length): 
    gamma_value = struct.unpack('>I', chunk_data)[0]
    if(gamma_value == 0):
        raise ValueError("Error: gamma value can not equal to 0")
    
    gamma = gamma_value / 100000
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")
    print(f"Gamma: {gamma:.5f}\n") 
        
def tIME(chunk_data, chunk_type, length):
    year, month, day, hour, minute, second = struct.unpack('>HBBBBB', chunk_data)
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")
    print(f"Ostatnia modyfikacja: {year}/{month}/{day} {hour}:{minute}:{second}\n")
     
def iTxt_tEXt_zTXt(chunk_data, chunk_type, length):
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    text = chunk_data.decode('utf-8')
    print("Data:")
    print(text)

def IDAT(chunk_data, chunk_type, length):
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")

def IEND(chunk_data, chunk_type, length):
    print("Length:", length)
    print("Type:", chunk_type.decode('utf-8'))
    print("Data:")

def main():
    path = "zdjecia/type_3.png"
    chunk_types = [b'IHDR', b'PLTE', b'cHRM', b'gAMA', b'tIME', b'IDAT', b'IEND']
    textual_chunk_types = [b'iTXt', b'tEXt', b'zTXt']
    i = 1

    with open(path, "rb") as f:
        signature = f.read(8)

        if not signature.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError("It is not a PNG file.")
        else:
            while True:
                length_bytes = f.read(4)
                if len(length_bytes) != 4:
                    break
                
                length = struct.unpack('>I', length_bytes)[0]
                chunk_type = f.read(4)
                chunk_data = f.read(length)
                
                if chunk_type in chunk_types:
                    print(f"Chunk #{i}")
                    i += 1
                    if chunk_type == b'IHDR':
                        IHDR(chunk_data, chunk_type, length)
                    elif chunk_type == b'PLTE':
                        PLTE(chunk_data, chunk_type, length, f)
                    elif chunk_type == b'cHRM':
                        cHRM(chunk_data, chunk_type, length)
                    elif chunk_type == b'gAMA':
                        gAMA(chunk_data, chunk_type, length)
                    elif chunk_type == b'IDAT':
                        IDAT(chunk_data, chunk_type, length)
                    elif chunk_type == b'IEND':
                        IEND(chunk_data, chunk_type, length)
                    else: 
                        tIME(chunk_data, chunk_type, length)
                    print("---------------------------------")

                elif chunk_type in textual_chunk_types:
                    print(f"Chunk #{i}")
                    i += 1
                    iTxt_tEXt_zTXt(chunk_data, chunk_type, length)   
                    print("---------------------------------")

                f.seek(4, 1)     

main()
