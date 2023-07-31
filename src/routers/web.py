from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=["Home"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

