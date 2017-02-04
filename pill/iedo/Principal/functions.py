# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy import misc, ndimage
from scipy.stats import chisquare
from skimage import io, color, filters, exposure
from skimage.morphology import disk

##########################################
# OBS: Na correlacao negativa
##########################################
def compareHist(inputIMG, img):
    
    H1,_ = np.histogram(inputIMG.ravel(), bins = 256,range=[0,256],normed=True)
    H2,_ = np.histogram(img.ravel(), bins = 256,range=[0,256],normed=True)
    
    H1 = np.float32(H1.reshape(256,1))
    H2 = np.float32(H2.reshape(256,1))
    
    CORREL = cv2.compareHist(H1, H2, cv2.cv.CV_COMP_CORREL)
    CHISQR = cv2.compareHist(H1, H2, cv2.cv.CV_COMP_CHISQR)
    INTERSECT = cv2.compareHist(H1, H2, cv2.cv.CV_COMP_INTERSECT)
    BHATTACHARYYA = cv2.compareHist(H1, H2, cv2.cv.CV_COMP_BHATTACHARYYA)
    
    return [np.abs(CORREL),CHISQR,INTERSECT,BHATTACHARYYA]

def sortDescriptors(ATT,inputIMG, nameImages, numReturn, ORD):
    
    for i in range(len(ATT)-1):
        for j in range(len(ATT)-1):
            
            if ATT[i+1]>=ATT[j+1]:
                auxATT = ATT[i+1]
                ATT[i+1] = ATT[j+1]
                ATT[j+1] = auxATT
                
                auxName = nameImages[i]
                nameImages[i] = nameImages[j]
                nameImages[j] = auxName

    if(ORD == 1):
        nameImages = nameImages[::-1]
        return nameImages[:numReturn]
    else:
        return nameImages[:numReturn]