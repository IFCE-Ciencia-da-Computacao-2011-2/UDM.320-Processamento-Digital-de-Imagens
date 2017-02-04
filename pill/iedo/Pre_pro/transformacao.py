# -*- coding: utf-8 -*-
import os
import cv2
#import numpy as np
#import matplotlib.pyplot as plt
from scipy import misc, ndimage
#from scipy.stats import chisquare
#from skimage.morphology import disk
from skimage import io, color, filters, exposure

dir_ = "/home/iedo/Documentos/IFCE/8° semestre /PDI/Trabalho/PILL/"
dir_results = "/home/iedo/Documentos/IFCE/8° semestre /PDI/Trabalho/"

MODELS = ["M_GRAY/", "M_RGB/", "M_HSV/"]
M = 2

nameImages = (os.listdir(dir_))
nameImages.sort()

for i in range(1):
    for img in nameImages:
        
        image = io.imread(dir_+img)
        
        if M == 0:
            imageGRAY = color.rgb2gray(image)
            misc.imsave(dir_results+MODELS[M]+img[:-4]+".png",imageGRAY)
        elif M == 1:
            misc.imsave(dir_results+MODELS[M]+img[:-4]+".png",image)
        else:
            imageHSV = color.rgb2hsv(image)
            misc.imsave(dir_results+MODELS[M]+img[:-4]+".png",imageHSV)