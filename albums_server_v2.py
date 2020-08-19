# 1. albums_server:
# Имортируем bootle
from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
from datetime import date
import time
from time import mktime, strptime
from datetime import datetime
import datetime

# Имортируем код для работы с базой
import albums_db

# Создаём классыы для исключений

# Это исключение выбрасывается когда значение года выпуска либо не может быть конвертирован в число
# Либо имеет какое-то невозможное значение
class YearValueError(Exception):
    pass

# Это исключение выбрасывается когда в POST запросе нам не передали название артиста или название альбома
class EmptyValueError(Exception):
    pass

@route("/albums/<artist>")
@route("/albums/<artist>/")
# Функция должна выводить список альбомов для артиста
def artist_albums(artist):
    # Получаем список альбомов для артиста из функции get_albums из модуля albums_db
    albums = albums_db.get_albums(artist)
    # Если список не пустой
    if albums:
        # Тут мы создаём строку с красивым выводом всех альбомов из списка и возвращаем
        album_names = [album.album for album in albums]
        result = "Кол-во албомов: {0}.\nСписок альбомов {1}: ".format(len(album_names), artist)
        result += ", ".join(album_names)
        return result
    
    else:
        # Тут мы должны вернуть ошибку 404
        error_message = "Альбомов {} не найдено".format(artist)
        return HTTPError(404, error_message)


@route("/albums", method="POST")
@route("/albums/", method="POST")
# Функция, которая добавляет новый альбом
def add_album():
    try:
        # Создаём объект класса Album
        album = albums_db.Album(
            album = request.forms.get("album"),
            artist = request.forms.get("artist"),
            genre = request.forms.get("genre"),
            year = request.forms.get("year")
        )
        # Валидируем альбом
        valid_album(album)
        # Добавляем альбом в ДБ
        albums_db.add_album(album)
        message = "Тут сообщение, что у {0} добавлен {1} альбом".format(album.artist, album.album)
        return message
    except EmptyValueError:
        return HTTPError(400, "Сообщение, что в поле артист и в поле альбом не может быть пусто")
    except YearValueError:
        return HTTPError(400, "Сообщение, что передан некорректный год")
    # Исключение DuplicateAlbumError означает что в БД уже есть такой альбом
    except albums_db.DuplicateAlbumError:
        return HTTPError(409, "Сообщение что уже есть такой альбом")

# Функция для валидации введенёх данных
#
def valid_album(album):
    try:
        # Конвертируем значение в поле год в тип int
        int_year = int(album.year)
        if int_year > 1800:
            

            return "OK"
        else:
            # Выбрасываем исключение, когда год не соответствует условию
            raise YearValueError()
    except Exception:
        raise YearValueError()


# Запускам сервер
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)