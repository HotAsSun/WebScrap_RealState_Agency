import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Selenium Setup ---
opts = Options()
opts.headless = False  # set True if you don't want browser window
driver = webdriver.Firefox(options=opts)


def extract_from_detail(detail):
    """Extracts apartment info from a single detail element."""
    href = detail.get("href")
    if not href:
        return None

    price, room, area, condition, place = None, None, None, None, None

    span_tags = detail.find_all("span")
    for i, span in enumerate(span_tags):
        text = span.get_text(strip=True)

        # Price and Place (next 2 spans after 'قیمت')
        if price is None and "قیمت" in text and i + 1 < len(span_tags):
            price = span_tags[i + 1].get_text(strip=True)
            if i + 2 < len(span_tags):
                place = span_tags[i + 2].get_text(strip=True)

        # Room
        if room is None and ("اتاق" in text or "خواب" in text) and i - 1 >= 0:
            room = span_tags[i - 1].get_text(strip=True)

        # Area
        if area is None and "متر" in text and i - 1 >= 0:
            area = span_tags[i - 1].get_text(strip=True)

        # Condition
        if condition is None:
            if "ساله" in text and i - 1 >= 0:
                condition = f"{span_tags[i - 1].get_text(strip=True)} ساله"
            elif "نوساز" in text:
                condition = "نوساز"
            elif "کلید نخورده" in text:
                condition = "کلید نخورده"

    if not price:  # skip invalid listings
        return None

    return {
        "href": href,
        "price": price,
        "room": room,
        "area": area,
        "condition": condition,
        "place": place
    }


def scrape_apartments(url):
    """Scrapes apartment data from Delta.ir by clicking 'More' until listings end."""
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/detail']")))

    seen = set()
    apartments = []

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        a_tags = soup.select("a[href^='/detail']")

        for detail in a_tags:
            data = extract_from_detail(detail)
            if not data:
                continue
            if data["href"] in seen:
                continue

            seen.add(data["href"])
            apartments.append(data)

            logging.info(f"Saved apartment: {data}")
            print(type(data))
            for i in data :
                print(data, data[i],"\n")
            with open("detail.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"قیمت: {data['price']}, اتاق: {data['room']}, متر: {data['area']}, وضعیت: {data['condition']}، منطقه: {data['place']}\n"
                )
                f.write("*" * 40 + "\n")

        # Try clicking "More"
        try:
            more_button = driver.find_elements(By.TAG_NAME, "button")[-1]
            driver.execute_script("arguments[0].scrollIntoView();", more_button)
            time.sleep(1)
            more_button.click()
            time.sleep(2)
            logging.info("Clicked 'More' button")
        except Exception:
            logging.info("No more button found. End of listings.")
            break

    return apartments


if __name__ == "__main__":
    url = "https://delta.ir/tehran/buy/apartment"
    results = scrape_apartments(url)
    driver.quit()
    logging.info(f"Scraping finished. Total {len(results)} apartments collected.")

