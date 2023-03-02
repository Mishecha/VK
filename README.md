# Публикация комиксов

Этот проект скачивает комиксы, передает в ВК и затем отправляет его в группу

# Как установить
Python3 должен быть уже установлен. Затем используйте pip для установки зависимостей:
```
pip install -r requirements.txt
```
## Создание группы приложений в VK
Для начала создадите свою собственную группу. Дальше ваш нужно создать приложение [вот тут](https://dev.vk.com/)

## client_id
Нужно нажать на кнопку “Редактировать” для нового приложения, в адресной строке вы увидите его client_id. 

## Переменные окружения
Узнать access_token можно после того, как вы сформируете запрос для его получения. Выглядит он так:
```
https://oauth.vk.com/authorize?client_id={ВАШ_КЛИЕНТ_ID}&display=page&scope=photos,groups,wall,offline&response_type=token&v=5.131&state=123456
```

После вставьте access_token в .env. В env нужно написать так:
```
ACCESS_TOKEN=token
```

Узнать group_id можно [здесь](https://regvk.com/id/). После вставьте токен group_id в .env. В env нужно написать так:
```
GROUP_ID=-token
```
## Запуск кода
Для того чтобы код работал, надо открыть терминал, написать cd и путь до вашего проекта. Для скачивания и отправки комиксов в VK нужно написать:
```
python main.py
```
# Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.