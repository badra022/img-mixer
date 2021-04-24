from matplotlib import image
from matplotlib import pyplot                                                                              
from scipy.fft import irfft , rfft, rfftfreq
import numpy as np 
  

# load image as pixel array
image = image.imread('photo1.png')
# summarize shape of the pixel array
print(type(image))
print(image.shape)
# display the array of pixels as an image
pyplot.imshow(image)
pyplot.show()

