from datetime import datetime

from playwright.async_api import async_playwright

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


class SelfEmployed:
    __error_logger = Logger('error')
    __info_logger = Logger()
    URL = "https://npd.nalog.ru/check-status/"

    @classmethod
    async def check(cls, inn: int, classObject: ResponseData) -> None:
        cls.__info_logger.info('SEMP', 1)
        if not inn:
            return
        formatted_date = datetime.strftime(datetime.today(), "%d-%m-%Y")
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
                page = await context.new_page()
                await page.goto(cls.URL, wait_until='domcontentloaded')
                await page.fill("#ctl00_ctl00_tbINN", str(inn))
                await page.fill("#ctl00_ctl00_tbDate", formatted_date)
                await page.press("#ctl00_ctl00_tbDate", 'Enter')
                async with page.expect_navigation(wait_until="networkidle"):
                    await page.click("#ctl00_ctl00_btSend")
                (
                    await page.wait_for_selector
                    ("#ctl00_ctl00_lblInfo", state="attached", timeout=10000)
                )
                classObject.semp = (
                    await page.inner_text
                    ("#ctl00_ctl00_lblInfo")
                )
                await browser.close()
                cls.__info_logger.info('SEMP', 2)
            except Exception as error:
                cls.__error_logger.error(str(error) + ' SEMP')
