import pandas as pd
import numpy as np
import cv2
import math


class ColorMeanProcessor:
    """
    Given a set of paths, returns the mean color for each image, ignoring the specified color
    """
        
    def process(self, paths, ignore_color):
        """
        Given a set of paths, returns the average color for each image, ignoring the specified color
        """
        table = []
        
        for path in paths:
            image = cv2.imread(path)
            middle = math.ceil(image.shape[1]/2)

            rgb = self.color_mean(image, ignore_color)
            rgb_left = self.color_mean(image[:, middle], ignore_color)
            rgb_right = self.color_mean(image[:, middle:], ignore_color)

            line = [path]
            line.extend(rgb)
            line.extend(rgb_left)
            line.extend(rgb_right)

            table.append((path, rgb, rgb_left, rgb_right))

        return pd.DataFrame(
            table,
            columns=(
                'path',
                'mean_r', 'mean_g', 'mean_b',
                'mean_left_r', 'mean_left_g', 'mean_left_b',
                'mean_right_r', 'mean_right_g', 'mean_right_b'
            )
        )

    @staticmethod
    def color_mean(image_brg, ignore_color):
        """
        :param cv2.image image_brg:
        :param list[number] ignore_color: Format [B, G, R]

        :return list[number]: color_mean in format [mean r, mean r, mean b]
        """
        pixels_dataframe = pd.DataFrame(image_brg.reshape((-1, 3)), columns=['B', 'G', 'R'])

        mask = (pixels_dataframe.B == ignore_color[0]) \
             & (pixels_dataframe.G == ignore_color[1]) \
             & (pixels_dataframe.R == ignore_color[2])
        
        pixels_dataframe_masked = pixels_dataframe[~mask]

        return np.array(
            [
                int(pixels_dataframe_masked.R.mean()),
                int(pixels_dataframe_masked.G.mean()),
                int(pixels_dataframe_masked.B.mean()),
            ],
            dtype=np.uint8
        )
