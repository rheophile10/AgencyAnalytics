import asyncio
from bigquery_writer.bigclient import OurClient
#from dotenv import dotenv_values
from agency_analytics.aa_client import Client
from datetime import datetime, timedelta
import requests
import os
import google.auth.transport.requests
import google.oauth2.id_token
import json

def write_keywords(campaign, day_span, aa_client, bigquery_client):
    end_date = datetime.today()
    start_date = end_date - timedelta(days = day_span)
    aa_client.write_keyword_rankings_list(bigquery_client.insert_keyword_rankings,campaign, start_date, end_date)

async def call_gcloud_fxn(campaigns_list, day_span):
    new_request_json = json.dumps({'campaigns_list': campaigns_list, 'day_span': day_span})
    url = os.getenv('FXN_URL')
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, url)
    headers = {'Authorization': f'Bearer {id_token}', "Content-Type": "application/json"}
    response = requests.post(url, data=new_request_json, headers=headers)
    return response.status_code

def wipe_yesterday_data():
    yesterday = datetime.today() - timedelta(days = 1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    bigquery = OurClient(os.getenv('PROJECT_ID'), os.getenv('DATASET'))
    bigquery.delete_keyword_rankings_with_date(yesterday)

def get_keywords(request):
    """Updates keywords table in bigquery
    """
    request_json = request.get_json()
    campaigns_list = request_json['campaigns_list']
    day_span = request_json['day_span']
    bigquery = OurClient(os.getenv('PROJECT_ID'), os.getenv('DATASET'))
    aa = Client(os.getenv('KEY'))
    if campaigns_list == []:
        wipe_yesterday_data()
        campaigns_list = aa.get_campaigns_list(active_only=True)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [loop.create_task(call_gcloud_fxn([campaign], day_span)) for campaign in campaigns_list]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        return f'finished: campaigns_list length {len(campaigns_list)}'
    elif len(campaigns_list) == 1: 
        campaign = campaigns_list[0]
        return write_keywords(campaign, day_span, aa, bigquery)
    else:
        return 'unexpected error'





