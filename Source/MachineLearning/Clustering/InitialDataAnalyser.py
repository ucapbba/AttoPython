import copy
from numpy import void
from Source.Base.BasePlotter import BasePlotter
from Source.MachineLearning.Clustering.ClusteringHelper import ClusteringHelper


def CreatePlotter(helper: ClusteringHelper, points, orbit) -> BasePlotter:
    newhelper = copy.deepcopy(helper)
    newhelper.truncate_array(points)
    newhelper.create_data_frame()
    newhelper.AssignColumnNames()
    newhelper.FilterByOrbit(orbit)
    newhelper.my_data_frame = newhelper.my_data_frame.drop(['rf', 'rf_perp', 'stability', 'guoy'], axis=1)
    plotter = BasePlotter(newhelper)
    return plotter


def InitialPlots(helper: ClusteringHelper, pairPoints: float, scatterPoints: float) -> void:
    helper.path = helper.path + "Initial/"
    for i in range(1, 5):
        print("plotting scatter for orbit " + str(i) + " with " + str(scatterPoints) + " points")
        plotter = CreatePlotter(helper, scatterPoints, i)
        plotter.plot2Scatter(helper.p0, helper.p0_perp, helper.pf, helper.pf_perp, \
                                "Initial Final scatter Orbit " + str(i), 10, 0.5, True)
        print("plotting pairs  for orbit " + str(i) + " with " + str(pairPoints) + " points")
        plotter = CreatePlotter(helper, pairPoints, i)
        plotter.plotSeaborn("pairPlot Orbit " + str(i), True)
