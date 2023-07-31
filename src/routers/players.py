from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..domain.player import service, schemas


router = APIRouter(
    prefix="/player",
    tags=["player"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.PlayerCreate, status_code=201)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return service.create_player(db=db, player=player)
