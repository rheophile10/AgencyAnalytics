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
    aa_client.get_campaigns_list()
    assert len(aa_client.campaigns) > 0

@pytest.fixture
def campaign_id(aa_client):
    return aa_client.get_campaigns_list(page=1)[0]['id']
    
def test_get_keywords_list(aa_client, campaign_id):
    aa_client.get_keywords_list(campaign_id = campaign_id)
    assert len(aa_client.keywords) > 0     

@pytest.fixture
def keyword_rankings_args(aa_client, campaign_id):
    date_created = datetime.strptime(aa_client.campaigns[0]['date_created'], '%Y-%m-%d %H:%M:%S')
    start_date = date_created - timedelta(days = 5)
    end_date = datetime.today()
    return campaign_id, start_date, end_date

def test_get_keyword_rankings_list(aa_client, keyword_rankings_args):
    campaign_id, start_date, end_date = keyword_rankings_args
    aa_client.get_keyword_rankings_list(campaign_id=campaign_id, start_date=start_date, 
        end_date=end_date, page=1)
    assert len(aa_client.__dict__['resources_rankings_campaign']) > 0     

@pytest.fixture 
def writer():
    return Writer()   

def test_write_campaigns_list(aa_client, writer):
    aa_client.write_campaigns_list(writer.write)
    assert len(writer.data) > 0

def test_write_keywords_list(aa_client, writer, campaign_id):
    aa_client.write_keywords_list(writer.write, campaign_id)
    assert len(writer.data) > 0

def test_write_keyword_rankings_list(aa_client, writer, keyword_rankings_args):
    campaign_id, start_date, end_date = keyword_rankings_args
    aa_client.write_keyword_rankings_list(writer.write, campaign_id=campaign_id, 
        start_date=start_date, end_date=end_date, page=1)
    assert len(writer.data) > 0
