from pydantic import BaseModel, ConfigDict
# Что клиент ПРИСЫЛАЕТ тебе, когда хочет добавить слово.
# BaseModel это "родитель" от Pydantic: он сам проверяет, что данные правильные
# (в hanzi пришла строка, а не число, обязательное поле не пропущено и т.д.).
# Если данные кривые, FastAPI сам вернёт клиенту ошибку, твой код даже не запустится.
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
