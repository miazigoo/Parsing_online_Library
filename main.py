import requests
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urlsplit
from os.path import splitext
from os.path import split

from requests import HTTPError


def check_for_redirect(response):
    if response.status_code > 204:
        raise HTTPError


def get_filename_and_ext(img_url):
    """Getting the link address and extension"""
    url_address = urlsplit(img_url).path
    encoding_url = unquote(url_address)
    filename = split(encoding_url)[-1]
    extension = splitext(filename)[-1]
    return filename, extension


def download_book(book_url, book_name, books_path):
    """Download the book"""
    book_path = Path(books_path)
    book_path.mkdir(parents=True, exist_ok=True)
    response = requests.get(book_url)
    response.raise_for_status()
    with open(f'{book_path}/{book_name}', 'wb') as file:
        file.write(response.content)


def fetch_10_books():
    books_path = 'books'
    fetch_book = 0
    book_id = 1
    while fetch_book < 10:
        try:
            url = 'https://tululu.org/txt.php'
            params = {'id': book_id}
            response = requests.get(url, params=params)
            check_for_redirect(response)
            response.raise_for_status()
            book_url = response.url
            book_name = f'{fetch_book}.txt'
            download_book(book_url, book_name, books_path)
            book_id += 1
            fetch_book += 1
        except HTTPError:
            book_id += 1


def main():
    fetch_10_books()


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
