Sure! Here's a professional and clear README for your project:

---

# Delta.ir Apartment Scraper

This project scrapes apartment listings from [delta.ir](https://delta.ir/tehran/buy/apartment) and saves the data into CSV or Excel files. The project is split into two parts:

* **scraper.py**: Handles fetching and parsing the website.
* **dql.py**: Handles saving the scraped data to CSV or Excel.

---

## Features

* Scrapes all apartment listings with links starting with `detail`.
* Extracts key information:

  * Title/Info (e.g., neighborhood, area)
  * Price
  * Link to the listing
  * Building condition (e.g., نوساز, years old, بیش از ۲۰ سال ساخت)
* Saves data to **CSV** or **Excel**.
* Designed to separate scraping logic and data-saving logic for clean code.

---

## Requirements

* Python 3.8+
* Packages:

  ```bash
  pip install requests beautifulsoup4 openpyxl
  ```

> Note: `openpyxl` is only required if you want to save to Excel.

---

## Usage

### Step 1: Scrape Data

`scraper.py` contains the scraping logic. You can test it independently:

```bash
python scraper.py
```

This will print the scraped rows in the console.

---

### Step 2: Save Data

`dql.py` will call `scraper.py` and save the data to CSV or Excel.

#### CSV:

```bash
python dql.py
```

This creates `delta_listings.csv` with columns:
`Title/Info | Price | Link | Condition`

#### Excel:

```python
# In dql.py, uncomment Excel section
# Output: delta_listings.xlsx
```

---

## Project Structure

```
project/
│── scraper.py   # Scrapes delta.ir and returns data
│── dql.py       # Saves scraped data to CSV/Excel
│── delta_listings.csv  # Example output file
│── README.md
```

---

## Notes

* Delta.ir is JavaScript-heavy; some listings may require Selenium if they are dynamically loaded. The current implementation works with static HTML and links starting with `detail`.
* Make sure to use a proper **User-Agent** in requests to avoid blocks.
* Always use this scraper **for educational purposes only**.

---

