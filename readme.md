# My News 
A personal curated news reading application. Registered user can see custom news based on their interest.

# Project Setup Guideline
Please follow the following guideline to set up this application

## System Requirements
* `Python Version >= 3.8`
* `PostgreSQL Version == 12.8 or Equivalent`

## Manual Virtualenv Setup Process
* **OS == LINUX**
  * `mkdir venvs`
  * `pip3 install virtualenv --user`
  * `virtualenv -p python3 venvs/venv`
  * `source venvs/venv/bin/activate`
* **OS == WINDOWS**
  * `mkdir \venvs`
  * `pip install virtualenv`
  * `virtualenv \venvs\venv`
  * `\venvs\venv\Scripts\activate`
  
## Create database and user
  * `sudo -u postgres psql`
  * `CREATE USER news;`
  * `ALTER USER news WITH SUPERUSER;`
  * `ALTER USER news WITH PASSWORD 'news';`
  * `CREATE DATABASE mynews;`

## Project Setup
* `git clone https://github.com/MohiuddinSumon/mynews.git`
* `cd mynews`
* `pip install -r requirements.txt`
* `python3 manage.py migrate`
* `python3 manage.py loaddata newsapi_sources newsapi_countries`

## Environment Setup
You will need api from sendgrid (for mail) and newsapi (for news).
Create a .env file and give value as **env_sample.txt**

## Redis needs to be running
For scheduling task redis is used as a broker for celery and it needs to be running.
* **Worker =>** `celery -A mynews worker -l info`
* **Beat =>** `celery -A mynews beat -l info`

One scheduler will run every 15 minute to fetch user specific news and save them.
Another will run every day and send newsletter email to user.


## User News List - API (postman)
We have a `/news-api/` end point that will serve user specific news.
This is done with drf and token protected. So you will need the token from 
`/token/` endpoint. Make a post request to this with username and password in Body. 
```json
{
    "username": "your_user_name",
    "password": "SuPeR&seCreT"
}
```
In response you will get token  = `{"token":"d08d2cb80c6b79c93772d8c5b7b4d281b233abe1"}`
For `news-api` go to `Auth -> API Key` then Key = `Authorization`, Value = `Token d08d2cb80c6b79c93772d8c5b7b4d281b233abe1`. 
This will give the news response for that user. 
