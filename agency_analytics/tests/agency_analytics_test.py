import pytest
from dotenv import dotenv_values
from agency_analytics.aa_client import Client

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
def writer():
    return Writer()   

def test_write_campaigns_list(aa_client, writer):
    aa_client.write_campaigns_list(writer.write, limit=5)
    assert len(writer.data) == 5

def test_write_keywords_list(aa_client, writer):
    aa_client.write_keywords_list(writer.write, limit=5)
    assert len(writer.data) == 5
