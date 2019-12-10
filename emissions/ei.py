"""Report NEM emissions intensity using NGER data.

   Copyright (C) 2017 Ben Elliston <bje@air.net.au>
"""

import sys
import json
import argparse
import urllib2
import datetime
import pandas as pd
import numpy as np

ntndp = {'Broken Hill Gas Turbines': 0.93,
         'Eraring Power Station': 0.88,
         'Jeeralang "B" Power Station': 0.76,
         'Lonsdale Power Station': 1.04,
         'Swanbank E Gas Turbine': 0.36,
         'Tarong Power Station': 0.84,
         'Tarong North Power Station': 0.8,
         'Tamar Valley Combined Cycled Power Station': 0.37,
         'Tamar Valley Peaking  Power Station': 0.63,
         'Torrens Island Power Station "A"': 0.64,
         'Torrens Island Power Station "B"': 0.58,
         'Townsville Gas Turbine': 0.43,
         'Wivenhoe Power Station No. 2 Pump': 0,
         'Yarwun Power Station': 0.53}

access_token = 'INSERT-TOKEN-HERE'

argparser = argparse.ArgumentParser()
argparser.add_argument('-d', type=str, default='http://services.aremi.d61.io/aemo/v7/csv/all')
argparser.add_argument('-n', type=str, default='NGERS - Designated generation facility data 2015-16.csv')
argparser.add_argument('-p', type=str, default='http://pv-map.apvi.org.au/api/v1/data/today.json?access_token=%s' % access_token)
args = argparser.parse_args()


def apvi(url):
    """Fetch APVI data."""
    urlobj = urllib2.urlopen(url)
    data = json.load(urlobj)
    output = data['output'][-2]

    ts = pd.Timestamp(output['ts'])
    now = pd.Timestamp(pd.datetime.utcnow()).tz_localize('UTC')
    delta = pd.Timedelta(minutes=30)
    assert (now - ts) < delta, "APVI data is stale"
    return output


nger = pd.read_csv(args.n, sep=',')
dispatch = pd.read_csv(urllib2.urlopen(args.d), sep=',')
pvoutput = apvi(args.p)

print '%s,' % datetime.datetime.now().isoformat("T"),

for rgn in ['NSW1', 'QLD1', 'SA1', 'TAS1', 'VIC1', 'ALL']:
    emissions = 0
    if rgn == 'ALL':
        total_output = pvoutput['nsw'] + pvoutput['qld'] + pvoutput['sa'] + \
                       pvoutput['tas'] + pvoutput['vic']
    else:
        total_output = pvoutput[rgn.rstrip('1').lower()]

    dispatch2 = dispatch if rgn == 'ALL' else dispatch[dispatch['Region'] == rgn]
    for row in dispatch2.itertuples():
        station_name = row[1]
        output_mw = row[2]
        lat = row[-2]
        lon = row[-1]

        if np.isnan(output_mw) or output_mw < 1:
            continue
        else:
            total_output += output_mw

        if row[16] in ['Hydro', 'Wind', 'Biomass', 'Landfill / Biogas',
                       'Renewable/ Biomass / Waste', 'Solar', 'Landfill, Biogas', 'Landfill Gas']:
            continue

        if station_name in ntndp:
            intensity = ntndp[station_name]
        else:
            selected = nger[np.logical_and(np.isclose(nger['Latitude'], lat),
                                           np.isclose(nger['Longitude'], lon))]
            if not selected:
                print >>sys.stderr, 'Not matched', station_name, lat, lon
                continue
            elif len(selected) > 1:
                # Take average if there are multiple NGER records
                intensity = selected['Emission intensity (t/Mwh)'].mean()
            else:
                intensity = selected['Emission intensity (t/Mwh)'].iloc[0]

        emissions += output_mw * intensity
    print '%.3f,' % (emissions / total_output),
print
