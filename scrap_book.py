from bs4 import BeautifulSoup
import requests
import re
from googlesearch import search
from bookshelf_reader.settings import is_running_in_docker

class BookInfo:

    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.author = kwargs.get("author")
        self.image_url = kwargs.get("image_url")
        self.publisher = kwargs.get("publisher")
        self.isbn_10 = kwargs.get("isbn_10")
        self.isbn_13 = kwargs.get("isbn_13")
        self.rating = kwargs.get("rating")
        self.description = kwargs.get("description")
        self.total_pages = kwargs.get("total_pages")
        self.genre = kwargs.get("genre")


def format_publisher(publisher):
    '''
    Cleans and returns the publisher name scrapped from
    the webpage.
    '''
    publisher = publisher[publisher.find("by") + 3:]
    publisher = publisher[0:publisher.find("\n")] + " " + \
        publisher[publisher.find("("):publisher.find(")") + 1]

    return publisher


def get_book_info(book_title):
    '''
    Searches the internet for book_title
    and returns a BookInfo object containing
    the scrapped information
    '''
    if is_running_in_docker:
        # Future imporvement giving flags with env variables to the container
        tld="de"
        search_txt = book_title + " book amazon"
        domain = "amazon.de"

    else:
        tld="co.in"
        search_txt = book_title + " book amazon india"
        domain = "amazon.in"

    book_amazon_link = ""
    for link in search(search_txt, tld=tld, num=10, stop=5, pause=2):
        if domain in link and "dp/" in link:
            book_amazon_link = link
            break

    isbn10 = book_amazon_link[book_amazon_link.find("dp/") + 3:]
    response = requests.get("https://www.goodreads.com/book/isbn/" + isbn10)
    soup = BeautifulSoup(response.text, "html.parser")

    image_url = soup.find("div", {"class": "editionCover"}).img.get("src")
    title = soup.find("div", {"class": "infoBoxRowItem"}).text
    author = soup.find("span", {"itemprop": "name"}).text
    publisher = soup.find_all("div", {"class": "row"})[1].text
    publisher = format_publisher(publisher)
    isbn13 = soup.find("span", {"itemprop": "isbn"}).text
    rating = ".".join(re.findall('\d+', soup.find("span", {"itemprop": "ratingValue"}).text))
    description = soup.find(id="description").find_all("span")[1].text
    total_pages = soup.find("span", {"itemprop": "numberOfPages"}).text
    total_pages = total_pages[0:total_pages.find("pages")]
    genre = soup.find("a", {"class": "actionLinkLite bookPageGenreLink"}).text + \
        ", " + soup.find_all("a", {"class": "actionLinkLite bookPageGenreLink"})[1].text

    return BookInfo(
        title=title,
        author=author,
        image_url=image_url,
        publisher=publisher,
        isbn_10=isbn10,
        isbn_13=isbn13,
        rating=rating,
        description=description,
        total_pages=total_pages,
        genre=genre
    )
