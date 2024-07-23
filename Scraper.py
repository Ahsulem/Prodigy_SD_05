import requests
from bs4 import BeautifulSoup
import csv
import time
import random


def get_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    return random.choice(user_agents)


def scrape_amazon_products(url, num_pages=1):
    products = []

    for page in range(1, num_pages + 1):
        page_url = f"{url}&page={page}"
        headers = {'User-Agent': get_user_agent()}

        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for item in soup.find_all('div', {'data-component-type': 's-search-result'}):
            product = {}
            # Extract product name
            product_name = item.find('span', {'class': 'a-size-medium'})
            if product_name:
                product['name'] = product_name.text.strip()
            else:
                continue

            # Extract price
            price = item.find('span', {'class': 'a-price-whole'})
            if price:
                product['price'] = price.text.strip()
            else:
                product['price'] = 'N/A'

            # Extract rating
            rating = item.find('span', {'class': 'a-icon-alt'})
            if rating:
                product['rating'] = rating.text.split()[0]
            else:
                product['rating'] = 'N/A'

            products.append(product)

        print(f"Scraped page {page}")
        time.sleep(random.uniform(1, 3))  # Random delay between requests

    return products


def save_to_csv(products, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'price', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for product in products:
            writer.writerow(product)


if __name__ == "__main__":
    # URL for Amazon search results (replace with your desired search or category)
    url = "https://www.amazon.com/s?k=laptop&crid=2QEVIPDMP2Z3M&sprefix=laptop%2Caps%2C350&ref=nb_sb_noss_1"

    num_pages = 3  # Number of pages to scrape

    products = scrape_amazon_products(url, num_pages)
    save_to_csv(products, 'amazon_products.csv')

    print(f"Scraped {len(products)} products and saved to amazon_products.csv")