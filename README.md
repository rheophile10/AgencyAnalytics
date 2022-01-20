## Description

Pulls data from the [Agency Analytics API](https://agencyanalytics.com/docs/api/introduction) with a date range of the last 13 months
loads the data to a table in google BigQuery

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


##### Blocked

- get a pass for api tests 
   - currently I am receiving HTTP 500 status codes from the api
- create a table in BigQuery
  - create a view
    - I need campaigns data before I can call the keywords ranking api.
- make a BigQuery Client
  - that handles keyword ranking - I am need the api to work before I can test that data


##### in progress

- make some tests to make sure all the data that came out of the API went into BigQuery

##### TODO

- write tests for the api client
  - test that the api client receives response data
  - test that data coming out of the api meets schema expectations
- get a pass for the api client tests
- load data to the table in BigQuery

- make a logger 
- test the logger

- deploy as a google cloud function
- run the google cloud function
- schedule the google cloud function
- check that the google cloud function ran at the scheduled time
- improve README




