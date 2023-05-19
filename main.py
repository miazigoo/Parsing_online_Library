import json
import os
import random
import sys
import time
import requests
import argparse
import logging

from tqdm import trange
from environs import Env
from pathlib import Path
from os.path import split, splitext
from pathvalidate import sanitize_filename
from requests import HTTPError
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, unquote

from parse_tululu_by_category import parse_url_book_by_category, parse_max_page

SESSION = requests.Session()


def retry(exc_type=requests.exceptions.ConnectionError):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            cooloff = 5
            cooloff_random = [5, 10, 15, 20, 30]
            while True:
                try:
                    return function(*args, **kwargs)
                except exc_type as e:
                    print(
                        "Сбой подключения. Произвожу попытку нового подключения.",
                        e,
                        file=sys.stderr,
                    )
                    logging.debug(e)
                    time.sleep(cooloff)
                    cooloff = random.choice(cooloff_random)

        return wrapper

    return real_decorator


def get_command_line_arguments():
    """parse args"""
    parser = argparse.ArgumentParser(
        description="""Программа скачивает книги. По дефолту будут скачены все книги  """
    )
    parser.add_argument(
        "--start_page",
        nargs="?",
        help="Введите с какой страницы скачивать книги: ",
        type=int,
    )
    parser.add_argument(
        "--end_page",
        nargs="?",
        help="Введите до какой страницы скачивать книги: ",
        type=int,
    )
    parser.add_argument(
        "--dest_folder", nargs="?", help="путь к каталогу с результатами парсинга: "
    )
    parser.add_argument(
        "--skip_imgs", help="не скачивать картинки.", action="store_true"
    )
    parser.add_argument("--skip_txt", help="не скачивать книги.", action="store_true")
    parser.add_argument(
        "--json_path",
        nargs="?",
        help="указать свой путь к *.json файлу с результатами: ",
    )
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
        raise BookRedirectFormatError("Произошел redirect. Перехожу к следующему ID")


@retry()
def download_txt(book_id, filename, folder="books/"):
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

    url = "https://tululu.org/txt.php"
    params = {"id": book_id}
    response = SESSION.get(url, params=params)
    check_for_redirect(response)
    response.raise_for_status()
    normal_filename = sanitize_filename(filename)
    file_path = os.path.join(folder, normal_filename)
    with open(f"{file_path}", "wb") as file:
        file.write(response.content)


@retry()
def download_image(url, filename, folder="images/"):
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
    response = SESSION.get(url)
    response.raise_for_status()
    normal_filename = sanitize_filename(filename)
    file_path = os.path.join(folder, normal_filename)
    with open(f"{file_path}", "wb") as file:
        file.write(response.content)


class BookRedirectFormatError(HTTPError):
    pass


def parse_book_page(book_id, response):
    soup = BeautifulSoup(response.text, "lxml")
    title_tag = soup.select_one("#content > h1").text
    book_comments = soup.select(".texts .black")
    img_src = soup.select_one("div.bookimage img")["src"]
    genres_tag = soup.select("span.d_book a")
    book_title = title_tag.split("::")[0].strip()
    book_author = title_tag.split("::")[1].strip()
    book_name = f"{book_id}.{book_title}.txt"
    genres_text = [x.text for x in genres_tag]
    comments_text = [com.text for com in book_comments]
    return book_name, img_src, comments_text, genres_text, book_title, book_author


def fetch_books_info(books_info, start_page, end_page, folder="books_INFO"):
    book_path = Path(folder)
    book_path.mkdir(parents=True, exist_ok=True)
    file_name = sanitize_filename(f"books_INFO_page_{start_page}_{end_page}.json")
    file_path = os.path.join(book_path, file_name)
    with open(f"{file_path}", "w", encoding="utf-8") as file:
        json.dump(books_info, file, ensure_ascii=False, indent=4)


def get_book_id(book_url):
    url_address = urlsplit(book_url).path
    encoding_url = unquote(url_address)
    book_id = encoding_url.split("b")[1].replace("/", "")
    return book_id


@retry()
def fetch_books(start_page, end_page, category_url, args):
    books_info = []
    dest_folder, skip_imgs, skip_txt, json_path = (
        args.dest_folder,
        args.skip_imgs,
        args.skip_txt,
        args.json_path,
    )
    with trange(start_page, end_page, colour="blue") as t_range:
        for page in t_range:
            logging.basicConfig(level=logging.INFO)
            logging.info(f"Загружаем со страницы №{page}")
            try:
                page_url = f"{category_url}{page}"
                response = SESSION.get(page_url)
                response.raise_for_status()
                check_for_redirect(response)
                book_urls = parse_url_book_by_category(response)

                for book_url in book_urls:
                    book_id = get_book_id(book_url)
                    url = f"https://tululu.org/b{book_id}/"
                    response_book_page = SESSION.get(url)
                    response_book_page.raise_for_status()
                    check_for_redirect(response_book_page)

                    (
                        book_name,
                        img_src,
                        comments_text,
                        genres_text,
                        book_title,
                        book_author,
                    ) = parse_book_page(book_id, response_book_page)
                    if skip_txt is False:
                        if dest_folder:
                            download_txt(book_id, book_name, folder=dest_folder)
                        else:
                            download_txt(book_id, book_name)

                    img_url = urljoin(book_url, img_src)
                    img_name, _ = get_filename_and_ext(img_url)

                    if skip_imgs is False:
                        if dest_folder:
                            download_image(img_url, img_name, folder=dest_folder)
                        else:
                            download_image(img_url, img_name)

                    normal_img_filename = sanitize_filename(img_name)
                    normal_book_filename = sanitize_filename(img_name)
                    books_info.append(
                        {
                            "title": book_title,
                            "author": book_author,
                            "img_src": f"images/{normal_img_filename}",
                            "book_path": f"books/{normal_book_filename}",
                            "comments": comments_text,
                            "genres": genres_text,
                        }
                    )
            except BookRedirectFormatError as error:
                print(error, file=sys.stderr)
                logging.debug(error)
                continue
            except HTTPError as error:
                print("Битая ссылка. Перехожу к следующей. ", error, file=sys.stderr)
                logging.debug(error)
                continue
    if json_path:
        fetch_books_info(books_info, start_page, end_page, folder=json_path)
    else:
        fetch_books_info(books_info, start_page, end_page)


def main():
    env = Env()
    env.read_env()
    category_url = env.str("TUTULU_CATEGOTY_URL", "https://tululu.org/l55/")
    response = SESSION.get(category_url)
    response.raise_for_status()
    max_page, select_page = parse_max_page(response)
    args = get_command_line_arguments()
    start_page, end_page = args.start_page, args.end_page
    if not start_page:
        start_page = select_page
    if not end_page:
        end_page = max_page
    fetch_books(start_page, end_page, category_url, args)


if __name__ == "__main__":
    main()
