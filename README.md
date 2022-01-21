## Description

Pulls data from the [Agency Analytics API](https://agencyanalytics.com/docs/api/introduction) with a date range of the last 13 months.
Loads the data to a table in google BigQuery.

## Setup

This uses python virtual environments and a .env file for client secrets. 

### Development

##### Done

- setup the project
- write tests for the api
- write tests for the api client
  - test that the api client receives response data
  - test that data coming out of the api meets schema expectations
- make a BigQuery Client
- create a table in BigQuery
  - created schema and initialize_db method to create a campaigns table
  - created schema and initialize_db method to create a keyword_rankings table
- get a pass for api tests
- create a table in BigQuery
- make a BigQuery Client
  - that handles keyword ranking 
- finish write_keyword_rankings_list on aa_client

##### in progress

- modify bigquery client
  - drop keywords table

- write the google cloud function
  - args ( campaigns: list )
  - first call: fxn( [] )
  - if len(args.campaigns) == 0, drop keywords table, pull fresh list of active campaigns, if len(campaigns) > 0 call fxn(campaigns)
  - else if len(args.campaigns) != 0, pop top campaign, get keywords, add to list, if len(campaigns) > 0 call fxn(campaigns)
- deploy as a google cloud function
- run the google cloud function
- schedule the google cloud function
- check that the google cloud function ran at the scheduled time

##### TODO (in order of descending priority)

- improve README
- annotate functions 


- make some tests to make sure all the data that came out of the API went into BigQuery
- write tests for the api client
  - test that the api client receives response data
  - test that data coming out of the api meets schema expectations

- get a pass for the api client tests
- load data to the table in BigQuery

- make a logger 
- test the logger




