import requests
from bs4 import BeautifulSoup
import csv


def product_page(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                 number_available, product_description, category, review_rating, image_url):
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    product_page_url = url
    universal_product_code = soup.find_all("td")[0].string
    title = soup.find("h1").string
    price_including_tax = soup.find_all("td")[3].string
    price_excluding_tax = soup.find_all("td")[2].string
    number_available = soup.find_all("td")[5].string
    product_description = soup.find("article").find_all("p")[3].string
    category = soup.find(class_="breadcrumb").find_all("a")[2].string
    review_rating = soup.find_all("td")[6].string
    image_url = soup.find(class_="item")("img")
    print(image_url)

    heading = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
               "number_available", "product_description", "category", "review_rating", "image_url"]

    rows = [
        {"product_page_url": product_page_url,
         "universal_product_code": universal_product_code,
         "title": title,
         "price_including_tax": price_including_tax,
         "price_excluding_tax": price_excluding_tax,
         "number_available": number_available,
         "product_description": product_description,
         "category": category,
         "review_rating": review_rating,
         "image_url": image_url}
    ]

    print(rows)

    with open("product.csv", "w", newline='') as product_csv:
        file_writer = csv.DictWriter(product_csv, fieldnames=heading)
        file_writer.writerow(rows)