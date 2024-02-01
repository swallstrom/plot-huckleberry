'''
Make a circular plot of my son's sleep over
'''


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

## Read in the csv data file as a pandas dataframe, and split off the sleep entries
df = pd.read_csv('Huckleberry_latest.csv')
s = df[df['Type'] == 'Sleep'].copy()

## Convert start dates/times and duration times to datetime objects
s['Start'] = pd.to_datetime(s['Start'])
s['End'] = pd.to_datetime(s['End'])

## Find date of first entry, and add a new colum with the number of days since then (dividing by "1 day" timedelta)
init_date = s['Start'].min().date()
s['N_days'] = ((s['Start'].dt.date - init_date)/np.timedelta64(1, 'D'))+50

## Add new columns with the start and end times converted into radians, assuming 24h makes a full circle (= 2*pi radians)
s['Start_rad'] = (s['Start'].dt.hour+s['Start'].dt.minute/60)*2*np.pi/24
s['End_rad'] = (s['End'].dt.hour+s['End'].dt.minute/60)*2*np.pi/24

## Assign different colors to different start locations (where the baby fell asleep)
sleepcolors = {'Worn or held':'mediumorchid', 'Co sleep':'lightcoral', 'Stroller':'limegreen', 'Nursing':'cornflowerblue', 'other':'darkgrey'}

## Create a figure with polar coordinates, and for each row in the data frame plot an arc between the start and end time, at a radius corresponding to N_days (plus 50 to make the inner part of the plot more visible)
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, polar=True)
for index, row in s.iterrows():
	## Get start location, explicitly converting to a string to deal with nans
	startloc = str(row['Start Location'])
	## Some entries have multiple start locations, take only the first
	if ';' in startloc:
		startloc = startloc.split(';')[0]
	## If start location is not in the color dictionary above, call it other
	if startloc not in sleepcolors:
		startloc = 'other'
	## If the sleep entry spans across midnight, split it into two sections
	if row['Start_rad'] > row['End_rad']:
		ax.plot(np.linspace(row['Start_rad'], 2*np.pi, 30), np.ones(30)*row['N_days'], color=sleepcolors[startloc], linestyle='-', label=startloc)
		ax.plot(np.linspace(0, row['End_rad'], 30), np.ones(30)*row['N_days'], color=sleepcolors[startloc], linestyle='-', label=startloc)	
	else:
		ax.plot(np.linspace(row['Start_rad'], row['End_rad'], 30), np.ones(30)*row['N_days'], color=sleepcolors[startloc], linestyle='-', label=startloc)

## Polar plots as standard have theta starting on the right and increasing counterclockwise, so adjust it to instead start at the top and increase clockwise. Set the labels to be times instead of degrees
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi/2.0)
ax.set_xticks(np.linspace(0, 2*np.pi, 9))
ax.set_xticklabels(['00', ' ', '06', '09', '12', '15', '18', ' 21', '00'])

## Turn off the radial axis ticks, and the grid
ax.set_rticks([])
ax.grid(False)

## Remove duplicate labels and plot the legend, moving it to slightly outside the plot
handles, labels = plt.gca().get_legend_handles_labels()
labels, ids = np.unique(labels, return_index=True)
handles = [handles[i] for i in ids]
plt.legend(handles, labels, fontsize=8, loc='lower left', bbox_to_anchor=(.5 + np.cos(np.pi/4)/2, .5 + np.sin(np.pi/4)/2))

## Set a title, save figure as .png image and plot
plt.title("My son's sleep from age 2 months (center) to 1 year")
plt.savefig('sleep.pdf', bbox_inches='tight')
plt.show()


