from pydantic import BaseModel


class PlayerBase(BaseModel):
    id: int
      
class PlayerCreate(BaseModel):
    name: str

class Player(PlayerBase):
    name: str

    class Config:
        from_attributes=True
    