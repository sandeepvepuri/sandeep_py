#####################################################################
#
# Tropical Cyclone Tracks (Python)
# Created by Jason W. Godwin (jgodwin@rsmas.miami.edu)
#
# Version: 1.0
# 
# Description: This program uses a CSV containing date and time in
# Unix Epoch format (column 1), latitude (column 2), longitude
# (column 3), min. central pressure (column 3), and max. sustained
# winds (column 4) to plot the tropical cyclone path and colour-coding
# each point according to the storm's Saffir-Simpson Scale category.
#
# Dependencies:
# Python: basemap, matplotlib, and numpy
# Files: cities.csv (contains the city locations that will plot on
# the map)
#
#####################################################################

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime as dt
import time
import sys

# specify csv_file path

################ EDIT THIS BLOCK ONLY! ###########################################

csv_file = '/Users/sandeepvepuri/Downloads/tc_track_v1_1/cities/wrfout_d01_2003-07-15_00-00-00.csv'		# CSV containing best track information
tc_name = 'Hud Hud'		# TC name (include the title "Hurricane" or "Tropical Storm"
tc_year = '2014'			# TC year
outfile_name = 'hudhud2014.png'	# what do you want to call the output file
use_map = 'full'			# what map to use (full, gulf, carib, east_coast)
grid ='on'				# lat/lon grid on or off?

# open new figure
fig = plt.figure(figsize=(11,8))

####################### Draw background map ######################################################

# setup Lambert conformal basemap
if use_map == 'full':
	print('Using Full Atlantic Basin Map')
	m = Basemap(width=10000000,height=7000000,projection='lcc',resolution='c',lat_0=25,lon_0=-50.)
	citycsv = 'cities/cities.csv'
elif use_map == 'gulf':
	print('Using Gulf of Mexico Map')
	m = Basemap(width=2000000,height=1600000,projection='lcc',resolution='c',lat_0=25, lon_0=-90.)
	citycsv = 'cities/gulf_cities.csv'
	lat_max = 32.0
	lat_min = 17.0
	lon_max = -100.0
	lon_min = -79.0
elif use_map == 'carib':
	print('Using Caribbean Map')
	m = Basemap(width=4000000,height=2500000,projection='lcc',resolution='c',lat_0=15, lon_0=-75.)
	citycsv = 'cities/carib_cities.csv'
	lat_max = 24.0 
	lat_min = 8.0
	lon_max = -89.0
	lon_min = -59.0
elif use_map == 'east_coast':
	print('Using East Coast Map')
	m = Basemap(width=4000000,height=3500000,projection='lcc',resolution='c',lat_0=32, lon_0=-65.)
	citycsv = 'cities/eastus_cities.csv'
	lat_max = 45.0 
	lat_min = 20.0
	lon_max = -82.0
	lon_min = -52.0
else:
	sys.exit('Please use either full, gulf, carib, or east_coast for your map!')

# draw the land-sea mask
print('Drawing map...')
m.drawlsmask(land_color='coral',ocean_color='aqua',lakes='True')

# draw various boundaries
m.drawstates(color='grey')
m.drawcountries(color='white')

# draw and label lat and lon grid
if grid == 'on':
	parallels = np.arange(-80.,81,10.)
	meridians = np.arange(10.,351.,20.)
	m.drawparallels(parallels,labels=[False,True,False,False],color='white')
	m.drawmeridians(meridians,labels=[False,False,False,True],color='white')

# add shaded relief background
m.bluemarble()

###################### Add cities ################################################################
print('Adding cities to map...')
cities = np.recfromcsv(citycsv, unpack=True, names=['city', 'clat', 'clon'], dtype=None)

for i in range(len(cities.city)):
	lon, lat = cities.clon[i], cities.clat[i]
	xpt, ypt = m(lon, lat)
	lonpt, latpt = m(xpt, ypt, inverse=True)
	m.plot(xpt, ypt, 'w+')
	if lon > lon_max and lon < lon_min and lat > lat_min and lat < lat_max:
		plt.text(xpt+50000,ypt+50000,cities.city[i],fontsize=6,color='White')

##################### Add storm ##################################################################
# unpack the storm CSV file
print('Plotting storm...')
tc = np.recfromcsv(csv_file, unpack=True, names=['times', 'tclat', 'tclon',
                       'tcpres', 'tcwind'], dtype=None)
# plot the best track
for j in range(len(tc.times)):
	lon, lat = tc.tclon[j], tc.tclat[j]
	xpt, ypt = m(lon, lat)
	lonpt, latpt = m(xpt, ypt, inverse=True)

	# convert winds from knots to mph
	tc.tcwind[j] = tc.tcwind[j] * 1.15155

	# color code points based on storm category
	if tc.tcwind[j] > 157:
		tccolor = 'mo'
	elif tc.tcwind[j] > 129:
		tccolor = 'ro'
	elif tc.tcwind[j] > 110:
		tccolor = 'yo'
	elif tc.tcwind[j] > 95:
		tccolor = 'go'
	elif tc.tcwind[j] > 73:
		tccolor = 'co'
	elif tc.tcwind[j] > 38:
		tccolor = 'bo'
	else:
		tccolor = 'wo'

	m.plot(xpt, ypt, tccolor)

	# plot date for 00 UTC positions
	if tc.times[j] % 1000 == 0:
		# convert epoch time to standard GMT time
		day = time.strftime('%m/%d', time.gmtime(tc.times[j]))
		if lon > lon_max and lon < lon_min and lat > lat_min and lat < lat_max:
			plt.text(xpt+50000,ypt,day,fontsize=6,color='Yellow')

# output image file

print('Creating image file...')

title = tc_name + ' (' + tc_year +')'
plt.title(title)
plt.savefig(outfile_name,orientation='landscape',bbox_inches='tight')

print('Great success!!!')
