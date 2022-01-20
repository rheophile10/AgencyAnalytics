from google.cloud import bigquery
from bigquery_writer.schemas import bigquery_model
from datetime import datetime

class OurClient(bigquery.Client):
    def __init__(self, project_id, dataset_name):
        super().__init__(project=project_id)
        self.dataset_name = dataset_name
        self.table_id_prefix = '{}.{}.'.format(project_id, self.dataset_name)

    def _initialize_db_from_schemas(self, exist_ok=False):
        """initializes the database from scratch"""
        for table in bigquery_model['tables']:
            table_id = self.table_id_prefix + table['name']
            new_table = bigquery.Table(table_id, table['schema'])
            self.create_table(new_table, exists_ok=exist_ok)
        for view in bigquery_model['views']:
            view_id = self.table_id_prefix + view['name']
            new_view = bigquery.Table(view_id)
            new_view.view_query = view['sql']
            self.create_table(new_view, exists_ok=exist_ok)

    def _insert_to_table(self, tablename, data):
        """inserts to table"""
        dataset_ref = self.dataset(self.dataset_name)
        table_ref = dataset_ref.table(tablename)
        table = self.get_table(table_ref) 
        return self.insert_rows(table, data)

    def _format_datetime_to_date(self, date):
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return date.strftime('%Y-%m-%d')

    def _clean_campaign_record(self, campaign_record):       
        campaign_record = {k:v for k,v in campaign_record.items() if campaign_record[k] is not None}
        campaign_record['date_created'] = self._format_datetime_to_date(campaign_record['date_created'])
        return campaign_record

    def insert_campaigns(self, campaigns_data, test=False):            
        campaigns_data = [self._clean_campaign_record(datum) for datum in campaigns_data]
        if test:
            self._insert_to_table('test_campaigns', campaigns_data)
        else:
            self._insert_to_table('campaigns', campaigns_data)

