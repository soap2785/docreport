from typing import Optional, Dict, List
from traceback import format_exc, print_exc

from aiohttp import ClientSession

from time import time
from src.api.v1.parsing.models import ResponseData
from ...logger import Logger
from ...captcha import solveCaptcha


URL = 'https://pb.nalog.ru/'
CAPTCHA_VERSION = 3


class WarningListUCHR1:
    __info_logger = Logger()
    __error_logger = Logger('error')

    @staticmethod
    async def getCaptcha() -> tuple[str, str]:
        ''' Returns captcha's image URL and token '''
        currentTime = int(round(time() * 1000))
        async with ClientSession(URL) as client:
            captchaCode = await (
                await client.get(f'/static/captcha.bin?{currentTime}')
            ).text()
            return captchaCode, (
                f'{URL}/static/captcha.bin?r='
                f'{int(round(time() * 1000))}&a={captchaCode}'
                f'&version={CAPTCHA_VERSION}'
            )

    @staticmethod
    async def solver(token: str, solution: str) -> str:
        '''
        Send captcha's solution to the server.

        :param solution: Captcha solution
        :type solution: `str`
        :param token: Captcha token
        :type token: `str`

        :return: pbCaptchaToken solved captcha token.
        :rtype: `str`

        :raise: `ValueError` if solution is invalid.
        :raise: `ConnectionError` on server error
        '''
        async with ClientSession(URL) as client:
            async with client.post(
                'captcha-proc.json', data={
                    'captcha': solution, 'captchaToken': token
                }
            ) as response:
                if response.status != 200:
                    if (
                        response.get('ERRORS') and
                        response['ERRORS'].get('captcha')
                    ):
                        raise ValueError('Catcha solution is incorrect.')
                    raise ConnectionError('Server error.')
                return await response.text()

    @classmethod
    async def __checkTokens(
        cls, payload: Dict[str, str], tokens: List[str],
        dataset: Optional[List[List[str]]] = []
    ) -> List[str]:
        '''
        Get organizations status by it's tokens

        :param payload: A dictionary with POST data.
        :type payload: `dict[str, str]`

        :param tokens: Tokens.
        :type tokens: `list[str]`

        :param dataset: Optional: An existing list with organizations statuses.
        :type dataset: `list[list[str]]`

        :return: A list with organizations statuses.
        :rtype: `list[str]`
        '''
        async with ClientSession(URL) as client:
            for token in tokens:
                payload.update({'token': token})
                response = await (
                    await client.post('search-proc.json', data=payload)
                ).json()
                if payload.get('pbCaptchaToken'):
                    del payload['pbCaptchaToken']
                print(response)
                if response.get('ERROR') and response['ERROR'].get('captcha'):
                    captchaToken, captchaURL = await cls.getCaptcha()
                    payload.update(
                        {
                            'pbCaptchaToken': await cls.solver(
                                captchaToken, await solveCaptcha(captchaURL)
                            )
                        }
                    )
                    return await cls.__checkTokens(
                        payload, tokens[tokens.index(token):], dataset
                    )
                if not response.get('ul') or not response['ul'].get('data'):
                    continue

                response: dict[str, str] = response['ul']['data'][0]
                dataset.append(
                    [
                        response['namec'],
                        response['sulst_name_ex'],
                        response['inn']
                    ]
                )
        return dataset

    @classmethod
    async def __check(cls, data: str) -> List[str]:
        '''
        Main parser logic

        :param data: Search query.
        :type data: `str`

        :return: List with organizations statuses.
        :rtype: `list[str]`
        '''

        payload = {
            "mode": "search-upr-uchr", "mspUl1": "1", "mspUl2": "1",
            "mspUl3": "1", "mspIp1": "1", "mspIp2": "1", "mspIp3": "1",
            "queryUpr": data, 'queryUl': data, "uprType1": "1",
            "uprType0": "1", "ogrFl": "1", "ogrUl": "1",
            "npTypeDoc": "1", "page": "1", "pageSize": "10",
            "pbCaptchaToken": ''
        }

        async with ClientSession(URL) as client:
            async with client.post(
                'search-proc.json', data=payload
            ) as resp:
                response = await resp.json()

            if 'ERROR' in response:
                return

            async with client.post(
                'search-proc.json',
                data={"id": response['id'], "method": "get-response"}
            ) as resp:
                response = await resp.json()
                if response:
                    tokens = [
                        card['token'] for card in response['uchr']['data']
                    ][0:4]
                    return await cls.__checkTokens(payload, tokens)

    @classmethod
    async def check(cls, classObject: ResponseData, data: str) -> None:
        try:
            cls.__info_logger.info('WARNUCHR1', 1)
            response = await cls.__check(data)
            if response:
                classObject.warnuchr1 = response
            cls.__info_logger.info('WARNUCHR1', 2)
        except Exception:
            print_exc()
            cls.__info_logger.debug(format_exc())
