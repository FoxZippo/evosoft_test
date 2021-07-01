Парсеры для twitch/twitter
=====================



### Установка

```shell
pip install -r requirements.txt
```
Для работы selenium необходимо установить [драйвер](https://sites.google.com/a/chromium.org/chromedriver/downloads). 
Убедитесь, что он находится в переменной PATH. [Подробнее](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/)

В файле .env для парсинга twitter определить данные пользователя в сооветствии с .env.example 

### Использование

```shell
python parsers/twitch_parser.py

python parsers/twitter_parser.py
```