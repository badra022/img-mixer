
# # summarize shape of the pixel array
# print(type(image))
# print(image.shape)
# signal=rfft(image)
# amb=np.abs(signal)
# ang=np.angle(signal)
# real=np.real(signal)
# img=np.imag(signal)
# print(real)
# print(type(signal))
# finalimage=irfft(signal)
# # display the array of pixels as an image
# pyplot.imshow(finalimage)
# pyplot.show()

from matplotlib import image
from matplotlib import pyplot                                                                              
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, irfft
import cmath

# load image as pixel array
image1 = image.imread('photo1.jpeg')
image2 = image.imread('photo2.jpeg')
# make a 1-dimensional view of arr
image1 = image1.ravel()
# make a 1-dimensional view of arr
image2 = image2.ravel()

print("for image1: ")
print(type(image1))
print(image1.shape)
print("for image2: ")
print(type(image2))
print(image2.shape)

# getting fft of the signal and subtracting amplitudes and phases (1)
rfft_coeff1 = rfft(image1)
rfft_coeff2 = rfft(image2)
signal_rfft_Coeff_abs1 = np.abs(rfft_coeff1)
signal_rfft_Coeff_angle1 = np.angle(rfft_coeff1)

# getting fft of the signal and subtracting amplitudes and phases (2)
signal_rfft_Coeff_abs2 = np.abs(rfft_coeff2)
signal_rfft_Coeff_angle2 = np.angle(rfft_coeff2)

# constructing fft coefficients again (from amplitudes and phases) after processing the amplitudes
new_rfft_coeff1 = np.zeros((len(rfft_coeff1),), dtype=complex)
for pixel in range(len(rfft_coeff1)):
    try:
        new_rfft_coeff1[pixel]= signal_rfft_Coeff_abs2[pixel]*cmath.exp(1j * signal_rfft_Coeff_angle2[pixel])
    except:
        pass

# constructing the new signal from the fft coeffs by inverse fft
new_image1 = irfft(new_rfft_coeff1).reshape(433, 640, 3)
# display the array of pixels as an image
pyplot.imshow(new_image1)
pyplot.show()