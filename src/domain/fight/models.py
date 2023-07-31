from sqlalchemy import Column, Integer, String, Text

from ...database import Base
from resources.constants import ENERGY, COMBINATIONS_PLAYERS


class Fight(Base):
    __tablename__ = "fights"

    id = Column(Integer, primary_key=True, index=True)
    match = Column(String)
    winner = Column(Integer)
    combat = Column(Text, index=True)

    def get_energy_opponent(self, attack: dict, attacker: int):
        playerEnergy = ENERGY
        player = f"player{attacker}"
        moves = attack["moves"]
        hits = attack["hits"]

        for i, move in enumerate(moves):
            hit = hits[i]
            attack = move + hit
            print(attack)
            
            if attack in COMBINATIONS_PLAYERS[player]:
                playerEnergy -= COMBINATIONS_PLAYERS[player][attack]['energy']
            
            if playerEnergy < 1:
                return 0

        if len(hits) > len(moves):
            for hit in hits[len(moves):]:
                if hit in COMBINATIONS_PLAYERS[player]:
                    playerEnergy -= COMBINATIONS_PLAYERS[player][hit]['energy']
                    if playerEnergy < 1:
                        return 0
                    
        return playerEnergy

    def update_energy_players_in_fight(self, combat: dict):
        player1 = combat["player1"]
        player2 = combat["player2"]
        
        player2Acttack = {
            "moves": player2["movimientos"],
            "hits": player2["golpes"]
        }
        energyPlayer1 = self.get_energy_opponent(player2Acttack, player2["player_id"])
        combat["player1"]["energy"] = energyPlayer1

        player1Acttack = {
            "moves": player1["movimientos"],
            "hits": player1["golpes"]
        }
        energyPlayer2 = self.get_energy_opponent(player1Acttack, player1["player_id"])
        combat["player2"]["energy"] = energyPlayer2

        return combat
    
    def check_winner(self, players: list):
        if players[0]["energy"] > 0 and players[1]["energy"]:
            return None
        winner = list(filter(lambda player: player['energy'] > 0 , players))

        return winner





        


