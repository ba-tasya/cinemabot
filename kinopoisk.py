import aiohttp
from urllib.parse import quote
import typing as tp
from config import X_API_KEY


async def film2info(film: str) -> tp.Dict[str, tp.Any]:
    film_encoded = quote(film)
    url = f"http://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={film_encoded}"
    headers = {'accept': 'application/json', 'X-API-KEY': X_API_KEY}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            json_body = await r.json()
            # print(json_body)
            return json_body
