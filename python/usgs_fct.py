#import the libraries
import json
import requests
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine
import pymysql

#open a URL connection to the event feed & read all of the data
url='https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2017-12-01&endtime=2017-12-31'
uh = requests.get(url)
data = uh.json()

#Flatten out the required elements using pandas
df = pd.io.json.json_normalize(data['features'])
df1 = df.drop('geometry.coordinates',axis=1)
df1.columns=['GeometryType','Id','PropertiesAlert','PropertiesCDI','PropertiesCode','PropertiesDetail','PropertiesDmin','PropertiesFelt','PropertiesGap','PropertiesIds','PropertiesMag','PropertiesMagType','PropertiesMmi','PropertiesNet','PropertiesNst','PropertiesPlace','PropertiesRms','PropertiesSig','PropertiesSources','PropertiesStatus','PropertiesTime','PropertiesTitle','PropertiesTsunami','PropertiesType','PropertiesTypes','PropertiesTz','PropertiesUpdated','PropertiesUrl','Type']
dfFinal=pd.concat([pd.DataFrame(list(df['geometry.coordinates']),columns = ['Latitude','Long','Depth']),df1],axis=1)

#connect to MySQL database
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",pw="user",db="usgs"))
dfFinal.to_sql(con=engine, name='stg_earthquake_fct', if_exists='append')