import json
from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import repository, schemas, models
from ..player import service as player_service
from resources.constants import DEFAULT_PLAYERS, ENERGY
from resources.strings import FIGTH_DOES_NOT_EXIST_ERROR


def create_fight(db: Session, fight: schemas.Fight):
    if (fight.match == ""):
        player1 = player_service.get_player_by_name(db, DEFAULT_PLAYERS[0])
        if player1 is None:
            player_service.load_players(db)
        player1 = player_service.get_player_by_name(db, DEFAULT_PLAYERS[0])
        player2 = player_service.get_player_by_name(db, DEFAULT_PLAYERS[1])

    fight.match = f"{player1.id}vs{player2.id}"
    combat = {
                "player1": {
                    "movimientos": [],
                    "golpes": [],
                    "attackMode": 1,
                    "player_id": player1.id,
                    "name": player1.name,
                    "energy": ENERGY
                },
                "player2": {
                    "movimientos": [],
                    "golpes": [],
                    "attackMode": 1,
                    "player_id": player2.id,
                    "name": player2.name,
                    "energy": ENERGY
                }
            }
    fight.combat = str(json.dumps(combat))

    return repository.create_fight(db, fight)

def get_fight(db: Session, id: int):
    figth = repository.get_fight(db, id)
    if figth is None:
        raise HTTPException(status_code=404, detail=FIGTH_DOES_NOT_EXIST_ERROR)
    return figth

def update_combat(db: Session, id: int, combat: str):
    figth = models.Fight()
    dictCombat = json.loads(combat)
    dictCombatUpdated = figth.update_energy_players_in_fight(dictCombat)
    combat = str(json.dumps(dictCombatUpdated))
    figth = repository.update_combat(db, id, combat)
    winner = figth.check_winner([dictCombatUpdated["player1"], dictCombatUpdated["player2"]])
    if winner is not None:
        if len(winner) == 1 and winner[0]["player_id"] > 0:
            repository.update_winner(db, id, winner[0]["player_id"])

    if figth is None:
        raise HTTPException(status_code=404, detail=FIGTH_DOES_NOT_EXIST_ERROR)
    return figth