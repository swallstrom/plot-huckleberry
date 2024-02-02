'''
Plot diapers over time, as total amount of pee and poo per day
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

## Read in the csv data file as a pandas dataframe, and split off the diaper entries
df = pd.read_csv('Huckleberry_latest_Y.csv')
s = df[df['Type'] == 'Diaper'].copy()

## Convert start dates/times to datetime objects, find date of first entry, and add a new colum with the number of days since then (dividing by "1 day" timedelta)
s['Start'] = pd.to_datetime(s['Start'])
init_date = s['Start'].min().date()
s['N_days'] = ((s['Start'].dt.date - init_date)/np.timedelta64(1, 'D'))

## The type of nappy is recorded in the column 'End Condition' (is that a pun?)
## Make new columns with how much pee and poo per nappy. Assume no listed size means medium. 
size = {'small':1, 'medium':2, 'large':4}
pee = []
poo = []
for index, row in s.iterrows():
	if row['End Condition'] == 'Dry':
		pee.append(0)
		poo.append(0)
	elif 'Both' in row['End Condition']:
		peesize = 'medium'
		poosize = 'medium'
		if 'ee' in row['End Condition']:
			peesize = row['End Condition'].split('ee')[1].split()[0].lstrip(':')
		if 'oo' in row['End Condition']:
			poosize = row['End Condition'].split('oo')[1].split()[0].lstrip(':')
		pee.append(size[peesize])
		poo.append(size[poosize])
	elif 'ee' in row['End Condition']:
		tmp = row['End Condition'].split(':')
		if len (tmp) == 1:
			pee.append(size['medium'])
		else:
			pee.append(size[tmp[1]])
		poo.append(0)
	elif 'oo' in row['End Condition']:
		tmp = row['End Condition'].split(':')
		if len (tmp) == 1:
			poo.append(size['medium'])
		else:
			poo.append(size[tmp[1]])
		pee.append(0)
	else:
		print('Anomalous entry detected: {} at {}'.format(row['End Condition'], row['Start']))

s['Pee amount'] = pee
s['Poo amount'] = poo

## For each day, sum up the amount of pee and poo
totpee = []
totpoo = []
for n in s['N_days'].unique():
	totpee.append(s.loc[s['N_days'] == n, 'Pee amount'].sum())
	totpoo.append(s.loc[s['N_days'] == n, 'Poo amount'].sum())


## Plot amount of pee and poo per day, and a rolling average over the last week for amount of pee
fig = plt.figure(figsize=(10,5))
plt.bar(np.linspace(s['N_days'].min(), s['N_days'].max(), len(totpee)), totpee, color='gold', label='Daily pee')
plt.plot(np.linspace(s['N_days'].min(), s['N_days'].max(), len(totpee)), pd.Series(totpee).rolling(7).mean(), 'kx', label='Rolling avg. pee')
plt.bar(np.linspace(s['N_days'].min(), s['N_days'].max(), len(totpoo)), totpoo, color='brown', label='Daily poo')
plt.legend()
plt.savefig('nappy_Y.pdf', bbox_inches='tight')
plt.show()

				

			