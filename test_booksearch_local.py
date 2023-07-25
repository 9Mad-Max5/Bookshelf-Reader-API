from bs4 import BeautifulSoup
import requests
import re
# import pandas as pd
import json
from googlesearch import search

book_title = "FBLACK HOLE ‘siihe>"
search_txt = book_title + " book amazon"

def format_publisher(publisher):
    '''
    Cleans and returns the publisher name scrapped from
    the webpage.
    '''
    publisher = publisher[publisher.find("by") + 3:]
    publisher = publisher[0:publisher.find("\n")] + " " + \
        publisher[publisher.find("("):publisher.find(")") + 1]

    return publisher

def search_for_key(json_data, search_key):
    if isinstance(json_data, dict):
        if search_key in json_data:
            return json_data[search_key]
        else:
            for key, value in json_data.items():
                result = search_for_key(value, search_key)
                if result is not None:
                    return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = search_for_key(item, search_key)
            if result is not None:
                return result
            
book_amazon_link = ""
for link in search(search_txt, tld="de", num=10, stop=10, pause=2):
    if "amazon" in link and "dp/" in link:
        book_amazon_link = link
        print(book_amazon_link)
        break

# Headers mit Location- und Language-Informationen
headers = {
    'Accept-Language': 'de',  # Beispiel für eine Sprachinformation (Deutsch)
}

isbn10 = book_amazon_link[book_amazon_link.find("dp/") + 3:]
response = requests.get("https://www.goodreads.com/book/isbn/" + isbn10, headers=headers)
# print(response.text)
if response.text:
    soup = BeautifulSoup(response.text, "html.parser")
    # image_url = soup.find("div", {"class": "editionCover"}).img.get("src")
    # class for pic has changed
    image_url = soup.find("div", {"class": "BookCover__image"}).img.get("src")
    # title = soup.find("div", {"class": "BookPageTitleSection__title"}).text
    title = soup.find("h1", {"class": "Text__title1"}).text

    author = soup.find("div", {"class": "ContributorLinksList"}).text
    details = soup.find("script", {"id": "__NEXT_DATA__"}).text
    json_data = json.loads(details)
    # print(json_data)
    # json_obj = json.dumps()
    # publisher = soup.find_all("div", {"class": "row"})[1].text
    # publisher = format_publisher(publisher)
    # isbn13 = soup.find("span", {"itemprop": "isbn"}).text
    # rating = ".".join(re.findall('\d+', soup.find("span", {"itemprop": "ratingValue"}).text))
    # description = soup.find(id="description").find_all("span")[1].text
    # total_pages = soup.find("span", {"itemprop": "numberOfPages"}).text
    # total_pages = total_pages[0:total_pages.find("pages")]
    # genre = soup.find("a", {"class": "actionLinkLite bookPageGenreLink"}).text + \
    #     ", " + soup.find_all("a", {"class": "actionLinkLite bookPageGenreLink"})[1].text

    # author = soup.find("span", {"itemprop": "name"})
    # publisher = search_key(json_data=json_obj, search_key="publisher")
    print(title)
    print(author)
    # print(type(dic_data))
    # print(dic_data["props"])

    # print(publisher)
else:
    print("Keine brauchbare response")