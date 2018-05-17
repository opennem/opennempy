# opennempy
python based access to the openNEM platform for National Electricity Market Data http://opennem.org.au

* For the front end repository, see here: [opennem-fe](https://github.com/chienleng/opennem-fe)

This is a python3 package that requires `pandas`, `requests` and `simplejson`.  To use this package clone the repository and add the directory to your $PYTHONPATH  (or clone it to a directory that is in your python path).  

There are two main modules `web_api` and `sql_api` that access the data (via web or mysql database respectively), save the data local and return a `pandas` dataframe (or two dataframes).  The directory for saving data in should be needs to be saved in a file name `config.ini` (see `config_example.ini` to see the config requirements).

Here is a small example:
```
from opennempy import web_api
df_5, df_30 = web_api.load_data(d1=datetime.datetime(2018,3,4), 
                                d2 = datetime.datetime(2018,4,19), 
                                region='sa1')
```
This will download, save the data as a csv in the directed lists in the config file, and return two data frames (containing data at a 5 minute and 30 minute resolution respectively). A single data fram containing all the data can also be obtained (by specifing the kwarg `split=False`). 

See the [jupter notebook](https://github.com/dylanjmcconnell/opennempy/blob/master/example.ipynb) for simple use case. 

## OpenNEM: an open platform for National Electricity Market Data
The **OpenNEM project** aims to make the wealth of public **National Electricity Market (NEM)** data more accessible to a wider audience.

We hope that improved access will facilitate **better public understanding of the market, improve energy literacy** and help facilitate a more **informed national discussion** on Australia’s energy transition in the long term interests of consumers.

By providing a **clear** window on the data, we hope to address the information asymmetry between stakeholders and improve the productivity of those engaged in energy market discussions.

OpenNEM is a project of the [Energy Transition Hub](http://energy-transition-hub.org/).

Developed by:

* Dylan McConnell ([@dylanjmcconnell)](https://twitter.com/dylanjmcconnell)
* simon holmes à court ([@simonahac](https://twitter.com/simonahac))
* Steven Tan ([@chienleng](https://twitter.com/chienleng)) 

### License
OpenNEMpy is MIT licensed.
