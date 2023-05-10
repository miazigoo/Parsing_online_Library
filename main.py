import os
import requests
from pathlib import Path
from os.path import split, splitext
from pathvalidate import sanitize_filename
from requests import HTTPError
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, unquote


def get_filename_and_ext(img_url):
    """Getting the link address and extension"""
    url_address = urlsplit(img_url).path
    encoding_url = unquote(url_address)
    filename = split(encoding_url)[-1]
    extension = splitext(filename)[-1]
    return filename, extension


def check_for_redirect(response):
    if response.status_code > 204:
        raise HTTPError


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    book_path = Path(folder)
    book_path.mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    normal_filename = sanitize_filename(filename)
    file_path = os.path.join(folder, normal_filename)
    with open(f'{file_path}', 'wb') as file:
        file.write(response.content)


def download_image(url, filename, folder='images/'):
    """Функция для скачивания изображений.
    Args:
        url (str): Cсылка на картинку, которую хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    book_path = Path(folder)
    book_path.mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    normal_filename = sanitize_filename(filename)
    file_path = os.path.join(folder, normal_filename)
    with open(f'{file_path}', 'wb') as file:
        file.write(response.content)


def get_soup(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_book_name(book_id):
    soup = get_soup(book_id)
    title_tag = soup.find('td', class_='ow_px_td').find('div', id='content').find('h1')
    book_title = title_tag.text.split('::')[0].strip()
    book_name = f'{book_id}.{book_title}.txt'
    return book_name


def fetch_book_comments(book_id, book_name):
    soup = get_soup(book_id)
    book_comments = soup.find_all('div', class_='texts')
    book_path = Path('comments')
    book_path.mkdir(parents=True, exist_ok=True)
    normal_book_name = sanitize_filename(book_name)
    file_path = os.path.join(book_path, normal_book_name)
    with open(f"{file_path}", "w", encoding='utf-8') as file:
        for comment in book_comments:
            file.write(comment.span.string + '\n')
    return 'success'


def get_img_url_name(book_id):
    url = 'https://tululu.org/'
    soup = get_soup(book_id)
    img = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(url, img)
    img_name, _ = get_filename_and_ext(img_url)
    return img_url, img_name


def fetch_books(num):
    fetch_book = 0
    book_id = 1
    while fetch_book < num:
        try:
            url = 'https://tululu.org/txt.php'
            params = {'id': book_id}
            response = requests.get(url, params=params, allow_redirects=False)
            check_for_redirect(response)
            response.raise_for_status()

            book_url = response.url
            book_name = get_book_name(book_id)
            fetch_book_comments(book_id, book_name)
            download_txt(book_url, book_name)

            img_url, img_name = get_img_url_name(book_id)
            download_image(img_url, img_name)

            book_id += 1
            fetch_book += 1
        except (HTTPError, AttributeError):
            book_id += 1


def main():
    fetch_books(10)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
