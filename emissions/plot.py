"""
Plot.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
from numpy import arange

public_html = '/home/bje/public_html/'
nrows = 288 * 7

repen = pd.read_csv('re-pen.log', sep=',', parse_dates=True, index_col='Time')
repen = repen.tail(nrows)

ei = pd.read_csv('ei.log', sep=',', parse_dates=True, index_col='Time')
ei = ei.tail(nrows)

fig2, ax2 = plt.subplots(nrows=1, ncols=2)
fig2.set_size_inches(20, 8)
plt.subplots_adjust(wspace=0.2)
plt.suptitle('National Electricity Market 5-min renewable share and emissions intensity\n\nData sourced from AREMI and APVI')

repen.plot(ax=ax2[0])
ax2[0].set_ylabel("Renewable share (%)")
ax2[0].xaxis.set_major_locator(DayLocator())
ax2[0].xaxis.set_minor_locator(HourLocator(arange(0, 25, 12)))
ax2[0].xaxis.set_minor_formatter(DateFormatter("%p"))
ax2[0].xaxis.set_major_formatter(DateFormatter('%Y-%m-%d   '))

ei.plot(ax=ax2[1])
ax2[1].set_ylabel("Emissions intensity (t CO2/MWh)")
ax2[1].xaxis.set_major_locator(DayLocator())
ax2[1].xaxis.set_minor_locator(HourLocator(arange(0, 25, 12)))
ax2[1].xaxis.set_minor_formatter(DateFormatter("%p"))
ax2[1].xaxis.set_major_formatter(DateFormatter('%Y-%m-%d   '))

plt.savefig(public_html + 'nem.png')
