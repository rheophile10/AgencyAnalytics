from bigquery_writer.bigclient import OurClient
#from dotenv import dotenv_values
from agency_analytics.aa_client import Client
from datetime import datetime, timedelta
import requests
import os
import google.auth.transport.requests
import google.oauth2.id_token

def keywords_update(campaigns_list, day_span = 390):
    #config = dotenv_values(".env") 
    bigquery = OurClient(os.getenv('PROJECT_ID'), os.getenv('DATASET'))
    #aa = Client(config['KEY'])
    aa = Client(os.getenv('KEY'))
    if campaigns_list == []:
        #first call
        #bigquery.wipe_keyword_rankings_table()
        #bigquery._initialize_db_from_schemas(exist_ok=True)
        wipe_yesterday_data()
        campaigns_list = aa.get_campaigns_list(active_only=True)
        call_gcloud_fxn(campaigns_list, 365)
    else:
        #other calls
        campaign = campaigns_list.pop()
        end_date = datetime.today()
        start_date = end_date - timedelta(days = day_span)
        aa.write_keyword_rankings_list(bigquery.insert_keyword_rankings,campaign, start_date, end_date)
    return campaigns_list

def call_gcloud_fxn(campaigns_list, day_span):
    new_request_json = {'campaigns_list': campaigns_list, 'day_span': day_span}
    url = os.getenv('FXN_URL')
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, url)
    header = {'Authorization': f'Bearer {id_token}'}
    response = requests.post(url, data=new_request_json, headers=header)
    return f'new request status code: {response.status_code} and {len(campaigns_list)} campaigns to go'

def wipe_yesterday_data():
    yesterday = datetime.today() - timedelta(days = 1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    bigquery = OurClient(os.getenv('PROJECT_ID'), os.getenv('DATASET'))
    bigquery.delete_keyword_rankings_with_date(yesterday)
