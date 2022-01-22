from gcloud_fxns import keywords_update, call_gcloud_fxn

def get_keywords(request):
    """Updates keywords table in bigquery
    """
    request_json = request.get_json()
   
    campaigns_list = request_json['campaigns_list']
    day_span = request_json['day_span']
    campaigns_list = keywords_update(campaigns_list, day_span)

    if len(campaigns_list) > 0:
        call_gcloud_fxn(campaigns_list, day_span)
