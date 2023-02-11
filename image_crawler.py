import os
import requests
import concurrent.futures
from bs4 import BeautifulSoup

def download_image(url, directory):
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split("/")[-1]
        print(f"Downloaded image: {filename}")
        with open(directory + "/" + filename, "wb") as f:
            f.write(response.content)

def crawl_images(url):
    response = requests.get(url)
    images = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        p_tags = soup.find_all("p")
        for p_tag in p_tags:
            img_tag = p_tag.find("img", class_="img-responsive")
            if img_tag:
                images.append(img_tag)
        image_urls = [image["src"] for image in images]
        directory = "images/" + url.split("/")[-1]
        if not os.path.exists(directory):
            os.makedirs(directory)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(download_image, image_url, directory) for image_url in image_urls]

# The URL of the website you want to crawl
url = input("input the url: ")

crawl_images(url)
