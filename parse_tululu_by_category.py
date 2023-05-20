from urllib.parse import urljoin
from bs4 import BeautifulSoup


def parse_url_book_by_category(response):
    soup = BeautifulSoup(response.text, "lxml")
    category_book_card = soup.select(".d_book .bookimage a")
    links = [item.get("href") for item in category_book_card]
    book_urls = [urljoin(response.url, book_url) for book_url in links]

    return book_urls


def parse_max_page(response):
    soup = BeautifulSoup(response.text, "lxml")
    pages = soup.select(".center a.npage")
    max_page = int(pages[-1].text)
    start_page = int(soup.select_one(".center .npage_select").text)

    return max_page, start_page
