from . import config
import requests
import simplejson
import pandas as pd
import datetime
import os

data_dir = config.get("local_settings",'data_dir')

def load_latest_week(region="sa1"):
	r = requests.get("http://data.opennem.org.au/power/{0}.json".format(region))
	df = pd.concat([json_to_pd(data_set) for data_set in data_sets(r)], axis=1)
	return df
	
def load_historical_data(d1=datetime.datetime(2018,2,3), d2 = datetime.datetime(2018,5,2), region="sa1"):
	#convert 
	d1_isocal = dt_to_isocal(d1)	
	d2_isocal = dt_to_isocal(d2)
	print (d2_isocal)	
	print (isocal_to_dt(d2_isocal))
	
def load_week(dt_start, region='sa1'):	
	filename = "{0}_{1}.csv".format(region,dt_start.strftime("%Y%m%d"))
	filepath = os.path.join(data_dir,filename)
	if os.path.exists(filepath):	
		return pd.read_csv(filepath,index_col=0,parse_dates=[0])
	else:
		df = download_week(dt_start, region=region)
		df.to_csv(filepath)
		return df

def download_week(dt_start, region='sa1'):
	iso_week = dt_to_isocal(dt_start)
	url = "http://data.opennem.org.au/power/history/5minute/{0}_{1}.json".format(region,iso_week)
	r = requests.get(url)
	return 	pd.concat([json_to_pd(data_set) for data_set in data_sets(r)], axis=1)

def dt_to_weekstart(dt):
	#convert dt to datetime of start of week
	return dt - datetime.timedelta(dt.weekday())

def dt_to_isocal(dt):
	#convert dt to ISO calendar week start (year week only)
	y, w, d = dt.isocalendar()	
	return "{0}W{1:02d}".format(y,w)

def isocal_to_dt(iso_cal):
	#convert iso_cal string to dt
	return datetime.datetime.strptime(iso_cal,"%GW%V%u")		
	
def data_sets(r):
	json = simplejson.loads(r.content)
	for data_set in json:
		yield data_set
	
def json_to_pd(data_set):
	_type = data_set['type']
	_id = data_set['id']
	series =  data_set['history']
	if _type != 'power':
		name = _type.upper()	
	else:
		name = _id.split(".")[-2].upper()
	
	dt_i = datetime.datetime.strptime(series['start'],'%Y-%m-%dT%H:%M+1000') 
	dt_f = datetime.datetime.strptime(series['last'],'%Y-%m-%dT%H:%M+1000')
	interval = series['interval']		
	
	if interval[-1] == "m":
		interval += "in"
		
	index = pd.date_range(start=dt_i, end = dt_f, freq = interval)[1:]
	
	return pd.DataFrame(index=index, data = series['data'], columns=[name])

def load_all_regions():
	return {region: load_week(region) for region in ['nsw', 'qld', 'sa','tas','vic','nem']}
	
