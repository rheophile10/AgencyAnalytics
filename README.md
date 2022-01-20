## Description

Pulls data from the [Agency Analytics API](https://agencyanalytics.com/docs/api/introduction) with a date range of the last 18 months

loads the data to a table in google BigQuery

## Setup

This uses python virtual environments and a .env file for client secrets. 

#### Development

##### Done

- setup the project
- write tests for the api
- write tests for the api client
  - test that the api client receives response data
  - test that data coming out of the api meets schema expectations

##### Blockers

- get a pass for api tests 
   - currently I am receiving HTTP 500 status codes from the api

##### TODO

- write tests for the api client
  - test that the api client receives response data
  - test that data coming out of the api meets schema expectations
- get a pass for the api client tests
- create a table in BigQuery
- load data to the table in BigQuery
- make some tests to make sure all the data that came out of the API went into the BigQuery
- make a logger 
- test the logger
- deploy as a google cloud function
- run the google cloud function
- schedule the google cloud function
- check that the google cloud function ran at the scheduled time
- improve README




