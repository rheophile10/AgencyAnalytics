import pytest
from dotenv import dotenv_values
from bigquery_writer.bigclient import OurClient

@pytest.fixture
def keyword_rankings():
  return [{
    "campaign_id": 42,
    "company": "test",
    "keywordId": 2,
    "keyword_phrase": "this is a test",
    "googleRanking": 1,
    "bingRanking":1,
    "lastResultsDate": "2018-08-01 00:00:00"
  }]

@pytest.fixture
def bigquery_client():
  config = dotenv_values(".env") 
  bigquery_client = OurClient(config['TEST_PROJECT_ID'], config['TEST_DATASET_ID'])
  bigquery_client._initialize_db_from_schemas(exist_ok=True)
  return bigquery_client

def test_insert_campaigns(bigquery_client, keyword_rankings):
  test = bigquery_client.insert_keyword_rankings(keyword_rankings, test=True)
  bigquery_client.delete_table(bigquery_client.table_id_prefix+'test_keyword_rankings')
  assert test is None #there will be an error if it doesn't work

#def test_insert_keyword_rankings(bigquery_client, keywords_data):


