# Парсер книг с сайта tululu.org

Программа скачивает книги, обложки книг и информацию в `*.json` файл [с этого сайта](https://tululu.org/txt.php).


### Как установить

* Скачать [этот script](https://github.com/miazigoo/Parsing_online_Library)

**Python3 уже должен быть установлен**. 
Используйте `pip` (или `pip3`, если возникает конфликт с Python2) для установки зависимостей:
```properties
pip install -r requirements.txt
```

### Аргументы

При запуске программы используйте аргументы 
```commandline
--start_page (Указать стартовую страницу)
--end_page (Указать последнюю страницу)
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