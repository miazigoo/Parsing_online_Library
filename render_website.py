import json
import logging
import os

from more_itertools import chunked
from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape


logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
    )

with open("Parse/books_INFO/books_INFO_page_1_10.json", "r", encoding="utf-8") as my_file:
    books_json = my_file.read()

books = json.loads(books_json)


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)


def on_reload():
    os.makedirs('pages', exist_ok=True)
    template = env.get_template('base.html')
    books_chunked_pages = list(chunked(books, 10))
    for num, books_10 in enumerate(books_chunked_pages, 1):
        books_chunked = list(chunked(books_10, 2))
        rendered_page = template.render(
            books_chunked=books_chunked
        )

        with open(f'pages/index{num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)
        logger.error("Работает (~_~)=/")


server = Server()
server.watch('pages/*.rst', shell('make html', cwd='pages'), on_reload())
server.watch("base.html", on_reload)
server.serve(root='.')
