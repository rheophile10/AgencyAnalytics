from gcloud_fxns import keywords_update, call_gcloud_fxn
import google.cloud.logging
import logging

def get_keywords(request):
    """Updates keywords table in bigquery
    """
    
    #client = google.cloud.logging.Client()
    #client.setup_logging()
    request_json = request.get_json()
    #logging.debug(f'json keys {request_json.keys()}')
    campaigns_list = request_json['campaigns_list']
    #logging.debug(f'campaigns_list length {len(campaigns_list)}')
    day_span = request_json['day_span']
    #logging.debug(f'day span {day_span}')
    campaigns_list = keywords_update(campaigns_list, day_span)
    #logging.debug(f'campaigns_list length after write {len(campaigns_list)}')
    if len(campaigns_list) > 0:
        call_gcloud_fxn(campaigns_list, day_span)
    return len(campaigns_list)