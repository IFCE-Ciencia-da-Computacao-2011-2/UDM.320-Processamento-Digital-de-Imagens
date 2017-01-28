from abc import ABCMeta, abstractmethod

import cv2

from image_similarity.image_similarity_processor import ImageSimilarityProcessor
from image_similarity.color_similarity.color_similarity import RGBColorSimilarity, HSVColorSimilarity, CIELABColorSimilarity


class ColorSimilarityProcessor(ImageSimilarityProcessor, metaclass=ABCMeta):
    def __init__(self, table_means, ignore_color):
        """
        :param pd.Dataframe table_means: Images processed by ColorMeanProcessor().process()
        :param list[int] ignore_color: Color that wil be ignored
        """
        super().__init__()
        self.table_means = table_means
        self.ignore_color = ignore_color

    @abstractmethod
    def process(self, image_path, images_path=None):
        pass


class RGBColorSimilarityProcessor(ColorSimilarityProcessor):

    def process(self, image_path, images_path=None):
        image = cv2.imread(image_path)
        return RGBColorSimilarity().process(image, self.table_means, self.ignore_color)


class HSVColorSimilarityProcessor(ColorSimilarityProcessor):

    def process(self, image_path, images_path=None):
        image = cv2.imread(image_path)
        return HSVColorSimilarity().process(image, self.table_means, self.ignore_color)


class CIELABColorSimilarityProcessor(ColorSimilarityProcessor):

    def process(self, image_path, images_path=None):
        image = cv2.imread(image_path)
        return CIELABColorSimilarity().process(image, self.table_means, self.ignore_color)
