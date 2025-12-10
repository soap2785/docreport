from typing import Optional

from playwright.async_api import async_playwright, TimeoutError

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


class Organizer:
    __error_logger = Logger('error')
    __info_logger = Logger()
    URL = "https://bankrot.fedresurs.ru/tradeorgs"

    def __init__(self) -> None:
        pass

    async def check(
        self, classObject: ResponseData,
        inn: Optional[int] = None, fullname: Optional[str] = None
    ) -> None:
        self.__info_logger.info('ORG', 1)
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
                    await page.goto(self.URL, wait_until='domcontentloaded')
                    await page.locator(".ng-untouched").nth(4).fill(data)
                    await page.locator(".ng-untouched").nth(4).press("Enter")
                    (
                        await page.wait_for_selector
                        ('.u-card-result_mb-standard', state="visible")
                    )
                    absList = []
                    for element in (
                        await page.locator(".u-card-result_mb-standard").all()
                    ):
                        tempList = []
                        tempList.append(
                            await element.locator
                            (".u-card-result__content_item-2").inner_text()
                        )
                        text, = (
                            await element.locator(".u-card-result__court-case")
                            .all_inner_texts()
                        )
                        tempList.extend(x for x in text.split() if x.isdigit())
                        if tempList:
                            absList.append(tempList)
                    if absList:
                        classObject.org = absList
                        return
                    self.__info_logger.info('ORG', 2)
                except TimeoutError:
                    return
                except Exception as error:
                    self.__error_logger.error(f"{error} ORG")
