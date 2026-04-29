# 🛒 E-commerce Product Data Scraper

A Python-based web scraper that extracts product data from e-commerce websites, cleans it, and exports it into a structured CSV file ready for analysis.

---

## 📌 Project Overview

This scraper targets [books.toscrape.com](https://books.toscrape.com) — a safe practice e-commerce site — and collects product information across **50 pages** (1000+ products) automatically.

---

## ✨ Features

- ✅ Scrapes product **title, price, star rating, and availability**
- ✅ Handles **pagination** automatically across all pages
- ✅ Cleans data — removes duplicates, fixes data types, strips whitespace
- ✅ Exports clean data to a structured **CSV file**
- ✅ Prints a **summary report** (avg price, top-rated books, etc.)
- ✅ Polite scraping with request delays

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| BeautifulSoup4 | HTML parsing & data extraction |
| Pandas | Data cleaning & CSV export |
| Requests | Sending HTTP requests |

---

## 📁 Project Structure

```
ecommerce-scraper/
│
├── books_scraper.py   # Main scraper script
├── books_data.csv     # Output CSV file (generated after running)
└── README.md          # Project documentation
```

---

## ⚙️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-scraper.git
cd ecommerce-scraper
```

**2. Install dependencies**
```bash
pip install requests beautifulsoup4 pandas
```

**3. Run the scraper**
```bash
# Scrape all pages
python books_scraper.py

# Or limit to N pages (e.g. 3 pages for a quick test)
python books_scraper.py 3
```

**4. Check your output**

A `books_data.csv` file will be created in the same folder.

---

## 📊 Sample Output

| Title | Price (£) | Star Rating | Availability |
|-------|-----------|-------------|--------------|
| A Light in the Attic | 51.77 | 3 | In stock |
| Tipping the Velvet | 53.74 | 1 | In stock |
| Soumission | 50.10 | 1 | In stock |

---

## 📈 Summary Report (auto-generated)

```
Total books      : 1000
Avg price        : £35.07
Cheapest book    : £10.00
Most expensive   : £59.99
5-star books     : 200
In stock         : 1000
```

---

## 🚀 Skills Demonstrated

- Web scraping with BeautifulSoup
- Pagination handling
- Data cleaning & transformation with Pandas
- CSV export & reporting
- Clean, well-structured Python code

---

## 📬 Contact

Feel free to reach out on [Upwork](https://www.upwork.com) for freelance web scraping or data extraction projects!
