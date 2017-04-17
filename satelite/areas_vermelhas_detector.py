import numpy as np
from skimage import morphology
from skimage import measure

class AreasVermelhasDetector(object):
    
    def r_menos_g(self, pil_imagem):
        r, g, b = pil_imagem.split()
        r, g, b = np.asarray(r, dtype=np.int16), np.asarray(g, dtype=np.int16), np.asarray(b, dtype=np.int16)

        return (r - g)
    
    def processar_imagem_casa(self, imagem):
        r_menos_g = self.r_menos_g(imagem)

        return r_menos_g.max()/4 < r_menos_g
    
    def processar_imagem_terra(self, imagem):
        r_menos_g = self.r_menos_g(imagem)
        
        return (0 < r_menos_g) & ~self.processar_imagem_casa(imagem)
    
    def processar_imagem_terra_2(self, imagem, fechamento_regiao_casas=20, area_minima=100):
        possiveis_areas_de_terra = self.processar_imagem_terra(imagem)

        areas_de_casa = self.processar_imagem_casa(imagem)
        # Ignorar regiões de casas
        areas_de_casa_expandida = morphology.closing(areas_de_casa, morphology.disk(fechamento_regiao_casas))
        possiveis_areas_de_terra_2 = possiveis_areas_de_terra & ~areas_de_casa_expandida

        areas_de_terra_3_maiores_que_limiar = self._filtrar_grupos(possiveis_areas_de_terra_2, area_minima)
        # Pequena abertura para dar uma "uniformizada"
        return morphology.binary_opening(areas_de_terra_3_maiores_que_limiar, morphology.disk(5))

    def _filtrar_grupos(self, imagem, tamanho_pixels):
        labels = measure.label(imagem, connectivity=2)

        buffer = np.zeros(labels.shape, dtype=bool)

        for region in measure.regionprops(labels):
            if region.area > tamanho_pixels:
                buffer |= (labels[:, :] == region.label)

        return buffer
