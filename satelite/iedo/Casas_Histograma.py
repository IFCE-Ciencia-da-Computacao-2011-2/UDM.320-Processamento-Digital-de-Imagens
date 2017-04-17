
# coding: utf-8

# In[27]:


#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 22:05:34 2017

@author: iedo
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import misc, ndimage
from skimage import data
from skimage.filters import threshold_otsu, threshold_local
from skimage import io, color, filters, exposure
from skimage.restoration import denoise_bilateral
from skimage.morphology import dilation, binary_opening, binary_closing, binary_dilation, binary_erosion
from skimage.morphology import disk, square
import matplotlib.pyplot as plt
#import cv2
from scipy.ndimage import convolve


w     = 3       # bilateral filter half-width
sigma = [3, 30]  # bilateral filter standard deviations

#SRM_q = 25
SRM_qlev = 130

Phansalkar_r = 15 #less brings less nucleus material

minAreaCito = 2500
maxAreaCito = 8000
saveCyto    = True
saveVoronoi = True
saveNucleus = True 
limArea = 150 # In fiji implementation is called minSize.. %as in the training set will miss 8 nuc 
limEcc = 0.98


# In[28]:

satelite = io.imread('satelite.jpg')
satelite_gray =  color.rgb2gray(satelite)
satelite_hsv =  color.rgb2xyz(satelite)


# In[29]:

fig = plt.figure(figsize=(15, 15))

a=fig.add_subplot(1,2,1)
imgplot = plt.imshow(satelite)
a.set_title('Original')


a=fig.add_subplot(1,2,2)
imgplot = plt.imshow(satelite_hsv)
imgplot.set_clim(0.0,0.7)
a.set_title('HSV')

plt.show()


# In[30]:

diferenca = (satelite[:,:,0] - satelite[:,:,1])/255
diferenca_hsv = np.abs((satelite_hsv[:,:,1]-satelite_hsv[:,:,0]))

fig = plt.figure(figsize=(20, 20))

a=fig.add_subplot(2,2,1)
imgplot = plt.imshow(satelite, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('satelite')

a=fig.add_subplot(2,2,3)
imgplot = plt.imshow(diferenca, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('R - G')

a=fig.add_subplot(2,2,4)
imgplot = plt.imshow(diferenca_hsv, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('diferenca_hsv')


plt.show()
np.min(diferenca)


# In[31]:

hist, bins = exposure.histogram(diferenca)

fig = plt.figure(figsize=(15, 5))

a=fig.add_subplot(1,2,1)
imgplot = plt.plot(bins, hist, 'r--', linewidth=1)
#imgplot.set_clim(0.0,0.7)
a.set_title('Histograma Gray')

hist, bins = exposure.histogram(diferenca_hsv)

a=fig.add_subplot(1,2,2)
imgplot = imgplot = plt.plot(bins, hist, 'r--', linewidth=1)
#imgplot.set_clim(0.0,0.7)
a.set_title('Histograma com HSV')


plt.show()

aux = np.copy(diferenca)
aux[aux>=0.8] =0
#misc.imshow(aux)


# # RGB

# In[33]:

diferenca_denoise = denoise_bilateral(diferenca,w,sigma_color = sigma[0], sigma_spatial=sigma[1],bins = 256, multichannel=False) 

aux = np.copy(diferenca)
aux[aux>0.5] = 0
aux[aux<0.1] = 0
#aux = (aux.max()/4 > aux)



aux2 = np.asarray(satelite[:,:,0], dtype="int16") - satelite[:,:,1]
aux2 = (aux2 < 0)

IbfHE = exposure.equalize_adapthist(aux,clip_limit = 0.01, nbins=256)

fig = plt.figure(figsize=(20, 20))

a=fig.add_subplot(2,2,1)
imgplot = plt.imshow(satelite, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('Satelite')

a=fig.add_subplot(2,2,2)
imgplot = plt.imshow(aux2, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('Verde')

a=fig.add_subplot(2,2,3)
imgplot = plt.imshow(aux, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('Aux')

a=fig.add_subplot(2,2,4)
imgplot = plt.imshow(IbfHE, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('IbfHE')

print()
plt.show()


# # HSV

# In[108]:

#denoise_bilateral(diferenca_abs,w,sigma_color = sigma[0], sigma_spatial=sigma[1],bins = 256, multichannel=False) 

aux = np.copy(diferenca_hsv)
aux[aux>0.5] = 0
aux[aux<0.1] = 0
#aux = (aux.max()/4 > aux)

aux2 = np.copy(diferenca_hsv)
aux2 = (aux2.max()/4 > aux2)

IbfHE = exposure.equalize_adapthist(aux2,clip_limit = 0.01, nbins=256)

fig = plt.figure(figsize=(20, 20))

a=fig.add_subplot(2,2,1)
imgplot = plt.imshow(satelite, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('R- G')

a=fig.add_subplot(2,2,2)
imgplot = plt.imshow(aux2, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('Verde')

a=fig.add_subplot(2,2,3)
imgplot = plt.imshow(aux, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('Aux')

a=fig.add_subplot(2,2,4)
imgplot = plt.imshow(IbfHE, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('IbfHE')

print(IbfHE)
plt.show()


# In[34]:

IbfHE = np.uint8(IbfHE*255)
global_thresh = threshold_otsu(IbfHE)
binary_global = IbfHE > global_thresh

block_size = 35
adaptive_thresh = threshold_local(IbfHE, block_size, offset=10)
binary_adaptive = IbfHE < adaptive_thresh

fig = plt.figure(figsize=(20, 20))

a=fig.add_subplot(2,2,1)
imgplot = plt.imshow(binary_global, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('binary_global ')

a=fig.add_subplot(2,2,2)
imgplot = plt.imshow(binary_adaptive, cmap="gray")
imgplot.set_clim(0.0,0.7)
a.set_title('binary_adaptive')

binary_global = binary_dilation(binary_global,disk(5))

image = np.copy(satelite)
image[:,:,0] = image[:,:,0]*(binary_global*1)
image[:,:,1] = image[:,:,1]*(binary_global*1)
image[:,:,2] = image[:,:,2]*(binary_global*1)

a=fig.add_subplot(2,2,3)
imgplot = plt.imshow(image)
imgplot.set_clim(0.0,0.7)
a.set_title('Casa')

a=fig.add_subplot(2,2,4)
imgplot = plt.imshow(satelite)
imgplot.set_clim(0.0,0.7)
a.set_title('Satelite')

plt.show()



# In[112]:

misc.imshow(satelite_hsv[:,:,1]-satelite_hsv[:,:,0])


# In[87]:

print(binary_global)

