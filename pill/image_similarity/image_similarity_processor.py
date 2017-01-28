from abc import ABCMeta, abstractmethod


class ImageSimilarityProcessor(metaclass=ABCMeta):

    @abstractmethod
    def process(self, image_path, images_path):
        """
        Return images paths (of images_path) ordered by similarity with image_path

        :param string image_path: Image path basis
        :param string images_path: Images path
        :return pd.Dataframe: Images ordered by similarity with image_path
        """
        pass
