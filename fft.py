import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft2, fftshift, ifft2
import cv2

def spectrum(file_path):

    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    fourier = fftshift(fft2(image))

    magnitude = np.abs(fourier)
    phase = np.angle(fourier)

    fourier_inverted = ifft2(fourier)

    plt.figure(figsize=(12, 6))

    plt.subplot(221)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')

    plt.subplot(222)
    plt.imshow(np.abs(fourier_inverted), cmap='gray')
    plt.title('Inverted Image')

    plt.subplot(223)
    plt.imshow(np.log(magnitude+1), cmap='gray')  
    plt.title('Magnitude')

    plt.subplot(224)
    plt.imshow(phase, cmap='gray')
    plt.title('Phase')

    plt.show()

        
