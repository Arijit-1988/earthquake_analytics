#import the libraries
import json
import requests
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine
import pymysql

#open a URL connection to the event feed & read all of the data
url='https://earthquake.usgs.gov/fdsnws/event/1/application.json'
uh = requests.get(url)
data = uh.json()

#Flatten out the required elements using pandas
df = pd.io.json.json_normalize(data)
dfcat=pd.DataFrame(list(df['catalogs'].apply(pd.Series).stack()),columns = ['catalogs'])
dfcont=pd.DataFrame(list(df['contributors'].apply(pd.Series).stack()),columns = ['contributors'])
dfprod=pd.DataFrame(list(df['producttypes'].apply(pd.Series).stack()),columns = ['producttypes'])
dfevnt=pd.DataFrame(list(df['eventtypes'].apply(pd.Series).stack()),columns = ['eventtypes'])
dfmag=pd.DataFrame(list(df['magnitudetypes'].apply(pd.Series).stack()),columns = ['magnitudetypes'])

#connect to MySQL database & Dump Data Frames into Tables
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",pw="user",db="usgs"))
dfcat.to_sql(con=engine, name='stg_catalogs_dim', if_exists='append')
dfcont.to_sql(con=engine, name='stg_contributors_dim', if_exists='append')
dfprod.to_sql(con=engine, name='stg_producttypes_dim', if_exists='append')
dfevnt.to_sql(con=engine, name='stg_eventtypes_dim', if_exists='append')
dfmag.to_sql(con=engine, name='stg_magnitudetypes_dim', if_exists='append')