import pytest
from dotenv import dotenv_values
from bigquery_writer.bigquery import OurClient

@pytest.fixture
def campaign_data():
  return [{
    "id": 42,
    "date_created": "2018-08-01 00:00:00",
    "date_modified": "2018-11-01 22:25:37",
    "date_deleted": None,
    "url": "http://test.com",
    "company": "test",
    "status": "active",
    "scope": "domain",
    "google_ignore_places": "false",
    "google_places_id": None,
    "google_cid": None,
    "google_mybusiness_id": None,
    "google_mybusiness_name": None,
    "group_title": None,
    "timezone": None,
    "account_id": 1
  }]

@pytest.fixture
def keywords_data():
  return [{
    "id": 123,
    "date_created": "2015-03-30 10:06:24",
    "date_modified": "2015-03-31 9:32:19",
    "keyword_phrase": "test keyword",
    "primary_keyword": "false",
    "campaign_id": 123
  }]

@pytest.fixture
def bigquery_client():
  config = dotenv_values(".env") 
  bigquery_client = OurClient(config['TEST_PROJECT_ID'], 'data')
  return bigquery_client

def test_insert_campaigns(bigquery_client, campaign_data):
  bigquery_client.insert_to_table('campaigns', campaign_data)
  #select from client
  #assert that what comes out is what went in

def test_insert_keywords(bigquery_client, keywords_data):
  bigquery_client.insert_to_table('keywords', keywords_data)
  #select from client
  #assert that what comes out is what went in
