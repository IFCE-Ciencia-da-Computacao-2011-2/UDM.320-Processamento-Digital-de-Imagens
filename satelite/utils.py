from PIL import Image
import matplotlib.pyplot as plt

import skimage
from skimage import segmentation


def apply_mask(image, mask):
    r, g, b = image.split()
    r, g, b = r * ~mask, g * ~mask, b * ~mask
    r, g, b = Image.fromarray(r), Image.fromarray(g), Image.fromarray(b)
    
    return Image.merge("RGB", [r,g,b])


def skshow(image):
    """
    Returns a skimage as a PIL
    """
    return Image.fromarray(skimage.util.img_as_ubyte(image))

def marcar_areas(imagem, mascara, outline_color):
    """
    Demarca as áreas mascaradas com a outline_color
    """
    return segmentation.mark_boundaries(imagem, mascara, outline_color=outline_color)

class ImagemGrid(object):
    
    def show(self, *args, cmap=None, ratio=(1, 1)):
        """
        Recebe n tuplas contendo (imagem, titulo) e imprime-as lateralmente
        """
        total_imagens = len(args)

        f, subplots = plt.subplots(1, total_imagens, sharey=True, figsize=(4*total_imagens*ratio[0], total_imagens*ratio[1]))

        for subplot, imagem_legenda in zip(subplots, args):
            imagem, titulo = imagem_legenda
            
            subplot.set_title(titulo)
            subplot.imshow(imagem, cmap)