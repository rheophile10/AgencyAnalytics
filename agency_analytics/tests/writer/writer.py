from typing import Any, List, Dict
from csv import DictWriter
import os

TEST_DATA_DIRECTORY = os.path.dirname(__file__)

class LocalWriter:
    """A local writer that writes data to csv files for testing purposes"""
    data: List[Dict[str, Any]] = []
    def __init__(self, test_data_directory:str)->None:
        self.test_dir = test_data_directory

    def write(self, data: List[Dict[str, Any]], filename: str = 'test.csv'):
        fieldnames = data[0].keys()
        with open(filename, 'w') as f:
            writer = DictWriter(f, fieldnames)
            writer.writerow({k:k for k in fieldnames})
            for row in data:
                writer.writerow(row)