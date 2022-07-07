#Project goal: take in data from youtube api (list of channels a youtube account is subscribed to) 
#print in the terminal a table with the channel names and 
import requests
import pprint
import json
import pandas as pd
import sqlalchemy as db
from sqlalchemy import create_engine 
import googleapiclient.discovery        
from googleapiclient.discovery import build



def data_to_dataframe(response):
  empty_list1 = []
  empty_list2 = []
  data_store = response['items']
  for data_access in data_store:
    subs_name = data_access['snippet']['title']
    subs_published = data_access['snippet']['publishedAt']
    empty_list1.append(subs_name)
    empty_list2.append(subs_published)
  subs_dataframe = pd.DataFrame(list(zip(empty_list1, empty_list2)),
               columns =['Channel Name', 'Date Published'])


#write function that puts dataframe into a database

def dataframe_to_database(subs_dataframe):
  engine = db.create_engine('sqlite:///subscriptions.db')
  subs_dataframe.to_sql('channels_info', con=engine, if_exists='replace', index=False)
  query_result = engine.execute("SELECT * FROM channels_info;").fetchall()
  print(pd.DataFrame(query_result))


api_key = 'AIzaSyCOvfykbh7rulikvgMYIBl83cgZNwiaOj4'
youtube = build('youtube', 'v3', developerKey=api_key)
request = youtube.subscriptions().list(
part='snippet',
channelId='UCkt0xYjL5NCoXsT6S2gobUA'
  )
response = requests.execute()
  

data_to_dataframe(response)
dataframe_to_database(subs_dataframe)
