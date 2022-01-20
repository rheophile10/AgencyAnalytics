import pytest
from dotenv import dotenv_values
from bigquery_writer.bigclient import OurClient

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
def bigquery_client():
  config = dotenv_values(".env") 
  bigquery_client = OurClient(config['TEST_PROJECT_ID'], config['TEST_DATASET_ID'])
  bigquery_client._initialize_db_from_schemas()
  return bigquery_client

def test_insert_campaigns(bigquery_client, campaign_data):
  test = bigquery_client.insert_campaigns(campaign_data, test=True)
  bigquery_client.delete_table(bigquery_client.table_id_prefix+'test_campaigns')
  assert test is None #there will be an error if it doesn't work

#def test_insert_keyword_rankings(bigquery_client, keywords_data):


