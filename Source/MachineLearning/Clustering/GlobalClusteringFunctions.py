import random
import copy
import string
from numpy import void
from Source.Base.BasePlotter import BasePlotter
from Source.MachineLearning.Clustering.ClusteringHelper import ClusteringHelper


def CreateHelpersForOrbits(MLhelper: ClusteringHelper):
    MLHelpers = []
    for i in range(1, 5):
        MLhelperNew = copy.deepcopy(MLhelper)
        MLhelperNew.FilterByOrbit(i)
        MLhelperNew.DropColumns()
        MLhelperNew.path = MLhelperNew.path + str(i) + "/"
        MLHelpers.append(MLhelperNew)
    MLhelper.Truncate(int(MLhelper.my_data_frame.shape[0] / 4))  # approx 4 times the size of each filtered helper
    MLhelper.DropColumns()
    MLhelper.path = MLhelper.path + "All/"
    MLHelpers.insert(0, MLhelper)  # all orbits at index 0
    return MLHelpers


def LoopClusteringParams(MLhelper: ClusteringHelper, minSamples: int, maxSamples: int, minEps: float, maxEps: float,
                  minClusters: int, maxClusters: int, maxRange: int) -> list:
    helpers = []
    for i in range(1, maxRange):
        print("i = " + str(i) + " of " + str(maxRange))
        eps = random.randint(minEps * 100, maxEps * 100) / 100
        samples = random.randint(minSamples, maxSamples)
        helperCopy = copy.deepcopy(MLhelper)
        clusters = helperCopy.RunClustering(eps, samples)
        if clusters >= minClusters and clusters <= maxClusters:
            print("Cluster fits criteria ")
            helpers.append(helperCopy)
    return helpers


def PlotResults(helpers: list, orbit: string) -> void:
    for helper in helpers:
        plotter = BasePlotter(helper)
        plotter.plotScatter(helper.p0, helper.p0_perp, \
                        "Clustering - eps = " + str(helper.eps) + " Samples = " + str(helper.samples) + " " + orbit, 15, 0.5, True)
