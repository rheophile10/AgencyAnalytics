from bigquery_writer.bigclient import OurClient
#from dotenv import dotenv_values
from agency_analytics.aa_client import Client
from datetime import datetime, timedelta
import requests
import os

def keywords_update(campaigns_list, day_span = 390):
    #config = dotenv_values(".env") 
    bigquery = OurClient(os.getenv('PROJECT_ID'), os.getenv('DATASET'))
    #aa = Client(config['KEY'])
    aa = Client(os.getenv('KEY'))
    bigquery._initialize_db_from_schemas(exist_ok=True)
    if campaigns_list == []:
        #first call
        bigquery.wipe_keyword_rankings_table()
        campaigns_list = aa.get_campaigns_list(active_only=True)
    else:
        #other calls
        campaign = campaigns_list.pop()
        end_date = datetime.today()
        start_date = end_date - timedelta(days = day_span)
        aa.write_keyword_rankings_list(bigquery.insert_keyword_rankings,campaign, start_date, end_date)
    return campaigns_list

def call_gcloud_fxn(campaigns_list, day_span):
    new_request_json = {'campaigns_list': campaigns_list, 'day_span': day_span}
    url = 'fxn url'
    requests.post(url, data=new_request_json)