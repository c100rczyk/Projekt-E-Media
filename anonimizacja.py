import struct


def new_image_without_adds(path, new_file_name):
    critical_chunks = [b'IHDR', b'PLTE', b'IDAT', b'IEND']

    with open(path , 'rb') as f:
        signature = f.read(8)

        if not signature.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError("It is not a PNG file")
        else:
            with open(new_file_name, 'wb') as new_image:
                new_image.write(signature)
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

                    if chunk_type in critical_chunks:
                        new_image.write(length_bytes)
                        new_image.write(chunk_type)
                        new_image.write(chunk_data)
                        new_image.write(crc_bytes)
                    
            

