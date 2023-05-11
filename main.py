import os
import sys
import time

import requests
import argparse
import logging

from pathlib import Path
from os.path import split, splitext
from pathvalidate import sanitize_filename
from requests import HTTPError
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, unquote


def retry(cooloff=5, exc_type=None):
    if not exc_type:
        exc_type = [requests.exceptions.ConnectionError]

    def real_decorator(function):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    if e.__class__ in exc_type:
                        print("Сбой подключения. Произвожу попытку нового подключения.", e, file=sys.stderr)
                        logging.debug(e)
                        time.sleep(cooloff)
                    else:
                        raise e

        return wrapper

    return real_decorator


def get_command_line_arguments():
    """parse args"""
    parser = argparse.ArgumentParser(
        description="""Программа скачивает книги. по дефолту будут скачены книги с id 1 по 10 """)
    parser.add_argument('start_id', nargs='?', help='Введите с какого id скачивать книги: ',
                        default=1, type=int)
    parser.add_argument('end_id', nargs='?', help='Введите до какого id скачивать книги: ',
                        default=10, type=int)
    args = parser.parse_args()

    return args


def get_filename_and_ext(img_url):
    """Getting the link address and extension"""
    url_address = urlsplit(img_url).path
    encoding_url = unquote(url_address)
    filename = split(encoding_url)[-1]
    extension = splitext(filename)[-1]
    return filename, extension


def check_for_redirect(response):
    if response.history:
        raise BookRedirectFormatError('Произошел redirect. Перехожу к следующему ID')


def download_txt(book_id, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        book_id (str): ID на книгу, которую хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    book_path = Path(folder)
    book_path.mkdir(parents=True, exist_ok=True)

    url = 'https://tululu.org/txt.php'
    params = {'id': book_id}
    session = requests.Session()
    response = session.get(url, params=params)
    check_for_redirect(response)
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
    session = requests.Session()
    response = session.get(url)
    response.raise_for_status()
    normal_filename = sanitize_filename(filename)
    file_path = os.path.join(folder, normal_filename)
    with open(f'{file_path}', 'wb') as file:
        file.write(response.content)


class BookRedirectFormatError(HTTPError):
    pass


def parse_book_page(book_id):
    try:
        url = f'https://tululu.org/b{book_id}/'
        session = requests.Session()
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        my_soup = {
            'title_tag': soup.find('td', class_='ow_px_td').find('div', id='content').find('h1'),
            'book_comments': soup.find_all('div', class_='texts'),
            'img_src': soup.find('div', class_='bookimage').find('img')['src'],
            'genres_tag': soup.find('span', class_='d_book').find_all('a')
        }
        return my_soup
    except AttributeError as err:
        print(err, file=sys.stderr)
        logging.debug(err)
        raise BookRedirectFormatError('Перехожу к следующей книге')


def get_book_name(book_id, soup):
    title_tag = soup['title_tag']
    book_title = title_tag.text.split('::')[0].strip()
    book_name = f'{book_id}.{book_title}.txt'

    genres_tag = soup['genres_tag']
    genres_text = [x.text for x in genres_tag]
    return book_name


def fetch_book_comments(book_name, soup):
    book_comments = soup['book_comments']
    book_path = Path('comments')
    book_path.mkdir(parents=True, exist_ok=True)
    normal_book_name = sanitize_filename(book_name)
    file_path = os.path.join(book_path, normal_book_name)
    with open(f"{file_path}", "w", encoding='utf-8') as file:
        for comment in book_comments:
            if comment.span.string:
                file.write(comment.span.string + '\n')
    return 'success'


def get_img_url_name(book_id, soup):
    url = f'https://tululu.org/b{book_id}/'
    img_src = soup['img_src']
    img_url = urljoin(url, img_src)
    img_name, _ = get_filename_and_ext(img_url)
    return img_url, img_name


def fetch_books(start_id, end_id):
    book_id = start_id
    while book_id <= end_id:
        try:
            soup = parse_book_page(book_id)

            book_name = get_book_name(book_id, soup)
            fetch_book_comments(book_id, book_name, soup)
            download_txt(book_id, book_name)

            img_url, img_name = get_img_url_name(book_id, soup)
            download_image(img_url, img_name)

            book_id += 1
        except BookRedirectFormatError as error:
            print(error, file=sys.stderr)
            logging.debug(error)
            book_id += 1


@retry()
def main():
    args = get_command_line_arguments()
    start_id, end_id = args.start_id, args.end_id
    fetch_books(start_id, end_id)


if __name__ == '__main__':
    main()
