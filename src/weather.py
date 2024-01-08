from urllib.parse import quote

import aiohttp
from bs4 import BeautifulSoup


class Weather:

    def __init__(self):
        self.host = "https://www.google.com/search?q="
        self.session = aiohttp.ClientSession()

    @property
    def headers(self) -> dict:
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    async def make_request(self, url: str) -> str:
        async with self.session.get(url, headers=self.headers) as resp:
            return await resp.text()
        
    async def get_weather(self, city: str):
        url = self.host + quote(f"погода в {city}")
        result = ""
        data = await self.make_request(url)
        bs = BeautifulSoup(data, "html.parser")
        taw = bs.find("div", {"id": "taw"})
        if taw:
            target = taw.text.split("Результаты:")[-1].replace("∙ Изменить регион", "").strip()
            result = f"Температура в городе {target}: "
        weather = bs.find("span", {"id": "wob_tm"})
        if weather:
            result += weather.text + "°C"
        else:
            return "Не удалось получить погоду в городе " + city
        return result
