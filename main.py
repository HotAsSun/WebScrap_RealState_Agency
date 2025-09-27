import time
import logging
from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from DML import insert_apartment


logging.basicConfig(filename="logs.log",level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


opts = Options()
opts.headless = False  
driver = webdriver.Firefox(options=opts)

class Apartment:
    def __init__(self, id, price, room, area, condition, place,link):
        self.id = id
        self.price = price
        self.room = room
        self.area = area
        self.condition = condition
        self.place = place
        self.link = link 

    def __repr__(self):
        return f"<Apartment id={self.id}, price={self.price}, room={self.room}, area={self.area}, condition={self.condition}, place={self.place}, link={self.link}>"

def extract_from_detail(detail):
    """Extracts apartment info from a single detail element."""
    href = detail.get("href")
    if not href:
        return None

    price, room, area, condition, place,price_num = None, None, None, None, None, None
    span_tags = detail.find_all("span")

    for i, span in enumerate(span_tags):
        text = span.get_text(strip=True)
        
        # Price and Place
        if price is None and "قیمت" in text and i + 1 < len(span_tags):
            price = span_tags[i + 1].get_text(strip=True)
            price_num = float(price.split()[0])
            price_num *= (10**9)
            print(price_num)
            
            if i + 2 < len(span_tags):
                place = span_tags[i + 2].get_text(strip=True)
                if '.' in place:
                    place  = place.split()[0]
                elif '(' in place:
                    place = place.split('(')[0]
                    

        # Room
        if room is None and ("اتاق" in text) and i - 1 >= 0:
            room = span_tags[i - 1].get_text(strip=True)
            if room == "یک":
                room = '1'
            elif room == "دو":
                room = '2'
            elif room == "سه":
                room = '3'
            elif room == "چهار":
                room = '4'
            else:
                room = 'بیش از 4' 
                
            
        # Area
        if area is None and "متر" in text and i - 1 >= 0:
            area = span_tags[i - 1].get_text(strip=True)

        # Condition
        if condition is None:
            if "ساله" in text and i - 1 >= 0:
                condition = f"{span_tags[i - 1].get_text(strip=True)}"
            elif "نوساز" in text:
                condition = "نوساز"
            elif "بیش" in text:
                condition = "بیش از ۲۰ سال ساخت"

    if not price:
        return None

    apt_id = href.split("/")[-1]
    link = "https://delta.ir" + href
    return Apartment(apt_id, int(price_num), room, area, condition, place,link)

def scrape_apartments(url):
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((by.By.CSS_SELECTOR, "a[href^='/detail']")))

    seen = set()
    apartments = []

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        a_tags = soup.select("a[href^='/detail']")



        for detail in a_tags:
            data = extract_from_detail(detail)
            if not data:
                continue
            if data.id in seen:
                continue
            

            
            

            seen.add(data.id)
            apartments.append(data)
            logging.info(f"Saved apartment: {data}")
            insert_apartment(data.id,data.price,data.area,data.room,data.condition,data.place,data.link)
            with open("detail.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"قیمت: {data.price}, اتاق: {data.room}, متر: {data.area}, وضعیت: {data.condition}, منطقه: {data.place} لینک = {data.link}\n"
                )
                f.write("*" * 40 + "\n")

        try:
            more_button = driver.find_elements(by.By.TAG_NAME, "button")[-1]
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
