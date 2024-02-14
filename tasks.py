import logging
import os

from celery import Celery
from celery.schedules import crontab
from scrape import scrape
from datetime import datetime
from subprocess import call


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

celery_app = Celery("scraper", broker=os.getenv("CELERY_BROKER_URL"))

celery_app.conf.beat_schedule = {
    "scraping": {
        "task": "tasks.perform_scrape",
        "schedule": crontab(
            hour=os.getenv("SCRAPING_HOUR"), minute=os.getenv("SCRAPING_MINUTE")
        ),
    },
    "database_dump": {
        "task": "tasks.perform_database_dump",
        "schedule": crontab(
            hour=os.getenv("DUMP_HOUR"), minute=os.getenv("DUMP_MINUTE")
        ),
    },
}


@celery_app.task
def perform_scrape():
    try:
        scrape()
        logging.info("Scrape task completed successfully.")
    except Exception as e:
        logging.error(f"Error during scraping task: {str(e)}")


@celery_app.task
def perform_database_dump():
    try:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_file_name = f"/dumps/database_dump_{current_time}.sql"
        postgres_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DATABASE')}"
        command = [
            "pg_dump",
            postgres_url,
            f"--file={dump_file_name}",
        ]

        logging.info(f"Executing command: {' '.join(command)}")
        call(command)
        logging.info("Dump task completed successfully.")

    except Exception as e:
        logging.error(f"Error during database dump task: {str(e)}")
        raise
