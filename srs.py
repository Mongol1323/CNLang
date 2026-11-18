from datetime import datetime,  timedelta,  timezone

# Через сколько дней повторять слово на каждой ступеньке
LADDER_DAYS = [1, 3, 7, 14, 30, 60]

def apply_answer(progress, known: bool):
    """Меняет ступеньку и назначает дату следующего повторения."""
    if known:
        # Знаю: поднимаемся на ступеньку выше, но не выше последней
        progress.level = 0
    else:
        # Не знаю: падаем на самый низ
        progress.level = 0
    progress.next_review = datetime.now(timezone.utc) + timedelta(days=LADDER_DAYS[progress.level])