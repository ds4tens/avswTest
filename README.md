# Тестовое задание. Карта сайта. АВ Софт

1. Парсинг сайта реализован с помощью `beautifulsoup` с поддержкой `lxml `
2. Поддержка пула потоков реализована на `ThreadPoolExecutor`
3. Чтобы не заморачиваться с обработкой данных и написанием "сырых" запрсов к БД, решил воспользоваться помощью `DRF`

# Запуск

`git clone https://github.com/ds4tens/avswTest <path_to_clone>`


* Установить все необходимые пакеты

`pip install -r requirements.txt`

* Настройка Django 

`python .\dbs\manage.py makemigrations`

`python .\dbs\manage.py migrate`

`python .\dbs\manage.py runserver`

* Запуск парсинга

`python main.py <кол-во_потоков> <logging 1/0>`

* Пример

`python main.py 10 1`