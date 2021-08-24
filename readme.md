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
  * `ALTER USER saleor WITH PASSWORD 'news';`
  * `CREATE DATABASE mynews;`

## Project Setup
* `git clone https://github.com/MohiuddinSumon/mynews.git`
* `cd mynews`
* `pip install -r requirements.txt`
