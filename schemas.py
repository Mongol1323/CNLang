from pydantic import BaseModel, ConfigDict, Field
# Что клиент ПРИСЫЛАЕТ тебе, когда хочет добавить слово.
# BaseModel это "родитель" от Pydantic: он сам проверяет, что данные правильные
# (в hanzi пришла строка, а не число, обязательное поле не пропущено и т.д.).
# Если данные кривые, FastAPI сам вернёт клиенту ошибку, твой код даже не запустится.
from datetime import datetime
class WordCreate(BaseModel):
    hanzi: str # обязательное поле, строка
    pinyin: str
    translation: str
    hsk_lvl: int | None = None # необязательное: либо число, либо ничего; по умолчанию ничего
# Что ты ОТДАЁШЬ клиенту в ответ.
# (WordCreate) значит: берём все поля оттуда и добавляем свои, не переписывая заново.
class WordOut(WordCreate):
    # from_attributes=True: разрешает превратить объект из базы (models.Word)
    # в эту схему. Без этого Pydantic не поймёт, что с ним делать.
    model_config = ConfigDict(from_attributes=True)
    id: int # клиенту сказать id, который база выдала сама

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6, max_length=100)
    email: str = Field(min_length=6, max_length=100)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str  # пароль и хеш наружу не отдаём
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str
class Answer(BaseModel):
    word_id: int
    known: bool # true = знаю, false = не знаю
# Что возвращаем после ответа
class Progress(BaseModel):
    word_id: int
    word: int
# Что посылает клиент, когда отвечает на карточку
class AnswerIn(BaseModel):
    word_id: int
    known: bool # true = знаю, false = не знаю
# Что возрващаем после ответа
class ProgressOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    word_id: int
    level: int
    next_review: datetime

# Что учить сегодня: слова на повторение и новые
class StudyToday(BaseModel):
    due: list[WordOut]
    new: list[WordOut]