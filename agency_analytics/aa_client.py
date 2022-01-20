import requests

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

    def _list_data(self, endpoint, params=None):
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

    def _build_params(self, args):
        if len(args.keys()) > 0:
            params = {}
            for arg in args:
                if args[arg] is not None:
                    params[arg] = args[arg]
        else:
            params = None
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
        """list all campaigns https://agencyanalytics.com/docs/api/campaigns#list-all-campaigns"""
        args = {'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._write_list_data('campaigns', write_function, params)
        return self.campaigns 

    def write_keywords_list(self, write_function, filter=None, page=None, limit=None, order_by=None, order_direction=None):
        """list all keywords https://agencyanalytics.com/docs/api/keywords#list-all-keywords"""
        args = {'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._write_list_data('keywords', write_function, params)
        return self.keywords 
