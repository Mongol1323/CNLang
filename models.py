from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from database import Base


# Один класс = одна таблица в базе
class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    hanzi = Column(String(50), nullable=False)
    pinyin = Column(String(100), nullable=False)
    translation = Column(String(200), nullable=False)
    hsk_lvl = Column(Integer, nullable=True)

class User(Base):
    __tablename__ = "users"

    start_level = Column(Integer, default=0, nullable=False) # с какого уровня хск давать новые слова
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
# Как пользователь знает это слово
class Progress(Base):
    __tablename__ = "progress"
    __table_args__ = (UniqueConstraint("user_id", "word_id"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # ссылка на users.id
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False) # ссылка на words.id
    level = Column(Integer, default=0, nullable=False)  # ступенька лесенкиб от 0 до 5
    next_review = Column(DateTime(timezone=True), nullable=False) # когда показать слово снова