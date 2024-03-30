from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from api.tanks.router import get_all_tanks_from_db, get_tank

router = APIRouter(
    prefix='/tanks',
    tags=['WEB Tanks']
)

templates = Jinja2Templates(directory='web/templates')


@router.get('/list')
async def get_tanks(request: Request, tanks=Depends(get_all_tanks_from_db)):
    return templates.TemplateResponse('index.html', {'request': request, 'tanks': tanks['data']})


@router.get('/{tank_name}')
async def get_tank_info(request: Request, tank=Depends(get_tank)):
    return templates.TemplateResponse('tank.html', {'request': request, 'tank': tank['data']})