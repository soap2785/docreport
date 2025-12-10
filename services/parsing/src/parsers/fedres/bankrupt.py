from typing import Optional

from playwright.async_api import async_playwright, TimeoutError

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


class Bankrupt:
    __error_logger = Logger('error')
    __info_logger = Logger()
    URL = 'https://bankrot.fedresurs.ru/bankrupts'

    def __init__(self) -> None:
        pass

    async def check(
        self, classObject: ResponseData,
        inn: Optional[int] = None, fullname: Optional[str] = None
    ) -> None:
        self.__info_logger.info('BANK', 1)
        data = inn or fullname
        for _ in range(10):
            async with async_playwright() as p:
                try:
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/91.0.4472.124 Safari/537.36"
                    )
                    page = await context.new_page()
                    await page.goto(self.URL, wait_until="domcontentloaded")
                    await page.locator('input').nth(1).fill(data)
                    await page.locator('input').nth(1).press("Enter")
                    absList = []
                    (
                        await page.wait_for_selector
                        (".u-card-result__wrapper", state='visible')
                    )
                    for element in (
                        await page.locator(".u-card-result__wrapper").all()
                    ):
                        tempList = []
                        tempList.append(
                            await element.locator
                            (".u-card-result__value").nth(4)
                            .text_content()
                        )
                        tempList.append(
                            await element.locator(".u-card-result__value_adr")
                            .text_content()
                        )
                        tempList.append(
                            await element.locator(".status-date")
                            .text_content()
                        )
                        tempList.append(
                            await element.locator
                            (".u-card-result__value_item-property")
                            .text_content()
                        )
                        if tempList:
                            absList.append(tempList)
                    if absList:
                        classObject.bank = absList
                        return
                    self.__info_logger.info('BANK', 2)
                except IndexError:
                    pass
                except TimeoutError:
                    return
                except Exception as error:
                    self.__error_logger.error(str(error) + ' BANK')
