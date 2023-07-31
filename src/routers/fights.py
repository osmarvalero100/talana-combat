from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..domain.fight import service, schemas


router = APIRouter(
    prefix="/fight",
    tags=["fight"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}", response_model=schemas.Fight)
def read_fight(id: int, db: Session = Depends(get_db)):
    return service.get_fight(db, id=id)

@router.post("/", response_model=schemas.Fight, status_code=201)
def create_fight(fight: schemas.FightCreate, db: Session = Depends(get_db)):
    return service.create_fight(db=db, fight=fight)

@router.patch("/{id}", response_model=schemas.Fight, status_code=201)
def update_combat(id: int, fight: schemas.FightUpdateCombat, db: Session = Depends(get_db)):
    return service.update_combat(db=db, id=id, combat=fight.combat)
