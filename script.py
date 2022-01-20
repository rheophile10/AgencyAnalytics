from bigquery_writer.bigclient import OurClient
from dotenv import dotenv_values
config = dotenv_values(".env") 
bigquery_client = OurClient(config['TEST_PROJECT_ID'], config['TEST_DATASET_ID'])
bigquery_client._initialize_db_from_schemas(exist_ok=True)
test_campaigns = [{
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
test = bigquery_client.insert_campaigns(test_campaigns, test=True)
test_records = bigquery_client.query('select * from `windy-bounty-337122.test.test_campaigns`;').result()
test_records.num_results
bigquery_client.delete_table('windy-bounty-337122.test.test_campaigns')