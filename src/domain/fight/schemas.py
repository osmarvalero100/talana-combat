from pydantic import BaseModel
from typing import Optional


class FightBase(BaseModel):
    id: int
      
class FightCreate(BaseModel):
    match: str
    combat: Optional[str] = None

class FightUpdateCombat(BaseModel):
    combat: str

class Fight(FightBase):
    match: str
    combat: Optional[str] = None
    winner: Optional[int] = None

    class Config:
        from_attributes = True
