from agency_analytics.client.submodules.protocol import ClientModule
from typing import List, Any

class Keywords(ClientModule):
    def data(self, **kwargs) -> List[Any]:
        """returns agency analytics data"""
        raise NotImplementedError
    
    def get_keywords_list(self, campaign_id, filter=None, page=None, limit=None, order_by=None, order_direction=None, csv=False):
        """list all keywords https://agencyanalytics.com/docs/api/keywords#list-all-keywords"""
        args = {'campaign_id':campaign_id, 'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._list_data('keywords', params, csv=csv)
        return self.keywords 
    
    def write_keywords_list(self, write_function, campaign_id, filter=None, page=None, limit=None, order_by=None, order_direction=None):
        """write all keywords https://agencyanalytics.com/docs/api/keywords#list-all-keywords"""
        args = {'campaign_id':campaign_id, 'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._write_list_data('keywords', write_function, params)
    
