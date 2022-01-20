from google.cloud import bigquery
import requests
import datetime

# copied in from a project proposal

class KeywordsDataPull:
    """ a class we might generalize later if if we were going to do other pulls """
    def __init__(self, project_id, days_range=365):
        self.end_date = datetime.date.today()
        self.start_date = self.end_date - datetime.timedelta(days = days_range)
        self.client = bigquery.Client(project=project_id)
        self.campaigns = {}
        self.keywords = None

    def _write_data(self, write_function, data, context_data):
        """enables self._get_data to use context_data arg"""
        if context_data is None:
            write_function(data)
        else: 
            write_function(data, context_data)
    
    def _get_data(self, endpoint, write_function, params=None, context_data=None):
        """a general function to call the client report api"""
        url = "https://api.clientseoreport.com/v3/"+endpoint
        headers = {
        'Authorization': 'Basic ########'
        }
        response = requests.request("GET", url, params, headers).json()
        pages = response['metadata']['total_pages']
        data = response['data']
        self._write_data(write_function, data, context_data)
        for page in range(2, pages):
            if params is None: 
                params = {'page': page}
            else:
                params['page'] = page
            data = requests.request("GET", url, params, headers).json()['data']
        self._write_data(write_function, data, context_data)
    
    def _initialize_bigquery_table(self, tablename, attr):
        """a general function to get a table_ref for some tablename and store it 
        in the class"""
        dataset_ref = self.client.dataset('data')
        table_ref = dataset_ref.table(tablename)
        self.__dict__[attr] = self.client.get_table(table_ref) 

    def _campaigns_write_function(self, data):
        """campaign data is written to the class as an attribute for later use"""
        for campaign in data:
            self.campaigns[campaign['id']] = campaign['company']
    
    def _keywords_write_function(self, data):
        """fetches rankings by keyword and writes it to bigquery
        TODO: this function ought to write keywords as a batch load - 
        not one insert per record"""
        def ftx_write_function(data, keyword_data):
            keyword_data["google_ranking"] = int(data["googleRanking"])
            keyword_data["bing_ranking"] = int(data["bingRanking"])
            keyword_data["date"]= str(data["date"])
            self.client.insert_rows(self.keywords, [keyword_data])

        for keyword in data:
            ## start building transaction
            keyword_data = {
                'campaign_id': str(keyword['campaign_id']),
                'company': str(self.campaigns[keyword['campaign_id']]),
                'keyword_id': str(keyword['id']),
                'keyword_phrase': str(keyword['keyword_phrase']),
            }          
            params = {
                'keyword_id': keyword['id'],
                'start_date': self.start_date.strftime('%Y-%m-%d'),
                'end_date': self.end_date.strftime('%Y-%m-%d')
            }
            #make request about keyword details
            self._get_data('resources/rankings/keyword', ftx_write_function, params, keyword_data)

    def get_keywords(self):
        #get campaigns data (so we can have company names)
        self._get_data('campaigns', self._campaigns_write_function)
        #intialize bigquery client for keywords
        self._initialize_bigquery_table('clc_api_data','keywords')
        self._get_data('keywords', self._keywords_write_function)