class RequesterData:
    fullname: str = None
    region: str = None
    birthdate: str = None
    passport_series: str = None
    passport_number: str = None
    passport_date: str = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ResponseData:
    inn: int
    fns: str = 'Данные не обнаружены'
    ter: str = 'Данные не обнаружены'
    civ: list | str = 'Данные не обнаружены'
    bank: dict = 'Данные не обнаружены'
    iss: list | str = 'Данные не обнаружены'
    warnip: list | str = 'Данные не обнаружены'
    warnorg: list | str = 'Данные не обнаружены'
    warnuchr1: list | str = 'Данные не обнаружены'
    warnuchr2: list | str = 'Данные не обнаружены'
    disq: dict | str = 'Данные не обнаружены'
    semp: str = 'Данные не обнаружены'
    inter: str = 'Данные не обнаружены'
    mass: str = 'Данные не обнаружены'
    arb: list | str = 'Данные не обнаружены'
    org: list | str = 'Данные не обнаружены'
    law: list = 'Данные не обнаружены'
    vk: list | str = 'Данные не обнаружены'
    ok: list | str = 'Данные не обнаружены'

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
