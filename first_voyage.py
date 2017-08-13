from __future__ import print_function
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import getvar
from mpl_toolkits.basemap import Basemap







data = Dataset("/Users/sandeepvepuri/Downloads/wrfout_d01_2014-10-05_00_00_00.nc")

#get the sea level pressure
slp = getvar(data, "slp")

#print(data.variables)

print(slp)

