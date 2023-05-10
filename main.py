import os
import requests
from pathlib import Path
from pathvalidate import sanitize_filename
from requests import HTTPError
from bs4 import BeautifulSoup


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


def get_book_name(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('td', class_='ow_px_td').find('div', id='content').find('h1')
    book_title = title_tag.text.split('::')[0].strip()
    book_name = f'{book_id}.{book_title}.txt'
    return book_name


def fetch_books(num):
    fetch_book = 0
    book_id = 1
    while fetch_book < num:
        try:
            url = 'https://tululu.org/txt.php'
            params = {'id': book_id}
            response = requests.get(url, params=params)
            check_for_redirect(response)
            response.raise_for_status()
            book_url = response.url
            book_name = get_book_name(book_id)
            download_txt(book_url, book_name)
            book_id += 1
            fetch_book += 1
        except (HTTPError, AttributeError):
            book_id += 1


def main():
    fetch_books(10)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
