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
        self.__dict__[endpoint] = data
        for page in range(2, pages):
            if params is None: 
                params = {'page': page}
            else:
                params['page'] = page
            _, data = self._make_request(endpoint, params)
            self.__dict__[endpoint] = data
        if csv:
            self._dump_to_csv(endpoint, data)

    def _dump_to_csv(self, endpoint, data):
        cols = set()
        for row in data:
            cols.add(row.keys()) 
        with open(f'{endpoint}.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, cols)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    def _build_params(self, args):
        params = {k:v for k, v in args.items() if args[k] is not None} if len(args.keys()) > 0 else None
        return params
    
    def get_campaigns_list(self, filter=None, page=None, limit=None, order_by=None, order_direction=None):
        """list all campaigns https://agencyanalytics.com/docs/api/campaigns#list-all-campaigns"""
        args = {'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._list_data('campaigns', params)
        return self.campaigns 

    def get_keywords_list(self, filter=None, page=None, limit=None, order_by=None, order_direction=None):
        """list all keywords https://agencyanalytics.com/docs/api/keywords#list-all-keywords"""
        args = {'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._list_data('keywords', params)
        return self.keywords 

    def get_keyword_rankings_list(self, campaign_id, start_date, end_date, search=None, page=None, limit=None, 
        sort_metric=None, sort_direction=None, compare_previous_method=None):
        """list all keyword rankings https://agencyanalytics.com/docs/api/feeds#list-campaign-rankings-by-keyword"""
        start_date = start_date.strftime(start_date, '%Y-%m-%d')
        end_date = end_date.strftime(end_date, '%Y-%m-%d')
        args = {'campaign_id':campaign_id, 'start_date':start_date, 'end_date':end_date, 
            'search':search, 'page':page, 'limit':limit, 'sort_metric':sort_metric, 
            'sort_direction':sort_direction, 'compare_previous_method':compare_previous_method}
        params = self._build_params(args)
        self._list_data('keyword_rankings', params)
        return self.rankings

    def _write_list_data(self, endpoint, write_function, params=None):
        """operates the list api endpoints and executes supplied write function"""
        pages, data = self._make_request(endpoint, params)
        write_function(data)
        for page in range(2, pages):
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

    def write_keywords_list(self, write_function, filter=None, page=None, limit=None, order_by=None, order_direction=None):
        """write all keywords https://agencyanalytics.com/docs/api/keywords#list-all-keywords"""
        args = {'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._write_list_data('keywords', write_function, params)
    
    def write_keyword_rankings_list(self, write_function, campaign_id, start_date, end_date, search=None, page=None, limit=None, 
        sort_metric=None, sort_direction=None, compare_previous_method=None):
        """write all keyword rankings https://agencyanalytics.com/docs/api/feeds#list-campaign-rankings-by-keyword"""
        start_date = start_date.strftime(start_date, '%Y-%m-%d')
        end_date = end_date.strftime(end_date, '%Y-%m-%d')
        args = {'campaign_id':campaign_id, 'start_date':start_date, 'end_date':end_date, 
            'search':search, 'page':page, 'limit':limit, 'sort_metric':sort_metric, 
            'sort_direction':sort_direction, 'compare_previous_method':compare_previous_method}
        params = self._build_params(args)
        self._list_data('keyword_rankings', write_function, params)
