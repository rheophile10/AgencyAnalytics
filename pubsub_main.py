from gcloud_fxns import call_gcloud_fxn

def get_keywords(event, context):
     """Calls our gcloud fxn to update keywords
     """
     campaigns_list = []
     call_gcloud_fxn(campaigns_list, 390)

