from PIL import Image

def IHDR_PIL(file_path):

    # Wczytanie obrazu PNG
    image = Image.open(file_path)

    # Pobranie wszystkich metadanych
    metadata = image.info

    # Wyświetlenie wszystkich metadanych
    for key, value in metadata.items():
        print(f"{key}: {value}")
    print(image.mode)

def main():

    path = "zdjecia/slonecznik.png"
    IHDR_PIL(path)

main()