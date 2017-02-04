# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2
import functions as fc
import matplotlib.pyplot as plt
from scipy import misc, ndimage
from scipy.stats import chisquare
from skimage import io, color, filters, exposure
from skimage.morphology import disk

#%% General Configuration  ################################

saveDesc=True # Set true to save the descriptor results 

MODELS = ["GRAY", "RGB", "HSV"]
M = 1

dir_ORIGINAL= "/home/iedo/Documentos/IFCE/8° semestre /PDI/Trabalho/PILL/"
dir_GRAY = "/home/iedo/Documentos/IFCE/8° semestre /PDI/Trabalho/M_GRAY/"
dir_RGB = "/home/iedo/Documentos/IFCE/8° semestre /PDI/Trabalho/M_RGB/"
dir_HSV = "/home/iedo/Documentos/IFCE/8° semestre /PDI/Trabalho/M_HSV/"

dir_ = [dir_GRAY, dir_RGB, dir_HSV]

#%% Read datasets ############################

nameImages = (os.listdir(dir_[M]))
nameImages.sort()

#%% Parte 1 - Separar por cor ############################
processAll = False

dir_results = "/home/iedo/Documentos/IFCE/8° semestre /PDI/Trabalho/Resultados01/"

dir_input_image = "/home/iedo/Documentos/IFCE/8° semestre /PDI/Trabalho/Entradas/00074-3020-11_PART_1_OF_1_CHAL10_SB_E01D703B.jpg"

numReturn = 20

opcATT = ['CORREL','CHISQR','INTERSECT','BHATTACHARYYA']

inputIMG = io.imread(dir_input_image) 

if not processAll:
    if M == 0:
        inputIMG = np.uint32(color.rgb2gray(inputIMG)*255)
    if M == 2:
        inputIMG = np.uint32(color.rgb2hsv(inputIMG)*255)

if processAll:
    ATT = {}
    ATT['GRAY'] = []
    ATT['RGB'] = [] 
    ATT['HSV'] = []
    
    for M in range(len(MODELS)):
        for name in nameImages:
            imgDataBase = io.imread(dir_[M]+name)
            
            if M == 0:
                ATT['GRAY'].append(fc.compareHist(inputIMG, imgDataBase))
            elif M == 1:
                ATT['RGB'].append(fc.compareHist(inputIMG, imgDataBase))
            else:
                ATT['HSV'].append(fc.compareHist(inputIMG, imgDataBase))

else:
    k = 0
    
    ATT = np.empty(shape = (len(nameImages)+1,len(opcATT)),dtype = np.float32)
    ATT[k] = (fc.compareHist(inputIMG, inputIMG))
        
    for name in nameImages:
        imgDataBase = io.imread(dir_[M]+name)
        print("Compare %s"%(name))
        
        if M == 0:
            ATT[k+1] = fc.compareHist(inputIMG, imgDataBase)
        elif M == 1:
            pass
        else:
            pass
        k = k+1 
        
#    print('Else')
if saveDesc:
    paramCORREL = fc.sortDescriptors(np.copy(ATT[:,0]),inputIMG, np.copy(nameImages), numReturn,1)
#    paramCHISQR = fc.sortDescriptors(ATT[:,1],inputIMG, np.copy(nameImages), numReturn,0)
#    paramINTERSECT = fc.sortDescriptors(ATT[:,2],inputIMG, np.copy(nameImages), numReturn,1)
#    paramBHATTACHARYYA = fc.sortDescriptors(ATT[:,3],inputIMG, np.copy(nameImages), numReturn,0)
    for name in paramCORREL:
        misc.imsave(dir_results+MODELS[M]+'/'+name,io.imread(dir_RGB+name))

#if saveDesc:
#     if (os.path.isfile(file_)):
#         os.remove(file_)
            
#        np.savetxt(file_, att, fmt="%f", delimiter=",")

    
#%% Parte 2 ############################


#img = ndimage.imread(dir_+nameImages[0], flatten=True)
#img = np.uint8(img[:,:,0]*0.3 + img[:,:,1]*0.59 + img[:,:,2]*0.11)
#misc.imshow(img)

#test = io.imread(dir_+nameImages[0])
#test = color.rgb2gray(test)
#test = color.rgb2hsv(test) 
#test[:,:,0] = 0
#misc.imshow(test)

#test = np.uint16(test*255)
#misc.imshow(test)
##plt.hist(test2.ravel(),bins=256,normed=True)

