# 2. albums_db:

# Импорты для sqlalchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаём класс для альбома
Base = declarative_base()
class Album(Base):
    __tablename__ = "album"
    id = sa.Column(sa.Integer, primary_key=True)
    year = sa.Column(sa.Integer)
    artist = sa.Column(sa.Text)
    genre = sa.Column(sa.Text)
    album = sa.Column(sa.Text)
    
DB_PATH = "sqlite:///albums.sqlite3"
# Фунция для подключения к ДБ
def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

# Функция для поиска альбомов
def get_albums(artist):
    # Создаём сессию
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all() #Тут делаем запрос к ДБ, чтобы найти альбомы
    # нужного артиста
    return albums

# Класс ошибки, которую мы выбрасываем, когда в БД уже есть альбом с таким именем
class DuplicateAlbumError(Exception):
    pass


# Функция для добавления альбома
def add_album(album):
    session = connect_db()
    # В базе нашёлся альбом с таким же названием:
    if session.query(Album).filter(Album.album == album.album).count() > 0:
        raise DuplicateAlbumError()
    # Добавляем в ДБ альбом и делаем commit
    session.add(album)
    session.commit()
    