from bigquery_writer.bigclient import OurClient
#from dotenv import dotenv_values
from agency_analytics.aa_client import Client
from datetime import datetime, timedelta
import os
import json
from google.cloud import pubsub_v1
import base64

def write_keywords(campaign, day_span, aa_client, bigquery_client):
    end_date = datetime.today()
    start_date = end_date - timedelta(days = day_span)
    return aa_client.write_keyword_rankings_list(bigquery_client.insert_keyword_rankings,campaign, start_date, end_date)
    
def wipe_yesterday_data():
    yesterday = datetime.today() - timedelta(days = 1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    bigquery = OurClient(os.getenv('PROJECT_ID'), os.getenv('DATASET'))
    bigquery.delete_keyword_rankings_with_date(yesterday)

def publish_campaign(campaign):
    publisher = pubsub_v1.PublisherClient()
    PROJECT_ID = os.getenv('PROJECT_ID')
    campaign_json = json.dumps({
        'data': campaign,
    })
    campaign_bytes = campaign_json.encode('utf-8')
    TOPIC_NAME = os.getenv('TOPIC_NAME')
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    try:
        publish_future = publisher.publish(topic_path, data=campaign_bytes)
        publish_future.result()  # Verify the publish succeeded
        return 'Message published.'
    except Exception as e:
        return e

def isint(some_string):
    try: 
        int(some_string)
    except ValueError:
        return False
    else:
        return True

def get_keywords(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    data = base64.b64decode(event['data']).decode('utf-8')
    bigquery = OurClient(os.getenv('PROJECT_ID'), os.getenv('DATASET'))
    aa = Client(os.getenv('KEY'))
    day_span = 365
    if data == 'start':
        wipe_yesterday_data()
        campaigns_list = aa.get_campaigns_list(active_only=True)
        for campaign in campaigns_list:
            publish_campaign(campaign)
    elif isint(data):
        write_keywords(data, day_span, aa, bigquery)
    else: 
        return f'Unexpected Error. data: {data}'




