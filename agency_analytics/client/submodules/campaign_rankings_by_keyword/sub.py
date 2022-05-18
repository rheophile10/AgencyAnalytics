from agency_analytics.client.submodules.protocol import ClientModule
from typing import List, Any

class CampaignsByKeyword(ClientModule):
    def data(self, **kwargs) -> List[Any]:
        """returns agency analytics data"""
        raise NotImplementedError
    
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