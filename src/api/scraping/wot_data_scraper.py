import asyncio
from aiohttp import ClientSession

from api.scraping.config import TANK_LIST_URI, TYPE, LEVEL, TANK_INFO_URI, POSTFIX_LIST
from api.scraping.parser import parse_tank_specification, parse_guns


async def get_specification_json(url: str):
    async with ClientSession() as session:
        async with session.get(url=url) as response:
            tank_json = await response.json()
            return tank_json


async def get_tanks_slug() -> list[str]:
    async with ClientSession() as session:
        async with session.get(TANK_LIST_URI) as resp:
            tanks_info: dict = await resp.json()
            slugs: list[str] = [tank['slug'] for tank in tanks_info['tanks'] if tank['tier'] == LEVEL and
                                                                                tank['type'] == TYPE]
    return slugs


def delete_duplicates(postfixes: list[str], slug_list: list[str]) -> list[str]:
    i = 0
    while i < len(slug_list):
        for postfix in postfixes:
            if postfix in slug_list[i]:
                slug_list.remove(slug_list[i])
                i -= 1
                break
        i += 1
    return slug_list


async def get_response():
    slugs: list[str] = await get_tanks_slug()
    slugs = delete_duplicates(POSTFIX_LIST, slugs)

    ru_tanks: list[str] = [slug for slug in slugs if '-ru' in slug]
    eu_tanks: list[str] = [eu_slug for eu_slug in slugs for ru_slug in ru_tanks if eu_slug == ru_slug.replace('-ru', '')]
    for item in eu_tanks:
        slugs.remove(item)
    tank_uris: list[str] = [f'{TANK_INFO_URI}/{slug}' for slug in slugs]

    tasks = []
    for url in tank_uris:
        tasks.append(asyncio.create_task(get_specification_json(url)))
    result = await asyncio.gather(*tasks)
    return result


async def get_guns_info():
    tank_jsons = await get_response()
    gun_list = []
    for item in tank_jsons:
        gun_list.append(parse_guns(item))
    return gun_list


async def get_tanks_info():
    tank_jsons = await get_response()
    tank_list = []
    for item in tank_jsons:
        tank_list.append(parse_tank_specification(item))
    return tank_list
