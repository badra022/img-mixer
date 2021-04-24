from matplotlib import image
from matplotlib import pyplot                                                                              
from scipy.fft import irfft , rfft, rfftfreq
import numpy as np 
  

# load image as pixel array
image = image.imread('photo1.png')
# summarize shape of the pixel array
print(type(image))
print(image.shape)
signal=rfft(image)
print(type(signal))
finalimage=irfft(signal)
# display the array of pixels as an image
pyplot.imshow(finalimage)
pyplot.show()
