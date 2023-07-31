from fastapi import APIRouter
from . import fights, players

router = APIRouter()

def include_api_routes():
    ''' Include to router all api rest routes with version prefix '''
    router.include_router(players.router)
    router.include_router(fights.router)

include_api_routes()