Запуск на локальной машине
--------------------------
##### Подготовить python окружение

Создать рабочее окружение с помощью virtualenv (virtualenvwrapper), перейти в него в папке проекта. Установить необходимые пакеты:

```pip install -r requirements.txt```

##### Подготовить файлы с данными
Поместить в папку data файлы:

   - [ft_freqprune_100K_20K_pq_300.bin](https://github.com/avidale/compress-fasttext/releases/tag/v0.0.1)
   сжатая версия fasttext модели от RusVectores (локально можно использовать и более крупную модель, но тогда нужно поменять атрибут MODEL_FILE_NAME в ```config.py```)  

   - freq_nouns.txt - лист самых частотных существительных в неопределенной форме

##### Создать туннель для запросов
Для того, чтобы локальный сервер мог получать запросы из сети, нужно создать туннель.
Это можно сделать утилитой ngrok (https://sysadmin.pm/ngrok/)

Запускаем туннель и не выключаем. Вкладка терминала занимается консолью ngrok.

```ngrok http 8443```

Из консоли копируем адрес, на который будет повешен webhook - запросы на этот адрес будут передаваться на локальную машину.
Например, ```https://7bd2f07d5a4d.ngrok.io```

##### Создать локальную базу данных
[Инструкция по созданию приложения с PostgreSQL](https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc)

Создаем базу (имя можно дать и другое - оно будет передано как переменная окружения):

``` sudo -u <username> createdb contact_bot ```

##### Переменные окружения
Устанавливаем значения environment variables:

```export WEBHOOK_HOST="https://7bd2f07d5a4d.ngrok.io"```

(выбираем именно https протокол - обязательно для webhook адреса)

```export DATABASE_URL="postgresql:///contact_bot"```

```export TOKEN=<...>```

```export APP_CONFIG="local"```

##### Настроить базу данных

Из корневой папки выполнить:

```python manage.py db migrate```

```python manage.py db upgrade```

В базе должны появиться таблицы defs и users_state. Их наличие можно проверить командой ```\dt```  в командной строке PostgreSQL.

##### Запуск
Запускаем бота:

```python ./run.py```

После запуска нужно единократно перейти в браузере по адресу WEBHOOK_HOST
(Сервер запускается в режиме lazy loading, то есть поднимается по первому запросу).

Бот готов к работе.


Запуск на heroku
---------------------------
[Полезная и понятная инструкция](https://tproger.ru/translations/telegram-bot-create-and-deploy/)

Проверить, установлены ли необходимые environment variables:

```TOKEN=<...>```

```APP_CONFIG="heroku"```

Для доступа в хранилище Amazon S3:

```AWS_ACCESS_KEY_ID```

```AWS_SECRET_ACCESS_KEY```

```S3_BUCKET_NAME```

После запуска нужно единократно перейти в браузере по адресу WEBHOOK_HOST
(Сервер запускается в режиме lazy loading, то есть поднимается по первому запросу).