from gcloud_fxns import call_gcloud_fxn, wipe_yesterday_data

def get_keywords(event, context):
     """Calls our gcloud fxn to update keywords
     """
     wipe_yesterday_data()
     campaigns_list = []
     call_gcloud_fxn(campaigns_list, 365)

