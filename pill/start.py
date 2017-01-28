import glob
import os.path

import pandas as pd

from pill.image_similarity import ColorMeanProcessor
from pill.image_similarity import RGBColorSimilarityProcessor, HSVColorSimilarityProcessor, CIELABColorSimilarityProcessor


class ImagesProcessorByColor(object):

    def __init__(self, images_path, ignore_color, results_path):
        self.images_path = images_path
        self.ignore_color = ignore_color
        self.results_path = results_path

        self.table_means = self.load_table_means()

    def load_table_means(self):
        path = self.results_path + "cache/table_means.csv"

        if not os.path.exists(path):
            table_means = ColorMeanProcessor().process(self.images_path, self.ignore_color)
            table_means.to_csv(path)
        else:
            table_means = pd.read_csv(path)

        return table_means

    def process(self, image_path):
        methods = [
            RGBColorSimilarityProcessor(self.table_means, self.ignore_color),
            HSVColorSimilarityProcessor(self.table_means, self.ignore_color),
            CIELABColorSimilarityProcessor(self.table_means, self.ignore_color),
        ]

        for method in methods:
            self._process(method, image_path)

    def _process(self, method, image_path):
        result_path = self.results_path + method.__class__.__name__ + ' - ' + image_path.split('/')[-1] + '.csv'
        print(result_path)

        result = method.process(image_path)

        result.to_csv(result_path)

if __name__ == '__main__':
    pilulas_path = glob.glob("PILL/*")
    cinza = [118, 118, 118]

    pilulas = [
        'PILL/00093-0147-01_PART_1_OF_1_CHAL10_SF_212990BC.jpg',  # ~ vermelho
        'PILL/00085-1322-01_PART_1_OF_1_CHAL10_SF_CF07E78F.jpg',  # ~ azul
        'PILL/00074-9189-90_PART_1_OF_1_CHAL10_SF_DF1DEFBF.jpg',  # ~ azul e amarelo
        'PILL/00093-0757-01_PART_1_OF_1_CHAL10_SB_AC2B561A.jpg',  # ~ verde
        'PILL/00093-0321-01_PART_1_OF_1_CHAL10_SB_902B486A.jpg',  # ~laranja'
    ]

    processador = ImagesProcessorByColor(pilulas_path, cinza, "resultados/")

    for pilula in pilulas:
        processador.process(pilula)
