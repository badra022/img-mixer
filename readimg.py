from matplotlib import image
from matplotlib import pyplot as plt                                                                           
import numpy as np
from numpy.fft import ifft2, fft2, fftshift
import cmath

# load image as pixel array
image1 = image.imread('photo1.jpeg', 0)
image2 = image.imread('photo2.jpeg', 0)

# FT of the first image
f = fft2(image1)

# shifting FT matrix
fshift1 = fftshift(f)

# getting phase and magnitude spectrums
phase_spectrumA = np.angle(fshift1)
magnitude_spectrumA = 20*np.log(np.abs(fshift1))

# FT of the second image
f2 = fft2(image2)

# shifting FT matrix
fshift2 = fftshift(f2)

# getting phase and magnitude spectrums
phase_spectrumB = np.angle(fshift2)
magnitude_spectrumB = 20*np.log(np.abs(fshift2))

# combining phase, magnitude spectrums into output image 
# (YOU CAN EDIT HERE TO DECIDE WHAT TO COMBINE)
combined = np.multiply(np.abs(f2), np.exp(1j*np.angle(f)))

# getting the real pixel values of the output image in the spatial domain
imgCombined = np.real(ifft2(combined))

# rescaling the image to 0's and 1's
imgCombined = [ element/256 for element in imgCombined]

plt.imshow(imgCombined)
plt.show()