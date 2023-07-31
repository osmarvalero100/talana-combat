from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas
from resources.strings import FIGTH_DOES_NOT_EXIST_ERROR


def create_fight(db: Session, fight: schemas.FightCreate):
    db_fight = models.Fight(**fight.dict())
    db.add(db_fight)
    db.commit()
    db.refresh(db_fight)

    return db_fight

def get_fight(db: Session, id: int):
    return db.query(models.Fight).filter(models.Fight.id == id).first()

def update_winner(db: Session, id: int, winner: int):
    db_fight = db.query(models.Fight).filter(models.Fight.id == id).first()

    if db_fight is None:
        raise HTTPException(status_code=404, detail=FIGTH_DOES_NOT_EXIST_ERROR)
    
    db_fight.winner = winner
    db.add(db_fight)
    db.commit()
    db.refresh(db_fight)

    return db_fight

def update_combat(db: Session, id: int, combat: str):
    db_fight = db.query(models.Fight).filter(models.Fight.id == id).first()

    if db_fight is None:
        raise HTTPException(status_code=404, detail=FIGTH_DOES_NOT_EXIST_ERROR)
    
    db_fight.combat = combat
    db.add(db_fight)
    db.commit()
    db.refresh(db_fight)

    return db_fight

