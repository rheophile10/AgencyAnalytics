from agency_analytics.client.submodules.protocol import ClientModule
from typing import List, Any

class Campaigns(ClientModule):
    def data(self, **kwargs) -> List[Any]:
        """returns agency analytics data"""
        raise NotImplementedError

    def get_campaigns_list(self, filter=None, page=None, limit=None, order_by=None, order_direction=None, csv=False, active_only = False):
        """list all campaigns https://agencyanalytics.com/docs/api/campaigns#list-all-campaigns"""
        args = {'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._list_data('campaigns', params, csv=csv)
        if active_only: 
            self.campaigns = self._prune_campaigns_list(self.campaigns)
        return self.campaigns 

    def write_campaigns_list(self, write_function, filter=None, page=None, limit=None, order_by=None, order_direction=None):
        """write all campaigns https://agencyanalytics.com/docs/api/campaigns#list-all-campaigns"""
        args = {'filter': filter, 'page':page, 'limit':limit, 'order_by': order_by, 'order_direction':order_direction}
        params = self._build_params(args)
        self._write_list_data('campaigns', write_function, params)