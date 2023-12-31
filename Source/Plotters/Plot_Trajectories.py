from Source.Base.BasePlotter import BasePlotter
from Source.Plotters.TrajDataHelper import TrajDataHelper

path = '/Data/'
filename = 'Binned_Initial_Condition_Grid_trunc1'
helper = TrajDataHelper(path, filename)
print("Loading to array....")
helper.LoadToArray()
helper.CreateDataFrame()
helper.AssignColumnNames()
# helper.FilterByOrbit(4)

print("plotting scatter plot")
plotter = BasePlotter(helper)
plotter.plotScatter(helper.p0, helper.p0_perp, "Initial Momentum", 10)
print("Done")

print("plotting scatter plot")
plotter = BasePlotter(helper)
plotter.plot2Scatter(helper.p0, helper.p0_perp, helper.pf, helper.pf_perp, \
                     "Initial Momentum", 10)
print("Done")
