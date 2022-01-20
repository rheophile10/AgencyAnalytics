from attr import dataclass
from google.cloud import bigquery

class OurClient(bigquery.Client):
    def __init__(self, project_id, dataset_name):
        super().__init__(project=project_id)
        self.dataset_name = dataset_name

    def insert_to_table(self, tablename, data):
        """inserts to table"""
        dataset_ref = self.dataset(self.dataset_name)
        table_ref = dataset_ref.table(tablename)
        table = self.get_table(table_ref) 
        self.insert_rows(table, data)