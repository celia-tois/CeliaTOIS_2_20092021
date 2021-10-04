import requests
from bs4 import BeautifulSoup
import csv


def product_page(url):
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
    image_url = soup.find(class_="item")("img")[0].attrs["src"].replace("../../", "http://books.toscrape.com/")

    product_info = [
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

    return product_info


def books_per_category(url, csv_file_name):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    book_url = soup.find_all(class_="image_container")

    heading = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
               "number_available", "product_description", "category", "review_rating", "image_url"]

    with open(csv_file_name, "w") as product_csv:
        file_writer = csv.DictWriter(product_csv, fieldnames=heading)
        file_writer.writeheader()
        for book in book_url:
            product = product_page(book.a["href"].replace("../../../", "http://books.toscrape.com/catalogue/"))
            file_writer.writerows(product)

# books_per_category()


def categories():
    page = requests.get("https://books.toscrape.com/index.html")
    soup = BeautifulSoup(page.content, "html.parser")
    category_url = soup.find_all(class_="nav-list")[0]("ul")[0]("li")
    for category in category_url:
        href = category.a["href"]
        link = "https://books.toscrape.com/" + href
        csv_file_name = category.a.string + ".csv"
        with open (csv_file_name, "w"):
            books_per_category(link, csv_file_name)
            print(link)

categories()

# url = "https://books.toscrape.com/catalogue/category/books/young-adult_21/page-1.html"
# page = requests.get(url)
# soup = BeautifulSoup(page.content, "html.parser")
# pager = soup.find(class_="pager")
# if pager.find(class_="next"):
#     next_button = pager.find(class_="next")
#     next_button_url = next_button.a["href"]
#     url = url[:-11] + next_button_url
#     categories(url)
#     print(url)
# else:
#     print("bkvjfd")