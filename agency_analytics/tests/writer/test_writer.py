import pytest
from agency_analytics.tests.writer import TEST_DATA_DIRECTORY, LocalWriter
from csv import DictReader
import os

source_data = [
        {
        "key": "j85NoKXpKleJNSV0VykwtyJ9pbs1",
        "label": "Mike",
        "read": "no",
        "value": "ExponentPushToken[jHBwpIEJGLl9O9njHc222m]",
        },
        {
        "key": "wU6NdkR8zBUnjuc4avOEwBACIB32",
        "label": "Amy",
        "read": "no",
        "value": "ExponentPushToken[DP8GhuHNQGiN-evdCxvdXD]",
        },
    ]

def test_writer():
    writer = LocalWriter(TEST_DATA_DIRECTORY)
    writer.write(source_data)
    assert 'test.csv' in os.listdir(TEST_DATA_DIRECTORY)

def test_file_content():    
    data = []
    with open('test.csv','r') as file:
        reader = DictReader(file)
        for row in reader:
            data.append(row)
    os.remove('test.csv')
    assert source_data == data