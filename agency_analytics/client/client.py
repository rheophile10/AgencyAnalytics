from agency_analytics.client.submodules import Campaigns, CampaignsByKeyword, Rankings, Keywords
from typing import Dict, Any
import requests

class AgencyAnalytics:
    """an API client that makes requests on Agency Analytics"""
    def __init__(self, api_key:str)->None:
        self.api_key = api_key
        self.keywords: Keywords
        self.campaings: Campaigns 
        self.campaigns_by_k: CampaignsByKeyword
        self.rankings: Rankings

    def _make_request(self, endpoint:str, params:Dict[str,Any]):
        """it makes a request of the agency analytics endpoint"""
        url = "https://api.clientseoreport.com/v3/"+endpoint
        headers = {
            'Authorization': 'Basic {}'.format(self.api_key)
        }
        response = requests.request("GET", url, params = params, headers = headers)
        response.raise_for_status()
        data = response.json()
        total_pages = data['metadata']['total_pages']
        data = data['data']
        return total_pages, data 

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

    def _build_params(self, args):
        params = {k:v for k, v in args.items() if args[k] is not None} if len(args.keys()) > 0 else None
        return params

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