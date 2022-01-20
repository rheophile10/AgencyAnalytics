from google.cloud import bigquery

campaigns_schema = [
    bigquery.SchemaField('id', 'INTEGER', 'REQUIRED'),
    bigquery.SchemaField('date_created', 'DATE'),
    bigquery.SchemaField('date_modified', 'DATETIME'),
    bigquery.SchemaField('date_deleted', 'DATE'),
    bigquery.SchemaField('url', 'STRING'),
    bigquery.SchemaField('company', 'STRING'),
    bigquery.SchemaField('status', 'STRING'),
    bigquery.SchemaField('scope', 'STRING'),
    bigquery.SchemaField('google_ignore_places', 'BOOL'),
    bigquery.SchemaField('google_places_id', 'INTEGER'),
    bigquery.SchemaField('google_cid', 'INTEGER'),
    bigquery.SchemaField('google_mybusiness_id', 'INTEGER'),
    bigquery.SchemaField('google_mybusiness_name', 'STRING'),
    bigquery.SchemaField('group_title', 'STRING'),
    bigquery.SchemaField('timezone', 'STRING'),
    bigquery.SchemaField('account_id', 'INTEGER')
]

keywords_schema = [ 
    bigquery.SchemaField('id', 'INTEGER', 'REQUIRED'),
    bigquery.SchemaField('date_created', 'DATETIME'),
    bigquery.SchemaField('date_modified', 'DATETIME'),
    bigquery.SchemaField('keyword_phrase', 'STRING'),
    bigquery.SchemaField('primary_keyword', 'BOOL'),
    bigquery.SchemaField('campaign_id', 'INTEGER'),
]

city_schema = [ 
    bigquery.SchemaField('id', 'INTEGER', 'REQUIRED'),
    bigquery.SchemaField('canonical_name', 'STRING'),
    bigquery.SchemaField('country_code', 'STRING'),
    bigquery.SchemaField('target_type', 'STRING'),

]

search_language_schema = [
    bigquery.SchemaField('id', 'INTEGER', 'REQUIRED'),
    bigquery.SchemaField('name', 'STRING'),
]

keyword_rankings_schema = [ 
    bigquery.SchemaField('keywordId', 'INTEGER', 'REQUIRED'),
    bigquery.SchemaField('keywordPhrase', 'STRING'),
    bigquery.SchemaField('searchLocation_', 'STRING'),
    bigquery.SchemaField('searchLocation', 'RECORD', fields = city_schema),
    bigquery.SchemaField('searchLanguage', 'RECORD', fields = search_language_schema),
    bigquery.SchemaField('primaryKeyword', 'BOOL'),
    bigquery.SchemaField('googleRanking', 'INTEGER'),
    bigquery.SchemaField('googleRankingChange', 'INTEGER'),
    bigquery.SchemaField('googleRankingUrl', 'STRING'),
    bigquery.SchemaField('googleSerpUrl', 'STRING'),
    bigquery.SchemaField('googleMobileRanking', 'INTEGER'),
    bigquery.SchemaField('googleMobileRankingChange', 'INTEGER'),
    bigquery.SchemaField('googleMobileRankingUrl', 'STRING'),
    bigquery.SchemaField('googleMobileSerpUrl', 'STRING'),
    bigquery.SchemaField('googlePlacesRanking', 'INTEGER'),
    bigquery.SchemaField('googlePlacesRankingChange', 'INTEGER'),
    bigquery.SchemaField('googleMapsSerpUrl', 'STRING'),
    bigquery.SchemaField('bingRanking', 'INTEGER'),
    bigquery.SchemaField('bingRankingChange', 'INTEGER'),
    bigquery.SchemaField('bingRankingUrl', 'STRING'),
    bigquery.SchemaField('bingSerpUrl', 'STRING'),
    bigquery.SchemaField('localMonthlySearches', 'INTEGER'),
    bigquery.SchemaField('competitors', 'INTEGER'),
    bigquery.SchemaField('lastGoogleRankingDate', 'DATE'),
    bigquery.SchemaField('lastGoogleMobileRankingDate', 'DATE'),
    bigquery.SchemaField('lastGooglePlacesRankingDate', 'DATE'),
    bigquery.SchemaField('lastBingRankingDate', 'DATE'),
    bigquery.SchemaField('lastSearchVolumeDate', 'DATE'),
    bigquery.SchemaField('lastStatPadderDate', 'DATE'),
    bigquery.SchemaField('lastMetricRollupDate', 'DATE'),
    bigquery.SchemaField('lastResultsDate', 'DATE')
]

bigquery_model = {
    'tables':
        [
            {
                'name': 'campaigns',
                'schema': campaigns_schema
            },
            {
                'name': 'rankings',
                'schema': keyword_rankings_schema
            },
            {
                'name': 'test_campaigns',
                'schema': campaigns_schema
            },
            {
                'name': 'test_rankings',
                'schema': keyword_rankings_schema
            },
        ],
    'views':
        [
            {
                'name':'call_tracking_metrics_api',
                'sql': 
                    '''
                    SELECT 
                        campaign_id
                        ,company
                        ,keyword_id
                        ,keyword_phrase
                        ,google_ranking
                        ,bing_ranking
                        ,date 
                    FROM
                    {} ranking
                    LEFT JOIN {} campaign on ranking.campaign_id = campaign.campaign_id
                    '''
            }
        ]
}
