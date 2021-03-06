import requests
import csv

class Client:
    """an API client for Agency Analytics"""
    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(self, endpoint, params):
        url = "https://api.clientseoreport.com/v3/"+endpoint
        headers = {
            'Authorization': 'Basic {}'.format(self.api_key)
        }
        response = requests.request("GET", url, params = params, headers = headers)
        response.raise_for_status()
        data = response.json()
        return data['metadata']['total_pages'], data['data']

    def _list_data(self, endpoint, params=None, csv=False):
        """operates the list api endpoints and saves results to class attribute"""
        pages, data = self._make_request(endpoint, params)
        self.__dict__[endpoint.replace('/','_')] = data
        for page in range(2, pages+1):
            if params is None: 
                params = {'page': page}
            else:
                params['page'] = page
            _, data = self._make_request(endpoint, params)
            self.__dict__[endpoint.replace('/','_')] += data
        if csv:
            self._dump_to_csv(endpoint, data)
        return self.__dict__[endpoint.replace('/','_')]

    def _dump_to_csv(self, endpoint, data):
        cols = set()
        for row in data:
            for key in row.keys():
                cols.add(key)
        with open(f'{endpoint}.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, cols)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    def _build_params(self, args):
        params = {k:v for k, v in args.items() if args[k] is not None} if len(args.keys()) > 0 else None
        return params
    
    def get_campaigns_list(self, filter=None, page=None, limit=None, order_by=None, order_direction=None, csv=False, active_only = False):
        """list all campaigns https://agencyanalytics.com/docs/api/campaigns#list-all-campaigns"""
        args = {'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._list_data('campaigns', params, csv=csv)
        if active_only: 
            self.campaigns = self._prune_campaigns_list(self.campaigns)
        return self.campaigns 

    def get_keywords_list(self, campaign_id, filter=None, page=None, limit=None, order_by=None, order_direction=None, csv=False):
        """list all keywords https://agencyanalytics.com/docs/api/keywords#list-all-keywords"""
        args = {'campaign_id':campaign_id, 'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._list_data('keywords', params, csv=csv)
        return self.keywords 

    def get_keyword_rankings_list(self, campaign_id, start_date, end_date, search=None, page=None, limit=None, 
        sort_metric=None, sort_direction=None, compare_previous_method=None):
        """list all keyword rankings https://agencyanalytics.com/docs/api/feeds#list-campaign-rankings-by-keyword"""
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        args = {'campaign_id':campaign_id, 'start_date':start_date, 'end_date':end_date, 
            'search':search, 'page':page, 'limit':limit, 'sort_metric':sort_metric, 
            'sort_direction':sort_direction, 'compare_previous_method':compare_previous_method}
        params = self._build_params(args)
        endpoint = 'resources/rankings/campaign'
        self._list_data(endpoint, params)
        return self.__dict__[endpoint.replace('/','_')]

    def _write_list_data(self, endpoint, write_function, params=None):
        """operates the list api endpoints and executes supplied write function"""
        pages, data = self._make_request(endpoint, params)
        write_function(data)
        for page in range(2, pages+1):
            if params is None: 
                params = {'page': page}
            else:
                params['page'] = page
            pages, data = self._make_request(endpoint, params)
            write_function(data)

    def write_campaigns_list(self, write_function, filter=None, page=None, limit=None, order_by=None, order_direction=None):
        """write all campaigns https://agencyanalytics.com/docs/api/campaigns#list-all-campaigns"""
        args = {'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._write_list_data('campaigns', write_function, params)

    def write_keywords_list(self, write_function, campaign_id, filter=None, page=None, limit=None, order_by=None, order_direction=None):
        """write all keywords https://agencyanalytics.com/docs/api/keywords#list-all-keywords"""
        args = {'campaign_id':campaign_id, 'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._write_list_data('keywords', write_function, params)
    
    def write_keyword_rankings_list_raw(self, write_function, campaign_id, start_date, end_date, search=None, page=None, limit=None, 
        sort_metric=None, sort_direction=None, compare_previous_method=None):
        """write all keyword rankings https://agencyanalytics.com/docs/api/feeds#list-campaign-rankings-by-keyword"""
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        args = {'campaign_id':campaign_id, 'start_date':start_date, 'end_date':end_date, 
            'search':search, 'page':page, 'limit':limit, 'sort_metric':sort_metric, 
            'sort_direction':sort_direction, 'compare_previous_method':compare_previous_method}
        params = self._build_params(args)
        self._write_list_data('resources/rankings/campaign', write_function, params)

    def _prune_campaigns_list(self, campaigns_list):
        active_campaigns_list=[]
        for campaign in campaigns_list:
            if campaign['status']=='active' and campaign['type']=='real':
                record = {
                    'campaign_id': campaign['id'],
                    'company': campaign['company'],
                    'status': campaign['status'],
                }
                active_campaigns_list.append(record)
        return active_campaigns_list

    def _make_keyword_rankings_record(self, campaign_record, keywords_ranking_records_list, params):
        record_list = []
        for keyword_record in keywords_ranking_records_list:
            record = {
                'campaign_id': campaign_record['campaign_id'],
                'company': campaign_record['company'],
                'keywordId': keyword_record['keywordId'],
                'keywordPhrase': keyword_record['keywordPhrase'],
                'googleRanking': keyword_record['googleRanking'],
                'bingRanking': keyword_record['bingRanking'],
                'lastResultsDate': keyword_record['lastResultsDate'],
                'insertDate': params['end_date']
            }
            record_list.append(record)
        return record_list

    def write_keyword_rankings_list(self, write_function, campaign, start_date, end_date):
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        params = {
            'campaign_id': campaign['campaign_id'],
            'start_date': start_date, 
            'end_date': end_date
        }
        pages, page_1_data = self._make_request('resources/rankings/campaign', params)
        page_1_data = self._make_keyword_rankings_record(campaign, page_1_data, params)
        results = []
        results.append(write_function(page_1_data))
        for page in range(2,pages+1): 
            params['page'] = page
            _, page_data = self._make_request('resources/rankings/campaign', params)
            page_data = self._make_keyword_rankings_record(campaign, page_data, params)
            results.append(write_function(page_data))
        return f'wrote {pages} of data with results: {results}'

    def get_keyword_rankings_by_date(self, keyword_id, start_date, end_date, search=None, page=None, limit=None, 
        sort_metric=None, sort_direction=None, compare_previous_method=None):
        """list all keyword rankings by date https://agencyanalytics.com/docs/api/feeds#list-keyword-rankings-by-date"""
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        args = {'keyword_id':keyword_id, 'start_date':start_date, 'end_date':end_date, 
            'search':search, 'page':page, 'limit':limit, 'sort_metric':sort_metric, 
            'sort_direction':sort_direction, 'compare_previous_method':compare_previous_method}
        params = self._build_params(args)
        endpoint = 'resources/rankings/keyword/date'
        return self._list_data(endpoint, params)
        


        
