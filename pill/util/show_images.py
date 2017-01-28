import math

import cv2
import matplotlib.pyplot as plt
import numpy as np

from image_similarity.color_similarity.color_mean_processor import ColorMeanProcessor


def show(paths, title='', columns=10, split=20):
    """
    Show images in group of n, where n is specified in ``split`` param
    
    :param List[string] paths: Imagem paths
    :param string title: Graph
    :param number columns: Total image columns
    :param int split: Number of elements a group of images will display
    """
    total_images = len(paths)
    
    for x in range(0, total_images, split):
        first = x
        last = x+split if x+split < total_images else total_images
        
        page = '. \n{}-{} de {}'.format(first, last, total_images)
        
        _show(paths[x:x+split], columns=columns, title=title + page)


def _show(paths, columns=10, title=None):
    total_images = len(paths)
    columns = total_images if total_images < columns else columns

    lines = math.ceil(total_images/columns)
    f, subplots = plt.subplots(lines, columns, sharex='col', sharey='row', figsize=(columns, lines))
    f.suptitle(title)

    for path, subplot in zip(paths, subplots.flat):
        image = cv2.imread(filename=path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        subplot.imshow(image)
        subplot.axis('off')
        
        del image

    plt.show()


def show_image_color_mean(path, ignore_color):
    image = cv2.imread(path)
    color_mean = ColorMeanProcessor.color_mean(image, ignore_color)

    f, subplots = plt.subplots(1, 2)

    f.suptitle(path + ' ' + 'mean = ' + str(color_mean))

    subplots.flat[0].axis('off')
    subplots.flat[1].axis('off')
    subplots.flat[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), interpolation='none')
    subplots.flat[1].imshow([[np.array(color_mean, dtype=np.uint8)]], interpolation='none')

    plt.show()

    del image
