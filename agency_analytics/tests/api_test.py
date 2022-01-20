import pytest
from dotenv import dotenv_values
import requests

@pytest.fixture
def headers():
    config = dotenv_values(".env") 
    headers = {
        'Authorization': 'Basic {}'.format(config['KEY'])
        }
    return headers

@pytest.fixture
def campaigns(headers):
    endpoint = 'campaigns'
    url = "https://api.clientseoreport.com/v3/"+endpoint
    params={'limit':10}
    campaigns = requests.request("GET", url, params = params, headers=headers)
    return campaigns

@pytest.fixture
def keywords(headers):
    endpoint = 'keywords'
    url = "https://api.clientseoreport.com/v3/"+endpoint
    params={'limit':10}
    keywords = requests.request("GET", url, params = params, headers=headers)
    return keywords

def test_keywords(keywords):
    assert keywords.status_code == 200

def test_campaigns(campaigns):
    assert campaigns.status_code == 200

