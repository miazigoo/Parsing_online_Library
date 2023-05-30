import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

with open("Parse/books_INFO/books_INFO_page_1_10.json", "r", encoding="utf-8") as my_file:
    books_json = my_file.read()

books = json.loads(books_json)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('index.html')

rendered_page = template.render(
    books=books
)

with open('pages/index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
