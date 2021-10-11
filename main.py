import requests
from bs4 import BeautifulSoup
import csv
import os


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
    image = requests.get(image_url).content
    image_name = universal_product_code + ".jpg"
    with open(image_name, "wb") as handler:
        handler.write(image)

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


def books_per_category(url, csv_file_name, add_heading):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    book_url = soup.find_all(class_="image_container")

    heading = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
               "number_available", "product_description", "category", "review_rating", "image_url"]

    with open(csv_file_name, "a") as product_csv:
        file_writer = csv.DictWriter(product_csv, fieldnames=heading)
        if add_heading:
            file_writer.writeheader()
        for book in book_url:
            product = product_page(book.a["href"].replace("../../../", "http://books.toscrape.com/catalogue/"))
            file_writer.writerows(product)

    if soup.find(class_="pager") and soup.find(class_="pager")(class_="next"):
        next_button = soup.find(class_="pager")(class_="next")[0]
        next_button_url = next_button.a["href"]
        new_url = url[:-11] + next_button_url
        books_per_category(new_url, csv_file_name, False)


def categories():
    page = requests.get("https://books.toscrape.com/index.html")
    soup = BeautifulSoup(page.content, "html.parser")
    category_url = soup.find_all(class_="nav-list")[0]("ul")[0]("li")

    parent_directory = "/Users/celiatois/Documents/OpenClassrooms/python/CeliaTOIS_2_20092021"
    parent_path = os.path.join(parent_directory, "Data")
    if not os.path.exists(parent_path):
        os.mkdir(parent_path)
    os.chdir(parent_path)

    for category in category_url:
        href = category.a["href"]
        link = "https://books.toscrape.com/" + href
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")

        if soup.find(class_="pager"):
            url = link[:-10] + "page-1.html"
            link = url
        else:
            link = link

        name = "".join(category.a.string.split())
        csv_file_name = name + ".csv"
        child_directory = parent_directory + "/Data"
        child_path = os.path.join(child_directory, name)
        if not os.path.exists(child_path):
            os.mkdir(child_path)
        os.chdir(child_path)
        with open(csv_file_name, "w"):
            books_per_category(link, csv_file_name, True)


categories()
