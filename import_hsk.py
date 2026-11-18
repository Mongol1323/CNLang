import json
import sys

from sqlalchemy import select

from database import SessionLocal
import models

# Какой файл читать: берём из команды, а если не указан, то hsk.json
path = sys.argv[1] if len(sys.argv) > 1 else "hsk.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

db = SessionLocal()
try:
    # Что уже есть в базе. Нужно, чтобы при повторном запуске не плодить дубли
    existing = {(h, p) for h, p in db.execute(select(models.Word.hanzi, models.Word.pinyin))}

    added = 0
    for item in data:
        hanzi = item["hanzi"].strip()
        pinyin = item["pinyin"].strip()
        if (hanzi, pinyin) in existing:
            continue  # такое слово уже есть, пропускаем

        translations = item.get("translations", {})
        # Берём русский перевод, а если его нет, то английский. Не больше 4 значений
        meanings = translations.get("rus") or translations.get("eng") or []
        translation = "; ".join(meanings[:4])[:200]  # [:200]: в колонке максимум 200 символов
        if not translation:
            continue

        db.add(models.Word(
            hanzi=hanzi,
            pinyin=pinyin,
            translation=translation,
            hsk_lvl=item.get("level"),
        ))
        existing.add((hanzi, pinyin))
        added += 1

    db.commit()  # все слова сохраняются одним махом
    print(f"Добавлено слов: {added}")
finally:
    db.close()