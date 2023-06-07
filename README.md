# Парсер книг с сайта tululu.org

Программа скачивает книги, обложки книг и информацию в `*.json` файл [с этого сайта](https://tululu.org/txt.php).
Из `*.json` файла можно сверстать `html` страницы и запустить сайт скриптом `render_website.py`

### Посмотреть пример сайта на:
https://miazigoo.github.io/Parsing_online_Library/pages/index_1.html
![screen](https://github.com/miazigoo/Parsing_online_Library/assets/55626306/7de72bcd-ac0b-464f-bf08-5ec7b937f584)


### Как пользоваться `render_website.py`:
В корне дирректории лежит файл `books_page.json` - там информация по спарсеным книгам.
Запустить `render_website.py` командой:
```sh
python render_website.py
```
Сайт будет доступен по [адресу `http://127.0.0.1:5500`](http://127.0.0.1:5500)


### Как пользоваться оффлайн:
Скачать [этот script](https://github.com/miazigoo/Parsing_online_Library.git). 
Перейти в директорию `pages` и открыть любой `html` файл.


### Скачать html сайт отдельно:
Перейти по [ссылке](https://github.com/miazigoo/miazigoo.github.io).
Прочитать `README.md`

### Как установить

* Скачать [этот script](https://github.com/miazigoo/Parsing_online_Library.git)

**Python3 уже должен быть установлен**. 
Используйте `pip` (или `pip3`, если возникает конфликт с Python2) для установки зависимостей:
```properties
pip install -r requirements.txt
```

### Ссылка на категорию книг

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `main.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
Доступны 2 переменные:
- `TUTULU_CATEGOTY_URL` — Ссылка на категорию книг. На сайте выберите нужную вам категорию, скопируйте ссылку, вставте в `.env` например: `TUTULU_CATEGOTY_URL=https://tululu.org/l93/`. По дефолту будут скачиваться книги с категории "Научная фантастика"
- `BOOKS_PAGES` - Путь к конфигурационному файлу. Дефолтно - `books_page.json`.

### Аргументы

При запуске программы используйте аргументы 
```commandline
--start_page (Указать стартовую страницу)
--end_page (Указать последнюю страницу. Без указания этого аргумента будут скачены все книги начиная с "--start_page" в категории)
--dest_folder (Указать другой путь к каталогу с результатами парсинга)
--skip_imgs (Не скачивать картинки)
--skip_txt (Не скачивать книги)
--json_path (указать свой путь к *.json файлу с результатами)
```
Например:
```commandline
python main.py --start_page 20 --end_page 30 --skip_txt --json_path my_json
```
Без указания аргументов дефолтные значения `--start_page` и `--end_page` равны 1 и 10.


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
