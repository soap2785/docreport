from typing import Optional

from playwright.async_api import async_playwright, TimeoutError

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


class Arbitration:
    __error_logger = Logger('error')
    __info_logger = Logger()
    URL = "https://bankrot.fedresurs.ru/arbitrmanagers"

    def __init__(self) -> None:
        pass

    async def check(
        self, classObject: ResponseData,
        inn: Optional[int] = None, fullname: Optional[str] = None
    ) -> None:
        self.__info_logger.info('ARB', 1)
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
                    await page.locator(".ng-untouched").nth(4).fill(data)
                    await page.locator(".ng-untouched").nth(4).press("Enter")
                    (
                        await page.wait_for_selector
                        (".u-card-result_mb-standard", state='visible')
                    )
                    absList = []
                    for el in (
                        await page.locator(".u-card-result_mb-standard").all()
                    ):
                        tempList = []
                        try:
                            for value in (
                                await el.locator(".u-card-result__status")
                                .locator(".no-data").all_text_contents()
                            ):
                                tempList.append(value[1:-1])
                        except TimeoutError:
                            pass
                        try:
                            for value in (
                                await el.locator(".u-card-result__status")
                                .locator(".u-card-result__value_status")
                                .all_text_contents()
                            ):
                                if value:
                                    tempList.append(value[1:-1])
                        except TimeoutError:
                            pass
                        for value in (
                            await el.locator(".sro-am-data")
                            .locator(".u-card-result__sro")
                            .all_text_contents()
                        ):
                            tempList.append(value[1:-1])
                        for value in (
                            await el.locator(".sro-am-data")
                            .locator(".u-card-result__value_fw").nth(0)
                            .all_text_contents()
                        ):
                            tempList.append(value[1:-1])
                        for value in (
                            await el.locator(".sro-am-data")
                            .locator(".u-card-result__value_fw").nth(1)
                            .all_text_contents()
                        ):
                            tempList.append(value[1:-1])
                        for value in (
                            await el.locator(".u-card-result__court-case")
                            .locator(".u-card-result__value").nth(0)
                            .all_text_contents()
                        ):
                            tempList.append(value[1:-1])
                        for value in (
                            await el.locator(".u-card-result__court-case")
                            .locator(".u-card-result__value").nth(1)
                            .all_text_contents()
                        ):
                            tempList.append(value[1:-1])
                        if tempList:
                            absList.append(tempList)
                        self.__info_logger.info('ARB', 2)
                    if absList:
                        classObject.arb = absList
                        return
                except TimeoutError:
                    return
                except Exception as error:
                    self.__error_logger.error(str(error) + ' ARB')
