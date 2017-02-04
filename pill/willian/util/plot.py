import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl


def plot_cubo_rgb(elementos, title=''):
    cores = elementos[['r', 'g', 'b']].apply(lambda e: [e[0]/255, e[1]/255, e[2]/255], axis=1)

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(elementos['r'], elementos['g'], elementos['b'], c=cores)
    ax.set_title(title)

    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')

    plt.show()


def plot_h_bar(cores, title):
    plt.title(title)

    color_map = plt.cm.get_cmap('hsv')

    # Colored hist
    n, bins, patches = plt.hist(cores, bins=100, color='red', edgecolor="none")
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    col = bin_centers - min(bin_centers)  # scale values to interval [0,1]
    col /= max(col)
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', color_map(c))

    plt.ylabel("nº de imagens")

    # Axis bar
    ax1 = plt.axes([0.1225, 0, 0.778, 0.05])
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=color_map, norm=norm, orientation='horizontal')
    cb1.set_label('Hue - Ângulo na proporção $ângulo/360$')

    plt.show()

