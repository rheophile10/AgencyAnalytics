from bigquery_writer.bigclient import OurClient
#from dotenv import dotenv_values
from agency_analytics.client.old_client import AgencyAnalytics
from datetime import datetime, timedelta
import os
import json
from google.cloud import pubsub_v1
import base64
import logging
import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


def write_keywords(campaign, day_span, aa_client: AgencyAnalytics, bigquery_client):
    end_date = datetime.today()
    start_date = end_date - timedelta(days = day_span)
    return aa_client.write_keyword_rankings_list(bigquery_client.insert_keyword_rankings,campaign, start_date, end_date)
    
def wipe_yesterday_data():
    yesterday = datetime.today() - timedelta(days = 1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    bigquery = OurClient(os.getenv('PROJECT_ID'), os.getenv('DATASET'))
    return bigquery.delete_keyword_rankings_with_date(yesterday)
    
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
    aa = AgencyAnalytics(os.getenv('KEY'))
    data = data if data == 'start' else json.loads(data)
    logging.warning(f'data = {data}')
    day_span = 365
    if data == 'start':
        logging.warning(f'start data: {data}')
        wipe_result = wipe_yesterday_data()
        logging.warning(f'wipe_result: {wipe_result}')
        campaigns_list = aa.get_campaigns_list(active_only=True)
        logging.warning(f'campaigns to publish: {len(campaigns_list)}')
        for campaign in campaigns_list:
            publish_campaign(campaign)
    elif 'campaign_id' not in data['data'].keys():
        logging.error(f'campaign_id not in {data.keys()}')
        return f'campaign_id not in {data.keys()}'
    elif isint(data['data']['campaign_id']):
        logging.warning(f'campaign data: {data}')
        write_result = write_keywords(data['data'], day_span, aa, bigquery)
        logging.warning(f'write result: {write_result}')
    else: 
        logging.error(f'Unexpected Error: {data} is not an integer or start')
        return f'Unexpected Error. data: {data}'




