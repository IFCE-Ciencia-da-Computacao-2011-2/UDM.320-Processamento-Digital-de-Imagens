import skimage
import cv2
import numpy as np


class AreasClarasDetector(object):
    
    def saturar(self, imagem, gain=100):
        """
        Ajuste de contraste
        Satura a imagem ajustanto o sigmoid ``O = 1/(1 + exp*(gain*(cutoff - I)))``
        """
        return skimage.exposure.adjust_sigmoid(imagem, gain=gain)

    def borrar(self, imagem, sigma=2):
        """
        Borra imagem com o filtro gaussiano
        """
        return skimage.filters.gaussian(imagem, sigma=sigma, multichannel=True)

    def limiarizar(self, imagem, limiar_minimo, limiar_maximo):
        lower = np.array([limiar_minimo, limiar_minimo, limiar_minimo])
        upper = np.array([limiar_maximo, limiar_maximo, limiar_maximo])
        
        return cv2.inRange(imagem, lower, upper)

    def processar_imagem(self, imagem):
        saturada = self.saturar(imagem)
        borrada = self.borrar(saturada)
        
        limiar_minimo = 150/255
        limiar_maximo = 1.1 # Aparentemente bugado: o valor máximo (branco) é > 1
        
        return self.limiarizar(borrada, limiar_minimo, limiar_maximo) == 255
