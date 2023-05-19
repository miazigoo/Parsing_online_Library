from urllib.parse import urljoin
from bs4 import BeautifulSoup


def parse_url_book_by_category(response):
    soup = BeautifulSoup(response.text, 'lxml')
    category_book_card = soup.select('.d_book .bookimage a')
    links = [item.get("href") for item in category_book_card]
    book_urls = []

    for book_url in links:
        book_urls.append(urljoin(response.url, book_url))
    return book_urls
