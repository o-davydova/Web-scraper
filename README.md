# Web-scraper

## Project Structure

###### The project is composed of several key components that come together for web scraping and distributed task processing using Celery.

* **scrape.py:** Contains code for extracting car data from the auto.ria.com website using the Selenium library.
* **db.py:** Includes code for interacting with a PostgreSQL database where information about cars is stored.
* **tasks.py:** Houses functions and Celery configurations for distributed task processing. It includes tasks for scraping (perform_scrape) and backing up the database (perform_database_dump).
* **docker-compose.yml:** The Docker Compose configuration file for creating and launching containers, including Celery, Redis, PostgreSQL, and Selenium.
* **.env**: Environment variable files containing configuration parameters for the project and Docker.
* **dumps/:** Directory for storing backups of the database.

## Running Instructions

###### Make environment variables are correctly configured before running the project. Replace the values in the sample .env file with your actual credentials and configuration.


| Variable | Description |       Example        |
| --- | --- |:--------------------:|
| `CELERY_BROKER_URL` | **_Celery_** broker URL | redis://redis:6379/0 |
| `CELERY_RESULT_BACKEND` | **_Celery_** result backend URL | redis://redis:6379/0 |
| `SCRAPING_HOUR` | **_Hour_** to schedule scraping task |          12          |
| `SCRAPING_MINUTE` | **_Minute_** to schedule scraping task |          00          |
| `DUMP_HOUR` | **_Hour_** to schedule database dump |          11          |
| `DUMP_MINUTE` | **_Minute_** to schedule database dump |          11          |
| `POSTGRES_HOST` | **_PostgreSQL_** host address |                     |
| `POSTGRES_DATABASE` | **_PostgreSQL_** database name |                     |
| `POSTGRES_USER` | **_PostgreSQL_** username |                     |
| `POSTGRES_PASSWORD` | **_PostgreSQL_** password |                     |


### Run with docker

`Docker` should be installed. Build & launch the containers using:

```
docker-compose build
docker-compose up
```
##
#### Happy Scraping! 🚗 🔍 
###### _Feel free to adapt the instructions based on your specific setup and requirements._
