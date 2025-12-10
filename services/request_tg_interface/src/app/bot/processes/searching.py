from app.bot.states import RequesterData

from aiohttp import ClientSession
from random import randint as rnt
from .logger import Logger


async def StartOSINT(data: dict | str) -> str:
    req = RequesterData(**data)
    async with ClientSession('http://parsing:9101/api/v1/') as resp:
        request_to_parsing = {
            "id": req.order,
            "fullname": req.fullname,
            "region": req.region,
            "birthdate": req.birthdate,
            "passport_series": req.passport_series,
            "passport_number": req.passport_number,
            "passport_date": req.passport_date
        }
        result = (
            await (await resp.post('parsing/', json=request_to_parsing)).json()
        )['response_data_dict']
    async with ClientSession('http://generation:9103/api/v1/') as resp:
        query = {
            "requester": req.__dict__,
            "response": result
        }
        Logger().debug(query)
        response = await resp.post('generating/', json=query)
        content = await response.read()
        file = f"/app/report{rnt(0, 1000)}.pdf"
        with open(file, "wb") as fp:
            fp.write(content)
        return file
