from random import randint
from base64 import b64decode
from os import remove as removeFile
from traceback import print_exc

from aiohttp import ClientSession
from ..config import TWOCAPTCHA_TOKEN
from twocaptcha import TwoCaptcha

captcha_solver = TwoCaptcha(TWOCAPTCHA_TOKEN)


async def solveCaptcha(url: str) -> str:
    captcha = f'captcha{randint(0, 1029301)}.png'
    for _ in range(10):
        try:
            if url.startswith('http'):
                async with ClientSession() as session:
                    async with session.get(url) as response:
                        with open(captcha, 'wb') as f:
                            f.write(await response.read())
            else:
                _, encodedData = url.split(",", 1)
                imageData = b64decode(encodedData)

                with open(captcha, "wb") as f:
                    f.write(imageData)
            return captcha_solver.normal(captcha)['code']
        except Exception:
            print_exc()
            continue
        finally:
            removeFile(captcha)
