import json
import logging
import math
import os

from environs import Env
from more_itertools import chunked
from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
    )

    environs = Env()
    environs.read_env()
    file_path = environs.str("BOOKS_PAGES", "books_page.json")

    with open(f"{file_path}", "r", encoding="utf-8") as my_file:
        books = json.load(my_file)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
    )

    def on_reload():
        books_on_page = 10
        count_pages = math.ceil(len(books) / books_on_page)
        os.makedirs("pages", exist_ok=True)
        template = env.get_template("template/base.html")
        books_chunked_pages = list(chunked(books, books_on_page))
        for page, books_10 in enumerate(books_chunked_pages, 1):
            books_in_column = 2
            chunked_books = list(chunked(books_10, books_in_column))
            rendered_page = template.render(
                chunked_books=chunked_books,
                count=count_pages,
                page_num=page
            )

            with open(f"pages/index_{page}.html", "w", encoding="utf8") as file:
                file.write(rendered_page)
            logger.error("Работает (~_~)=/")

    server = Server()
    server.watch("pages/*.rst", shell("make html", cwd="pages"), on_reload())
    server.watch("template/base.html", on_reload)
    server.serve(open_url_delay=5, debug=False, default_filename="pages/index_1.html")


if __name__ == "__main__":
    main()
