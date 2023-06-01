# Парсер книг с сайта tululu.org

Программа скачивает книги, обложки книг и информацию в `*.json` файл [с этого сайта](https://tululu.org/txt.php).


### Как установить

* Скачать [этот script](https://github.com/miazigoo/Parsing_online_Library)

**Python3 уже должен быть установлен**. 
Используйте `pip` (или `pip3`, если возникает конфликт с Python2) для установки зависимостей:
```properties
pip install -r requirements.txt
```

### Ссылка на категорию книг

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `main.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
Доступна 1 переменная:
- `TUTULU_CATEGOTY_URL` — Ссылка на категорию книг. На сайте выберите нужную вам категорию, скопируйте ссылку, вставте в `.env` например: `TUTULU_CATEGOTY_URL=https://tululu.org/l93/`. По дефолту будут скачиваться книги с категории "Научная фантастика"

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

### Запуск сайта
https://miazigoo.github.io/Parsing_online_Library/pages/index_1.html

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
