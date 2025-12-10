from typing import Optional, Union
from asyncio import gather

from playwright.async_api import async_playwright

from src.api.v1.parsing.models import ResponseData
from ...logger import Logger
from ...captcha import solveCaptcha


class WarningListUCHR2:
    __error_logger = Logger(type='error')
    __info_logger = Logger()
    URL = 'https://pb.nalog.ru'

    def __init__(self) -> None:
        pass

    async def check(
        self, classObject: ResponseData,
        fullname: Optional[str] = None, inn: Optional[int] = None
    ) -> None:
        self.__info_logger.info('WARNUCHR2', 1)
        data = inn or fullname
        async with async_playwright() as p:
            try:
                print(1)
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
                    .locator('li').nth(3).click()
                )
                print(2)

                # Вводим данные
                await page.fill('#queryUpr', data)
                await page.press('#queryUpr', 'Enter')

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
                print(3)

                # Создаём range-объект с количеством анкет
                elements = range(len(
                    await page.locator('#resultuchr')
                    .locator('.pb-card--clickable').all()
                ))
                if len(elements) > 5:  # Максимальное кол-во элементов - 5
                    elements = range(5)

                # Запускаем кол-во браузеров, равное elements.
                # Возвращение к анкетам багованное
                await browser.close()
                print(4)
                for _ in range(5):
                    result = await self.compilewarn(data, elements)
                    self.__info_logger.info('WARNUCHR2', 2)
                    print(result)

                    if result:
                        classObject.warnuchr2 = result
                        return

            except Exception as error:
                self.__error_logger.error(str(error) + ' WARNUCHR2')

    async def checkCard(self, data: str | int, index: int) -> list:
        async with async_playwright() as p:
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
                .locator('li').nth(3).click()
            )

            # Вводим данные
            await page.fill('#queryUpr', data)
            await page.press('#queryUpr', 'Enter')

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
                ), (
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
                await page.wait_for_selector('#uniDialogFrame', state='hidden')
            except Exception:
                pass

            # Нажимаем на анкету
            (
                await page.locator('#resultuchr')
                .locator('.pb-card--clickable')
                .nth(index).click()
            )

            # Решаем капчу
            try:
                (
                    await page.wait_for_selector
                    ('#uniDialogFrame', state='visible')
                )
                img = 'https://pb.nalog.ru' + (
                    await page.frame_locator('#uniDialogFrame')
                    .locator('.mt-2').get_attribute('src')
                )
                captcha = await solveCaptcha(img)
                (
                    await page.frame_locator('#uniDialogFrame')
                    .locator('#captcha').fill(captcha)
                ), (
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

            tempList = []

            # Название компании
            tempList.append(await page.inner_text('.pb-card__title'))

            # Статус компании
            tempList.append(
                await page.locator('.pb-subject-status')
                .nth(0).inner_text()
            )

            # ИНН
            text = (
                await page.locator('.pb-items').nth(2).inner_text()
            )
            tempList.append(text.split()[1])
            return tempList

    @classmethod
    async def compilewarn(
        self, data: Union[str, int], elements: list[int]
    ) -> list:
        return await gather(
            *[
                WarningListUCHR2().checkCard(data, index)
                for index in elements
            ]
        )
