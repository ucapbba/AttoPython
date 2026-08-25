import os
import string
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from Source.Base.BaseDataHelper import BaseDataHelper
import matplotlib
import seaborn as sns


class BasePlotter():
    """Generic base plotting functions"""
    def __init__(self, _helper: BaseDataHelper):
        self.helper = _helper

    def plotScatter(self, col1: string, col2: string, title="", fontsize=10, pointsize=0.001, save=False):
        df = self.helper.get_data_frame()
        dfOrbit = df[self.helper.orbit]
        Xarray = np.asarray(df[col1])
        Yarray = np.asarray(df[col2])
        fig, ax = plt.subplots()
        # fig.canvas.set_window_title(title + " plot")
        plt.title(title, fontsize=fontsize)
        plt.xlabel(col1, fontsize=fontsize)
        plt.ylabel(col2, fontsize=fontsize)
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        scatter = ax.scatter(Xarray, Yarray, c=dfOrbit, s=pointsize)
        legend1 = ax.legend(*scatter.legend_elements(),\
                            loc="upper left", title="Orbit")
        ax.add_artist(legend1)
        self.SaveOrShow(save, title)
        matplotlib.pyplot.close()

    def plot2Scatter(self, col1: string, col2: string, col3: string, col4: string, title="", fontsize=10, pointsize=0.001, save=False):
        df = self.helper.get_data_frame()
        Xarray = np.asarray(df[col1])
        Yarray = np.asarray(df[col2])
        X2array = np.asarray(df[col3])
        Y2array = np.asarray(df[col4])
        fig = plt.figure()
        # fig.canvas.set_window_title(title + " plot")
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        ax1.scatter(Xarray, Yarray, s=pointsize, color="purple")
        ax1.set(adjustable='box', aspect='equal')
        ax2.scatter(X2array, Y2array, s=pointsize, color="purple")
        ax2.set(adjustable='box', aspect='equal')
        # axis
        ax1.set_xlabel(col1, fontsize=fontsize)
        ax1.set_ylabel(col2, fontsize=fontsize)
        ax2.set_xlabel(col3, fontsize=fontsize)
        # ax2.set_ylabel(col4, fontsize=fontsize)
        self.SaveOrShow(save, title)

    def PlotColourMesh(self, title=""):
        font = {'family': 'serif',
                'weight': 'normal',
                'size': 10}
        matplotlib.rc('font', **font)  # increase all font size
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        XRESI = self.helper.x_resi
        YRESI = self.helper.y_resi
        ZRESI = self.helper.z_resi
        _min = self.helper.min
        _max = self.helper.max
        ax.pcolormesh(XRESI, YRESI, ZRESI, norm=LogNorm(vmin=_min, vmax=_max),\
                      rasterized=True, shading='gouraud')
        ax.set(title=title)
        plt.axis('off')
        plt.show()

    def plotSeaborn(self, title: string = "", save: bool = False) -> np.void:
        df = self.helper.get_data_frame()
        sns.color_palette("pastel")
        sns.pairplot(df, hue='orbit', kind="reg", plot_kws=dict(scatter_kws=dict(s=0.1)), height=1.5)
        self.SaveOrShow(save, title)

    def SaveOrShow(self, save: bool, title: string) -> np.void:
        if save is True:
            cwd = os.getcwd()
            outputDir = cwd + self.helper.path
            os.makedirs(outputDir, exist_ok=True)
            plt.savefig(outputDir + title + ".png")
        plt.show()
