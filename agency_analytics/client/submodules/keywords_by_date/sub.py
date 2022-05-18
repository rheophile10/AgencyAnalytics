from agency_analytics.client.submodules.protocol import ClientModule
from typing import List, Any

class KeywordsByDate(ClientModule):
    def data(self, **kwargs) -> List[Any]:
        """returns agency analytics data"""
        raise NotImplementedError
    
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