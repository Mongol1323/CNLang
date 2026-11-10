from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # читает .env и кладёт значения в "переменные окружения"

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
# Создаем движок базы данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Создаем фабрику сессий для работы с запросами
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Базовый класс для описания таблиц (моделей)
Base = declarative_base()
# Функция-зависимость для получения сессии базы в эндпоинтах FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()