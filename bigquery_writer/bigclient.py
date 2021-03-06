from google.cloud import bigquery
from bigquery_writer.schemas import bigquery_model
from datetime import datetime

class OurClient(bigquery.Client):
    def __init__(self, project_id, dataset_name):
        super().__init__(project=project_id)
        self.dataset_name = dataset_name
        self.table_id_prefix = '{}.{}.'.format(project_id, self.dataset_name)

    def _initialize_db_from_schemas(self, exist_ok=True):
        """initializes the database from scratch"""
        for table in bigquery_model['tables']:
            table_id = self.table_id_prefix + table['name']
            new_table = bigquery.Table(table_id, table['schema'])
            self.create_table(new_table, exists_ok=exist_ok)
        for view in bigquery_model['views']:
            view_id = self.table_id_prefix + view['name']
            new_view = bigquery.Table(view_id)
            params = [self.table_id_prefix + param for param in view['sql']['params']]
            new_view.view_query = view['sql']['sql'].format(*params)
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
    
    def _clean_keyword_ranking_record(self, keyword_ranking_record):       
        campaign_record = {k:v for k,v in keyword_ranking_record.items() 
            if keyword_ranking_record[k] is not None}
        campaign_record['lastResultsDate'] = self._format_datetime_to_date(campaign_record['lastResultsDate'])
        return campaign_record

    def wipe_keyword_rankings_table(self):
        self.delete_table(f'{self.table_id_prefix}rankings', not_found_ok=True)
        
    def insert_keyword_rankings(self, keyword_rankings_data):            
        campaigns_data = [self._clean_keyword_ranking_record(datum) for datum in keyword_rankings_data]
        if len(campaigns_data) > 0:
            return self._insert_to_table('rankings', campaigns_data)
        else:
            return 'there were no campaign keywords to insert!'

    def delete_keyword_rankings_with_date(self, date):
        query = f'DELETE FROM {self.table_id_prefix}rankings WHERE insertDate = \'{date}\''
        return self.query(query).result()
