from agency_analytics.client.submodules.protocol import ClientModule
from typing import List, Any, Callable
from datetime import datetime
import logging 

class Rankings(ClientModule):
    def data(self, **kwargs) -> List[Any]:
        """returns agency analytics data"""
        raise NotImplementedError

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

    def write_keyword_rankings_list(self, write_function: Callable, campaign, 
        start_date: datetime, end_date:datetime) -> None:
        """writes the the ranking"""
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        params = {
            'campaign_id': campaign['campaign_id'],
            'start_date': start_date, 
            'end_date': end_date, 
            'page': 1
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
        logging.warning(f'write result: wrote {pages} of data with results: {results}')
