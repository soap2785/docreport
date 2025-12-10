from typing import Optional
from asyncio import sleep as asleep

from playwright.async_api import async_playwright

from src.api.v1.parsing.models import ResponseData
from ...logger import Logger
from ...captcha import solveCaptcha


class WarningListIP:
    __error_logger = Logger('error')
    __info_logger = Logger()
    URL = 'https://pb.nalog.ru/'

    def __init__(self) -> None:
        pass

    async def check(
        self, classObject: ResponseData,
        fullname: Optional[str] = None, inn: Optional[int] = None
    ) -> None:
        self.__info_logger.info('WARNIP', 1)
        data = inn or fullname
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
                page = await context.new_page()

                # Устанавливаем размер окна иначе не выберем категорию поиска
                await page.set_viewport_size({"width": 800, "height": 600})

                await page.goto(self.URL, wait_until='domcontentloaded')

                # Нажимаем на выпадающий список "Общий поиск" и выбираем ИП
                await page.click('#btnSelectMode')
                (
                    await page.locator('.dropdown-menu').nth(1)
                    .locator('li').nth(2).click()
                )

                # Вводим данные
                await page.fill('#queryIp', data),
                await page.press('#queryIp', 'Enter')

                # Решаем капчу
                try:
                    img = 'https://pb.nalog.ru' + (
                        await page.frame_locator('#uniDialogFrame')
                        .locator('.mt-2').get_attribute('src')
                    )
                    captcha = await solveCaptcha(img)
                    (
                        await page.frame_locator('#uniDialogFrame')
                        .locator('#captcha').fill(captcha)
                    )
                    await asleep(5)
                    (
                        await page.frame_locator('#uniDialogFrame')
                        .locator('#btnOk').click()
                    )

                    # Ловим ошибку Цифры с картинки введены неверно
                    for _ in range(10):
                        if (
                            await page.frame_locator('#uniDialogFrame')
                            .locator('.u3-error').inner_text()
                        ):
                            (
                                await page.frame_locator('#uniDialogFrame')
                                .locator('#btnOk').click()
                            )
                        else:
                            break
                except Exception:
                    pass
                (
                    await page.wait_for_selector
                    ('.pb-card--clickable', state='visible')
                )

                # Переходим к основной информации по лицу
                absList = []  # Все анкеты на лицо
                for card in await page.locator('.pb-card--clickable').all():
                    if len(absList) == 5:  # Максиальное кол-во анкет - 5
                        break
                    tempList = []  # Информация в анкете

                    # Статус ИП
                    tempList.append(
                        await card.locator('.pb-subject-status').nth(0)
                        .inner_text()
                    )

                    # ИНН
                    items = await card.locator('.pb-items').nth(2).inner_text()
                    for item in items.split():
                        if len(item) == 12:
                            tempList.append(item)

                    if tempList:
                        absList.append(tempList)
                if absList:
                    classObject.warnip = absList
                    return absList
                self.__info_logger.info('WARNIP', 2)
            except Exception as error:
                self.__error_logger.error(f"{error} WARNIP")
