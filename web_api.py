from . import config
import requests
import simplejson
import pandas as pd
import datetime
import os

data_dir = config.get("local_settings",'data_dir')
live_url = "http://data.opennem.org.au/power/{0}.json"
history_url = "http://data.opennem.org.au/power/history/5minute/{0}_{1}.json"

def live_week(region="sa1"):
	r = requests.get(live_url.format(region))
	df = pd.concat([json_to_pd(data_set) for data_set in data_sets(r)], axis=1)
	return df
	
def historical_weeks(d1=datetime.datetime(2018,2,3), d2 = datetime.datetime(2018,5,2), region="sa1"):
	dt_i = dt_to_weekstart(d1)
	while dt_i < d2:	
		yield load_week(dt_i, region=region)
		dt_i += datetime.timedelta(7)
		
def load_data(d1=datetime.datetime(2018,2,5), d2 = datetime.datetime(2018,2,6), region="sa1", split=True):	
	series_list = [series for series in historical_weeks(d1=d1,d2=d2,region=region)]
	df = pd.concat(series_list)
	df.sort_index(inplace=True)
	
	#assert no duplicated index
	assert len(df.index) == len(set(df.index))

	dx = df[(df.index>d1) & (df.index<=d2)].copy()

	if split:
		return split_df(dx)
	else:
		return dx
	
def split_df(df):
	_30min_series = ["PRICE", "TEMPERATURE", "ROOFTOP_SOLAR"]
	df_30 = pd.concat([df[series].dropna() for series in _30min_series], axis=1)	
	df.drop(_30min_series, inplace=True, axis=1)	
	return df, df_30
		
def load_week(dt_start, region='sa1'):	
	filename = "{0}_{1}.csv".format(region,dt_start.strftime("%Y%m%d"))
	folder = "power"
	filepath = os.path.join(data_dir,"power",filename)
	if os.path.exists(filepath):	
		return pd.read_csv(filepath,index_col=0,parse_dates=[0])
	else:
		df = download_week(dt_start, region=region)
		df.to_csv(filepath)
		return df

def download_week(dt_start, region='sa1'):
	iso_week = dt_to_isocal(dt_start)
	url = history_url.format(region,iso_week)
	r = requests.get(url)
	return 	merge_series(r)
	
def merge_series(r):
	df = pd.concat([json_to_pd(data_set) for data_set in data_sets(r)], axis=1)	
	merge_and_drop_ic(df)
	if ("BATTERY_CHARGING" in df) or ("BATTERY_DISCHARGING" in df):
		merge_and_drop_batt(df)	
	return standardised_columns(df)

	
def standardised_columns(df):
	fuel_tech = ["BIOMASS","BLACK_COAL", "BROWN_COAL", "DISTILLATE", "GAS_CCGT", "GAS_OCGT", "GAS_RECIP", "GAS_STEAM", "HYDRO", "PUMPS", "SOLAR", "WIND", "BATTERY"]
	for col in fuel_tech:
		if col not in df:
			df[col] = pd.np.nan
	col_order = ["DEMAND", "NETINTERCHANGE"] + sorted(fuel_tech) + ["PRICE", "TEMPERATURE", "ROOFTOP_SOLAR"]
	return df[col_order]
	
def merge_and_drop_ic(df):
	df["NETINTERCHANGE"] = df[["EXPORTS", "IMPORTS"]].sum(axis=1)
	df.drop(["EXPORTS", "IMPORTS"], axis=1,inplace=True)	

def merge_and_drop_batt(df):
	df["BATTERY"] = df["BATTERY_DISCHARGING"] - df["BATTERY_CHARGING"]
	df.drop(["BATTERY_DISCHARGING", "BATTERY_CHARGING"], axis=1,inplace=True)	

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
	return {region: load_week(region) for region in ['nsw', 'qld', 'sa','tas','vic']}
	
