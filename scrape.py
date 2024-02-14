import re
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from sqlalchemy.orm import sessionmaker

from db import engine, save_cars


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def extract_numbers(text):
    numbers = re.findall(r"\d+", text)
    return int("".join(numbers))


def scrape():
    firefox_options = webdriver.FirefoxOptions()

    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=firefox_options,
    )

    try:
        start_page_url = "https://auto.ria.com/uk/car/used/"
        driver.get(start_page_url)

        pagination_links = driver.find_elements(By.CLASS_NAME, "page-link")
        total_pages = int(pagination_links[-2].text.replace(" ", ""))

        card_links = []
        parsed_cars = []
        failed_cars = []

        for page_number in range(1, total_pages + 1):
            page_url = f"{start_page_url}?page={page_number}"
            driver.get(page_url)

            cards = driver.find_elements(By.CLASS_NAME, "ticket-item")

            for card in cards:
                card_link = card.find_element(By.CLASS_NAME, "address").get_attribute(
                    "href"
                )
                card_links.append(card_link)

        for card_link in card_links:
            try:
                car_vin = driver.find_element(By.CLASS_NAME, "label-vin").text
            except NoSuchElementException:
                try:
                    car_vin = driver.find_element(By.CLASS_NAME, "vin-code").text
                except NoSuchElementException:
                    failed_cars.append(card_link)
                    continue

            driver.get(card_link)
            title = driver.find_element(By.CLASS_NAME, "head").get_attribute("title")

            price_element = driver.find_element(By.CLASS_NAME, "price_value")
            price_usd = extract_numbers(price_element.text)

            odometer_element = driver.find_element(By.CLASS_NAME, "base-information")
            odometer = extract_numbers(odometer_element.text) * 1000

            username = driver.find_element(By.CLASS_NAME, "seller_info_name").text

            media_element = driver.find_element(By.CLASS_NAME, "photo-620x465")
            image_element = media_element.find_element(By.TAG_NAME, "img")
            image_url = image_element.get_attribute("src")

            images_count_text = driver.find_element(
                By.CLASS_NAME, "action_disp_all_block"
            ).text
            images_count = extract_numbers(images_count_text)

            try:
                car_number = driver.find_element(By.CLASS_NAME, "state-num").text
            except NoSuchElementException:
                car_number = ""

            phone_show_link = driver.find_element(By.CLASS_NAME, "phone_show_link")
            driver.execute_script("arguments[0].click();", phone_show_link)
            phone_element = driver.find_element(By.CLASS_NAME, "phone")
            phone_number_text = phone_element.get_attribute("data-phone-number")
            while len(phone_number_text) < 1:
                phone_number_text = phone_element.get_attribute("data-phone-number")
            phone_number = f"+380{extract_numbers(phone_number_text)}"

            car_data = {
                "url": card_link,
                "title": title,
                "price_usd": price_usd,
                "odometer": odometer,
                "username": username,
                "phone_number": phone_number,
                "image_url": image_url,
                "images_count": images_count,
                "car_number": car_number,
                "car_vin": car_vin,
            }
            parsed_cars.append(car_data)

        if failed_cars:
            logging.warning(
                f"Failed to extract VIN for the following cars: {', '.join(failed_cars)}"
            )

        driver.quit()

        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = Session()

        save_cars(parsed_cars, session)
        logging.info(f"Scraping completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    scrape()
