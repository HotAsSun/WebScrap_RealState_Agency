import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Apartment class ---
class Apartment:
    def __init__(self, href, price, rooms, area, condition):
        self.href = href
        self.price = price
        self.rooms = rooms
        self.area = area
        self.condition = condition

    def __str__(self):
        return f"قیمت: {self.price}, اتاق: {self.rooms}, متر: {self.area}, وضعیت: {self.condition}, لینک: {self.href}"

# --- Selenium driver setup ---
def setup_driver(headless=False):
    opts = Options()
    opts.headless = headless
    driver = webdriver.Firefox(options=opts)
    logging.info("WebDriver initialized")
    return driver

# --- Extract info from a single detail element ---
def find_data(detail):

    # Find price
    price = None
    location = None
    for s in detail.find_all("span"):
        if "قیمت" in s.get_text(strip=True):
            next_span = s.find_next_sibling("span")
            second_span = next_span.find_next_sibling("span") if next_span else None
            if next_span:
                price = next_span.get_text(strip=True)
            if second_span:
                location = second_span.get_text(strip=True)
            break

    if not price:
        return None

    # Rooms
    rooms = None
    for s in detail.find_all("span"):
        if "اتاق" in s.get_text():
            rooms = s.find_previous_sibling("span")


    # Area
    area = None
    for s in detail.find_all("span"):
        if "متر" in s.get_text(strip=True):
            prev = s.find_previous_sibling("span")
            if prev:
                area = prev.get_text(strip=True)
            break

    # Condition
    condition = None
    for s in detail.find_all("span"):
        t = s.get_text(strip=True)
        if "ساله" in t:
            prev = s.find_previous_sibling("span")
            if prev:
                condition = f"{prev.get_text(strip=True)} ساله"
            break
        if "نوساز" in t:
            condition = "نوساز"
            break


    return Apartment( price=price, rooms=rooms, area=area, condition=condition)
    print()
# --- Load all listings by clicking "More" until the end ---
def get_page(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/detail']")))

    seen = set()
    apartments = []

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        details = soup.select("a[href^='/detail']")
        logging.info(f"Found {len(details)} listings on current page")

        for detail in details:
            apt = find_data(detail)
            if apt and apt.href not in seen:
                seen.add(apt.href)
                apartments.append(apt)
                logging.info(f"Added: {apt}")

        # Click "More" button if exists
        try:
            more_button = driver.find_elements(By.TAG_NAME, "button")[-1]
            driver.execute_script("arguments[0].scrollIntoView();", more_button)
            time.sleep(1)
            more_button.click()
            time.sleep(2)
            logging.info("Clicked 'More' button")
        except Exception:
            logging.info("No more button found. All listings loaded.")
            break

    return apartments

# --- Main execution ---
def main():
    url = "https://delta.ir/tehran/buy/apartment"
    driver = setup_driver(headless=False)

    try:
        apartments = get_page(driver, url)

        # Save results to file
        with open("detail.txt", "w", encoding="utf-8") as f:
            for apt in apartments:
                f.write(apt)
                f.write("*" * 40 + "\n")

        logging.info(f"Scraping finished. Total {len(apartments)} apartments saved.")

    finally:
        driver.quit()
        logging.info("WebDriver closed")

if __name__ == "__main__":
    main()
