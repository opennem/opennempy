"""Instantaneous RE generation in the NEM."""

import json
import urllib2
import argparse
import datetime
import pandas as pd
import numpy as np

access_token = 'INSERT-TOKEN-HERE'

parser = argparse.ArgumentParser()
parser.add_argument('--url', type=str, default='http://services.aremi.d61.io/aemo/v7/csv/all')
parser.add_argument('-p', type=str, default='http://pv-map.apvi.org.au/api/v1/data/today.json?access_token=%s' % access_token)
args = parser.parse_args()

def apvi(url):
  urlobj = urllib2.urlopen(url)
  data = json.load(urlobj)
  output = data['output'][-2]

  ts = pd.Timestamp(output['ts'])
  now = pd.Timestamp(pd.datetime.utcnow()).tz_localize('UTC')
  delta = pd.Timedelta(minutes=30)
  assert (now - ts) < delta, "APVI data is stale"
  return output

print '%s,' % datetime.datetime.now().isoformat("T"),

df = pd.read_csv(urllib2.urlopen(args.url), sep=',')
pvoutput = apvi(args.p)

totalmw = {}
renewmw = {}

for region in ['NSW1', 'QLD1', 'SA1', 'TAS1', 'VIC1']:
    select = df[df['Region'] == region]
    totalmw[region] = select['Current Output (MW)'].sum()
    totalmw[region] += pvoutput[region.rstrip('1').lower()]

    remaining = select[~select['Technology Type - Primary'].isin(['Renewable', 'Wind', 'Combustion', np.nan])]
    if len(remaining) > 0:
        print 'WARNING: some generators not matched'
        print remaining

    renewables = select[select['Technology Type - Primary'] == 'Renewable']
    renewmw[region] = renewables['Current Output (MW)'].sum()
    renewmw[region] += pvoutput[region.rstrip('1').lower()]

    print '%4.1f,' % (renewmw[region] / totalmw[region] * 100),

# Exclude TAS1 from the totals as it is not AC-connected
total_renew = sum(renewmw.values()) - renewmw['TAS1']
total_ac_mw = sum(totalmw.values()) - totalmw['TAS1']
print '%4.1f' % (total_renew / total_ac_mw * 100)
