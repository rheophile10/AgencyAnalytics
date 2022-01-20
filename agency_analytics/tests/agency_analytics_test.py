import pytest
from dotenv import dotenv_values
from agency_analytics.aa_client import Client
from datetime import datetime, timedelta

class Writer:
    def __init__(self):
        self.data = []
    def write(self, data):
        self.data.append(data)

@pytest.fixture
def aa_client():
    config = dotenv_values(".env") 
    aa_client = Client(config['KEY'])
    return aa_client

def test_get_campaigns_list(aa_client):
    aa_client.get_campaigns_list(limit=5)
    assert len(aa_client.campaigns) == 5
    
def test_get_keywords_list(aa_client):
    aa_client.get_keywords_list(limit=5)
    assert len(aa_client.keywords) == 5     

@pytest.fixture
def keyword_rankings_args(aa_client):
    aa_client.get_campaigns_list(limit=5)
    campaign_id = aa_client.campaigns[0]['id']
    date_created = datetime.strptime(aa_client.campaigns[0]['date_created'], '%Y-%m-%d %H:%M:%S')
    start_date = date_created - timedelta(days = 5)
    end_date = datetime.today()
    return campaign_id, start_date, end_date

def test_get_keyword_rankings_list(aa_client, keyword_rankings_args):
    aa_client.get_campaigns_list(limit=5)
    campaign_id, start_date, end_date = keyword_rankings_args
    aa_client.get_keyword_rankings_list(campaign=campaign_id, start_date=start_date, 
        end_date=end_date, limit=5)
    assert len(aa_client.keyword_rankings) > 0     

@pytest.fixture 
def writer():
    return Writer()   

def test_write_campaigns_list(aa_client, writer):
    aa_client.write_campaigns_list(writer.write, limit=5)
    assert len(writer.data) == 5

def test_write_keywords_list(aa_client, writer):
    aa_client.write_keywords_list(writer.write, limit=5)
    assert len(writer.data) == 5

def test_write_keyword_rankings_list(aa_client, writer, keyword_rankings_args):
    campaign_id, start_date, end_date = keyword_rankings_args
    aa_client.get_keyword_rankings_list(write_function = writer.write, campaign=campaign_id, 
        start_date=start_date, end_date=end_date, limit=5)
    assert len(writer.data) > 0
