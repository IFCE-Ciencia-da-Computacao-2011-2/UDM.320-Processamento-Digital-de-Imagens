import numpy as np
import cv2

from areas_claras_detector import AreasClarasDetector
from areas_vermelhas_detector import AreasVermelhasDetector


class RuasDetector(object):

    def mediana(self, imagem, janela=9):
        return cv2.medianBlur(imagem, janela)
        
    def limiarizar(self, imagem, limiar_minimo, limiar_maximo):
        lower = np.array(limiar_minimo, dtype="uint8")
        upper = np.array(limiar_maximo, dtype="uint8")
        
        return cv2.inRange(imagem, lower, upper) != 0

    def processar_imagem(self, imagem, limiar_minimo=None, limiar_maximo=None):
        if limiar_minimo is None:
            limiar_minimo = (80, 80, 80)
        
        if limiar_maximo is None:
            limiar_maximo = (158, 153, 135)

        imagem_mediana = self.mediana(np.asarray(imagem))
        imagem_limiarizada = self.limiarizar(imagem_mediana, limiar_minimo, limiar_maximo)

        detector = AreasVermelhasDetector()
        
        imagem_detectada = imagem_limiarizada & ~detector.processar_imagem_casa(imagem)
        imagem_detectada = imagem_detectada   & ~detector.processar_imagem_terra_2(imagem)
        
        detector = AreasClarasDetector()
        imagem_detectada = imagem_detectada   & ~detector.processar_imagem(np.asarray(imagem))
        
        return imagem_detectada