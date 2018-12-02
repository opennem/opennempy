from . import config
import requests
import simplejson
import pandas as pd
import datetime
import os
import logging

log = logging.getLogger()

data_dir = config.get("local_settings",'data_dir')
if not os.path.exists(os.path.join(data_dir,"power")):
	os.mkdir(os.path.join(data_dir,"power"))

def live_data(region="sa1"):
	#returns latest (live) data for a region (previous week)
	r = requests.get("http://data.opennem.org.au/power/{0}.json".format(region))	
	df = pd.concat([json_to_pd(data_set) for data_set in data_sets(r)], axis=1)
	return df
	
def historical_week(d1=datetime.datetime(2018,2,3), d2 = datetime.datetime(2018,5,2), region="sa1"):
	#yields historical data for a region, times d1 and d2
	dt_i = dt_to_weekstart(d1)
	while dt_i < d2:	
		yield load_week(dt_i, region=region)
		dt_i += datetime.timedelta(7)
		
def load_data(d1=datetime.datetime(2018,2,5), d2 = datetime.datetime(2018,2,6), region="sa1", split=True):	
	#list of data frames contain relevant weeks of data
	frame_list = [series for series in historical_week(d1=d1,d2=d2,region=region)]
	
	#concatinate into one dataframe
	df = pd.concat(frame_list)
	df.sort_index(inplace=True)
	
	#assert no duplicated index
	assert len(df.index) == len(set(df.index))

	#filter desired date range
	dx = df[(df.index>d1) & (df.index<=d2)].copy()

	if split:
		return split_df(dx)
	else:
		return dx
	
def split_df(df):
	#splits 30 minute data sets from 5 minute datasets
	_30min_series = ["PRICE", "TEMPERATURE", "ROOFTOP_SOLAR"]
	df_30 = pd.concat([df[series].dropna() for series in _30min_series], axis=1)	
	df.drop(_30min_series, inplace=True, axis=1)	
	return df, df_30
		
def load_week(dt_start, region='sa1'):	
	#loads data from local data dir (if available), or downloads and saves data
	filename = "{0}_{1}.csv".format(region,dt_start.strftime("%Y%m%d"))
	folder = "power"
	filepath = os.path.join(data_dir,"power",filename)

	if os.path.exists(filepath):
		log.info('reading cache: ' + filepath)
		df = pd.read_csv(filepath,index_col=0,parse_dates=[0])
	else:
		df = download_week(dt_start, region=region)
		if len(df): # don't save empty df
			df.to_csv(filepath)
	rows = len(df)
	msg = filename + ' contains ' + str(rows) + ' rows'
	if rows != 2016:
		log.error(msg)
	else:
		log.info(msg)
	return df

def download_week(dt_start, region='sa1'):
	#downloads a specfic week from a specific region
	iso_week = dt_to_isocal(dt_start)
	url = "http://data.opennem.org.au/power/history/5minute/{0}_{1}.json".format(region,iso_week)
	log.debug('fetching: ' + url)
	r = requests.get(url)
	log.info('got ' + str(len(r.content)) + 'bytes')
	log.info('repsonse code ' + str(r.status_code))
	if r.status_code == '404':
		log.error('that\'s a 404 on ' + url)
		return pd.DataFrame() # empty df
	try:
		m = merge_series(r)
	except Exception as err:
		log.error('failed merging:\n' + str(r.content))
		log.info(type(err))
		log.info(err)
		m = pd.DataFrame()
	return m

def merge_series(r):
	#merges list of series in a dataframe (recombines interchange and battery fields)
	df = pd.concat([json_to_pd(data_set) for data_set in data_sets(r)], axis=1)	
	merge_and_drop_ic(df)
	if ("BATTERY_CHARGING" in df) or ("BATTERY_DISCHARGING" in df):
		merge_and_drop_batt(df)	
	return standardised_columns(df)
	
def standardised_columns(df):
	#ensures data frames have standardised structure (useful for people opening/manipulating data with excel)
	fuel_tech = ["BIOMASS","BLACK_COAL", "BROWN_COAL", "DISTILLATE", "GAS_CCGT", "GAS_OCGT", "GAS_RECIP", "GAS_STEAM", "HYDRO", "PUMPS", "SOLAR", "WIND", "BATTERY"]
	for col in fuel_tech:
		if col not in df:
			df[col] = pd.np.nan
	col_order = ["DEMAND", "NETINTERCHANGE"] + sorted(fuel_tech) + ["PRICE", "TEMPERATURE", "ROOFTOP_SOLAR"]
	return df[col_order]
	
def merge_and_drop_ic(df):
	#recombines interconnector flow data
	df["NETINTERCHANGE"] = df[["EXPORTS", "IMPORTS"]].sum(axis=1)
	df.drop(["EXPORTS", "IMPORTS"], axis=1,inplace=True)	

def merge_and_drop_batt(df):
	#recombines battery data
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
	#convert iso_cal string to dtdata_sets
	return datetime.datetime.strptime(iso_cal,"%GW%V%u")		
	
def data_sets(r):
	#yields dataset from get request
	json = simplejson.loads(r.content)
	for data_set in json:
		yield data_set
	
def json_to_pd(data_set):
	#returns a pandas data series from JSON dataset
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
	#returns a dict of latest live data for all regions
	return {region: live_data(region) for region in ['nsw1', 'qld1', 'sa1','tas1','vic1']}	
