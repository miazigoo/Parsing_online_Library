import argparse
import json
import logging
import math
import os

from more_itertools import chunked
from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)


def get_command_line_argument():
    """parse arg"""
    parser = argparse.ArgumentParser(
        description="""
        Программа рендерит веб страницы. 
        """
    )
    parser.add_argument(
        "page_path",
        nargs="?",
        help="Укажите путь до исполняемого файла, по дефолту - books_page.json: ",
        default="books_page.json",
    )
    page_path = parser.parse_args().page_path

    return page_path


BOOK_PAGE_PATH = get_command_line_argument()


def on_reload():
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html"])
    )
    with open(BOOK_PAGE_PATH, "r", encoding="utf-8") as my_file:
        books = json.load(my_file)
    books_on_page = 10
    count_pages = math.ceil(len(books) / books_on_page)
    os.makedirs("pages", exist_ok=True)
    template = env.get_template("template/base.html")
    books_chunked_pages = list(chunked(books, books_on_page))
    for page, books in enumerate(books_chunked_pages, 1):
        books_in_column = 2
        chunked_books = list(chunked(books, books_in_column))
        rendered_page = template.render(
            chunked_books=chunked_books, count=count_pages, page_num=page
        )

        with open(f"pages/index_{page}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    logger.info("Скрипт запущен")
    server = Server()
    server.watch("pages/*.rst", shell("make html", cwd="pages"), on_reload())
    server.watch("template/base.html", on_reload)
    server.serve(open_url_delay=5, debug=False, default_filename="pages/index_1.html")


if __name__ == "__main__":
    main()
