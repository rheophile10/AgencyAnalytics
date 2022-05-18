import pytest
from dotenv import dotenv_values
from agency_analytics.tests.writer import LocalWriter


@pytest.fixture 
def writer():
    return LocalWriter() 
