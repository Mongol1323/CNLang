from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import security

from database import get_db, engine, Base
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.post("/words", response_model=schemas.WordOut)
def create_word(word: schemas.WordCreate, db: Session = Depends(get_db)):
    new_word = models.Word(**word.model_dump())
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word


@app.get("/words", response_model=list[schemas.WordOut])
def list_words(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.scalars(select(models.Word).offset(skip).limit(limit)).all()


@app.get("/words/{word_id}", response_model=schemas.WordOut)
def get_word(word_id: int, db: Session = Depends(get_db)):
    word = db.get(models.Word, word_id)
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    return word
@app.post("/register", response_model=schemas.UserOut)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    taken = db.scalar(select(models.User).where(models.User.username == data.username))
    if taken:
        raise HTTPException(status_code=400, detail="Это имя уже занято")

    user = models.User(
        username=data.username,
        hashed_password=security.hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(models.User).where(models.User.username == form.username))
    if user is None or not security.verify_password(form.password, user.hashed_password):
        # Одно и то же сообщение для обоих случаев, чтобы нельзя было угадывать имена
        raise HTTPException(status_code=401, detail="Неверное имя или пароль")

    token = security.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(security.get_current_user)):
    return current_user