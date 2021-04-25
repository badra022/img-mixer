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
from scipy.fft import rfft, rfftfreq, irfft, fft2, ifft2
import cmath
from PIL import Image
import matplotlib.pyplot as plt

# load image as pixel array
image1 = image.imread('photo1.jpg')
image2 = image.imread('photo2.jpg')

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
signal_rfft_Coeff_real1 = np.real(rfft_coeff1)
signal_rfft_Coeff_img1 = np.imag(rfft_coeff1)



#print(signal_rfft_Coeff_real1)

#print(signal_rfft_Coeff_abs1)

# getting fft of the signal and subtracting amplitudes and phases (2)
signal_rfft_Coeff_abs2 = np.abs(rfft_coeff2)
signal_rfft_Coeff_angle2 = np.angle(rfft_coeff2)
signal_rfft_Coeff_real2 = np.real(rfft_coeff2)
signal_rfft_Coeff_img2 = np.imag(rfft_coeff2)
x,y,z=signal_rfft_Coeff_img2.shape

print(signal_rfft_Coeff_real2[10,3,1])


#print(signal_rfft_Coeff_abs2)
m=rfft_coeff1
b=1j
for i in range(x):
    for g in range (y):
        for k in range (z):
            m[i,g,k]= signal_rfft_Coeff_real1[i,g,k] + b* signal_rfft_Coeff_img2[i,g,k] 


# # # constructing fft coefficients again (from amplitudes and phases) after processing the amplitudes
new_rfft_coeff1 = rfft_coeff1
for i in range(x):
    for g in range (y):
        for k in range (z):
            new_rfft_coeff1[i,g,k]= signal_rfft_Coeff_abs2[i,g,k]*cmath.exp(1j * signal_rfft_Coeff_angle2[i,g,k])
   

# # constructing the new signal from the fft coeffs by inverse fft
new_image10 = Image.fromarray(irfft(rfft_coeff1), 'RGB')
# # display the array of pixels as an image
#pyplot.imshow(new_image1)
#pyplot.show()
#print()
plt.imshow(new_image10)
#print(type(newyf))
#finalimage=irfft(rfft_coeff1)
# display the array of pixels as an image
#pyplot.imshow(new_image1)
pyplot.show()

