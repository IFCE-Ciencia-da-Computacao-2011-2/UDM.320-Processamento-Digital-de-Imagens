from abc import ABCMeta, abstractmethod
import colorsys
import math
from skimage import color as skimage_color


from .color_mean_processor import ColorMeanProcessor


class ColorSimilarity(metaclass=ABCMeta):
    """
    Compara por cor a similaridade das imagens.

    A imagem é dividida em duas partes (esquerda e direta).
    para cada imagem img_banco do banco de imagens:
        img_banco.distância = min(
            distancia_cor(imagem.left, img_banco.left)
            distancia_cor(imagem.left, img_banco.right)
            distancia_cor(imagem.right, img_banco.left)
            distancia_cor(imagem.right, img_banco.right)
        )

    A implementação de distancia_cor fica a cargo das classes filhas
    """
    def process(self, image_brg, table_mean, ignore_color):
        middle = math.ceil(image_brg.shape[1] / 2)

        color_mean_left = ColorMeanProcessor.color_mean(image_brg[:, middle], ignore_color)
        color_mean_right = ColorMeanProcessor.color_mean(image_brg[:, middle:], ignore_color)
        
        return self.similarity(table_mean, color_mean_left, color_mean_right)

    def similarity(self, table_mean, color_mean_left, color_mean_right):
        table = table_mean.copy()

        table['distance_left_left'] = self._distance_left(color_mean_left, table_mean)
        table['distance_left_right'] = self._distance_right(color_mean_left, table_mean)
        table['distance_right_left'] = self._distance_left(color_mean_right, table_mean)
        table['distance_right_right'] = self._distance_right(color_mean_right, table_mean)

        columns_distances = [
            'distance_left_left',
            'distance_left_right',
            'distance_right_left',
            'distance_right_right'
        ]
        function = lambda distances: min(distances)
        table['distance'] = table[columns_distances].apply(function, axis=1)

        columns = ['path', 'distance']
        return table[columns].sort_values(by='distance')

    def _distance_left(self, color_mean, table):
        columns_left_rgb = ['mean_left_r', 'mean_left_g', 'mean_left_b']
        function = lambda other_color_mean: self.distance_colors(color_mean, other_color_mean)

        return table[columns_left_rgb].apply(function, axis=1)

    def _distance_right(self, color_mean, table):
        columns_right_rgb = ['mean_right_r', 'mean_right_g', 'mean_right_b']
        function = lambda other_color_mean: self.distance_colors(color_mean, other_color_mean)

        return table[columns_right_rgb].apply(function, axis=1)

    @abstractmethod
    def distance_colors(self, color1, color2):
        pass


class RGBColorSimilarity(ColorSimilarity):

    def distance_colors(self, color_mean, other_color_mean):
        return math.sqrt(
            math.pow(color_mean[0] - other_color_mean[0], 2) +
            math.pow(color_mean[1] - other_color_mean[1], 2) +
            math.pow(color_mean[2] - other_color_mean[2], 2)
        )


class HSVColorSimilarity(ColorSimilarity):

    def distance_colors(self, color_mean, other_color_mean):
        color_hsv_mean = self.to_hsv(color_mean)
        other_color_hsv_mean = self.to_hsv(other_color_mean)

        return min(
            abs(color_hsv_mean[0] - other_color_hsv_mean[0]),
            1 - abs(color_hsv_mean[0] - other_color_hsv_mean[0])
        )

    def to_hsv(self, color):
        return colorsys.rgb_to_hsv(color[0]/256, color[1]/256, color[2]/256)


class CIELABColorSimilarity(ColorSimilarity):

    def distance_colors(self, color_mean, other_color_mean):
        color_lab_mean = self.to_lab(color_mean)
        other_color_lab_mean = self.to_lab(other_color_mean)

        return skimage_color.deltaE_cie76(color_lab_mean, other_color_lab_mean)

    def to_lab(self, color):
        rgb_image_color = [[[color[0]/255, color[1]/255, color[2]/255]]]

        lab_image_color = skimage_color.rgb2lab(rgb_image_color)
        return lab_image_color[0][0]

