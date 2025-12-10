class RequesterData:
    order: int
    fullname: str
    region: str
    birthdate: str
    passport_series: str
    passport_number: str
    passport_date: str

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
