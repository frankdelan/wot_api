from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from api.tanks.endpoints.tank import get_all_tanks_from_db, get_tank
from web.tanks.filter import filter_tanks

router = APIRouter(
    prefix='/tanks',
    tags=['WEB Tanks']
)

templates = Jinja2Templates(directory='web/templates')


@router.get('')
async def get_tanks(request: Request, tanks=Depends(get_all_tanks_from_db)):
    filtered_tanks = await filter_tanks(request, tanks['data'].copy())
    tanks_types = {tank.type for tank in filtered_tanks}
    return templates.TemplateResponse('tank_list.html', {'request': request,
                                                         'tanks': tanks['data'],
                                                         'filtered_tanks': filtered_tanks,
                                                         'tanks_types': tanks_types})


@router.get('/{tank_slug}')
async def get_tank_info(request: Request, tank=Depends(get_tank)):
    return templates.TemplateResponse('tank_info.html', {'request': request, 'tank': tank['data']})
