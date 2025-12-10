from datetime import datetime
from random import randint
from os import makedirs
from logging import (
    ERROR, DEBUG, FileHandler, Formatter, Logger as Logger_
)


class Logger(Logger_):
    formatter = Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    def __init__(self, type: str = 'info') -> None:
        makedirs('app/logs', exist_ok=True)
        if type == 'info':
            super().__init__('info_logger' + str(randint(0, 100000)))
            self.setLevel(DEBUG)
            handler = FileHandler('app/logs/docreport.log')
        elif type == 'error':
            super().__init__('error_logger' + str(randint(0, 100000)))
            self.setLevel(ERROR)
            handler = FileHandler('app/logs/docreport.err.log')
        else:
            raise ValueError("Logger type must be either 'info' or 'error'")
        handler.setFormatter(self.formatter)
        self.addHandler(handler)

    def info(self, parser: str, count: int, *args, **kwargs) -> None:
        message = {
            (False, 1): f" {parser} parsing started",
            (False, 2): f" {parser} parsed successfully",
            (True, 1): " COMPILING started",
            (True, 2): " COMPILED successfully"
        }
        msg = message.get((parser == 'COMPILER', count))
        if msg:
            return super().info(f"[{datetime.now():%H:%M:%S}] {msg}", *args, **kwargs)
        return super().info(
            f'[{datetime.now():%H:%M:%S}] {parser} {count}', *args, **kwargs
        )
