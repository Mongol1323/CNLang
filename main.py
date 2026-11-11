from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

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