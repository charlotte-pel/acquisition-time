__author__ = 'Charlotte Pelletier'
_VERSION = '0.1'

import numpy as np
import pandas as pd

import datetime
from datetime import date
from dateutil.rrule import rrule, DAILY

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import colors

##############################
#  globals
##############################
STARTDATE = "20170101"
YYYY = int(STARTDATE[0:4])
month_names = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
monthday = [(date(YYYY,mm+1,1)-date(YYYY,mm,1)).days for mm in range(1,len(month_names))] #-- january to november
monthday.append((date(YYYY+1,1,1)-date(YYYY,len(month_names),1)).days) #-- december


##############################
#  date management
##############################
def read_datefile(datefile, start_date=STARTDATE):
	"""
		Read a datefile and store the doy into a list
		datefile format
			20170125
			20170130
			20170206
			...
			20171223
		Return
			25
			30
			...
			357
	"""
	with open(datefile) as f:
		content = f.readlines()
	content = [doa2doy(x.strip(), start_date=STARTDATE) for x in content]
	return content


def strdate2date(strdate):
	"""
		Convert a date saved in a string into a date object
		Supported format: "YYYYMMDD"
	"""	
	return date(int(strdate[0:4]), int(strdate[4:6]), int(strdate[6:8]))

def doa2doy(cur_date, start_date=STARTDATE):
	"""
		Return the doy of the cur_date using STARTDATE as a reference
	"""
	start = strdate2date(start_date)
	cur = strdate2date(cur_date)
	return cur.toordinal()-start.toordinal()+1
    
##############################
#  date management
##############################

#-- Color information
#https://matplotlib.org/3.1.0/gallery/color/named_colors.html

def draw_timeline(tile_doy, tile_names=None, interp_doy=None, pdfsave_file=None):
	
	
	if not isinstance(tile_doy[0], list): #-- not a list of list
		draw_singletile(tile_doy, tile_names, interp_doy, pdfsave_file)
	else:
		draw_multipletiles(tile_doy, tile_names, interp_doy, pdfsave_file)


def draw_singletile(tile_doy, tile_names=None, interp_doy=None, pdfsave_file=None):
	
	#-- global
	marker_size = 10
	monthbarsize = 0.025
	
	ndates = len(tile_doy)
	
	plt.figure(figsize=(6,1))
	ax = plt.gca()
	if tile_names is None:
		plt.scatter(tile_doy,ndates*[0],s=marker_size,zorder=1)
	else:
		plt.scatter(tile_doy,ndates*[0],s=marker_size,zorder=1,label=tile_names[i])

	xmin,xmax = plt.xlim()
	ymin,ymax = plt.ylim()
	
	# Arrow configuration
	hw = 1./2*(ymax-ymin) # arrow head width
	hl = 1./30.*(xmax-xmin) # arrow head length
	ohg = 0.3

	ax.arrow(xmin, 0, xmax-xmin+15, 0.,  color = mcolors.CSS4_COLORS['gray'], fc=mcolors.CSS4_COLORS['gray'], ec=mcolors.CSS4_COLORS['gray'],
		 lw = 1, head_width=hw, head_length=hl, overhang = ohg,
		 length_includes_head= True, clip_on = False,zorder=-1)
	ax.set_ylim([-0.05,0.15])
	min_doy = min(tile_doy)
	max_doy = max(tile_doy)
	plt.plot([0, 0], [-monthbarsize,monthbarsize], mcolors.CSS4_COLORS['orange']) #-- ~month bar [check]
	for idx, m in enumerate(month_names):
		if idx==0:
			xm = 4
		else:
			xm = np.cumsum(monthday)[idx-1]
		if xm<min_doy or xm>max_doy:
			continue
		plt.plot([np.cumsum(monthday)[idx], np.cumsum(monthday)[idx]], [-monthbarsize,monthbarsize], mcolors.CSS4_COLORS['orange']) #-- ~month bar [check]
		plt.annotate(m,(xm,0.05),xycoords='data', color = mcolors.CSS4_COLORS['orange'])

	#-- Dashed red lines for interpolated doy
	if not interp_doy is None:
		for dd in interp_doy:
			plt.plot([dd, dd], [0,(T-1)/T], 'r--', dashes=(5, 10), lw=0.5, zorder=-1)
	
	plt.xticks([])	
	plt.yticks([])
	plt.box(False)
	
	if not tile_names is None:
		plt.legend(bbox_to_anchor=(1.25, 1))
	if not pdfsave_file is None:
		plt.savefig(pdfsave_file,bbox_inches='tight')
	plt.show()		
		
def draw_multipletiles(tile_doy, tile_names=None, interp_doy=None, pdfsave_file=None):
	
	#-- global
	marker_size = 10
	
		
	T = len(tile_doy) # no. of tiles
	
	plt.figure(figsize=(6,1))
	ax = plt.gca()

	for i in range(T):
		ndates = len(tile_doy[i])
		yval = i/T
		if tile_names is None:
			plt.scatter(tile_doy[i],ndates*[yval],s=marker_size,zorder=1)
		else:
			plt.scatter(tile_doy[i],ndates*[yval],s=marker_size,zorder=1,label=tile_names[i])

	xmin,xmax = plt.xlim()
	ymin,ymax = plt.ylim()
	# Arrow configuration
	hw = 1./10.*(ymax-ymin) # arrow head width
	hl = 1./40.*(xmax-xmin) # arrow head length
	ohg = 0.3 # arrow overhang
	
	for i in range(T):
		yval = i/T
		ax.arrow(xmin, yval, xmax-xmin, 0.,  color = mcolors.CSS4_COLORS['gray'], fc=mcolors.CSS4_COLORS['gray'], ec=mcolors.CSS4_COLORS['gray'],
			 lw = 1, head_width=hw, head_length=hl, overhang = ohg,
			 length_includes_head= True, clip_on = False,zorder=-1)
	ax.set_ylim([-0.1,2/T+0.15])
	min_doy = min(min(tile_doy))
	max_doy = max(max(tile_doy))
	for idx, m in enumerate(month_names):
		if idx==0:
			xm = 4
		else:
			xm = np.cumsum(monthday)[idx-1]
		if xm<min_doy or xm>max_doy:
			continue
		#-- if month bar desired [check draw_singletile]
		plt.annotate(m, (xm,(T-1)/T+0.15),xycoords='data', color = mcolors.CSS4_COLORS['gray'])

	#-- Dashed red lines for interpolated doy
	if not interp_doy is None:
		for dd in interp_doy:
			plt.plot([dd, dd], [0,(T-1)/T], 'r--', dashes=(5, 10), lw=0.5, zorder=-1)
	
	#-- plt.xticks([])	##-- decomment to hide doy values in the x-axis
	plt.yticks([])
	plt.box(False)
	
	if not tile_names is None:
		plt.legend(bbox_to_anchor=(1.25, 1))
	if not pdfsave_file is None:
		plt.savefig(pdfsave_file,bbox_inches='tight')
	plt.show()



#EOF
