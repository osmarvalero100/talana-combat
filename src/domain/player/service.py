from sqlalchemy.orm import Session

from . import repository, schemas, models
from resources.constants import DEFAULT_PLAYERS

def get_player_by_name(db: Session, name: str):
    return repository.get_player_by_name(db, name)


def create_player(db: Session, player: schemas.Player):
    return repository.create_player(db, player)

def load_players(db: Session):
    player = models.Player()
    player1 = get_player_by_name(db, DEFAULT_PLAYERS[0])
    if player1 is None:
        player.name = DEFAULT_PLAYERS[0]
        player1 = create_player(db, player)

    player2 = get_player_by_name(db, DEFAULT_PLAYERS[1])
    if player2 is None:
        player.name = DEFAULT_PLAYERS[1]
        player2 = create_player(db, player)