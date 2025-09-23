import re


class AppValidationConstants:
    """
    Системные валидационные правила, REGEXP и проверки
    """

    EMAIL_REGEX_STR = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    TWELVE_DIGITS_REGEX_STR = r"^\d{12}$"
    BIN_REGEX_STR = r"^\d{12}$"
    IIN_REGEX_STR = r"^\d{12}$"
    KZ_MOBILE_REGEX_STR = r"^77\d{9}$"
    ONLY_RUSSIAN_KAZAKH_STR = r"^[\u0400-\u04FF0-9.,!? \-]+$"
    LOGIN_REGEX_STR = r"^[a-zA-Z0-9._@-]{3,255}$"
    PASSWORD_STR = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=]).{8,}$"
    ALATAY_ORDER_STR = r"^\d{6,22}$"

    def __init__(self) -> None:
        self.EMAIL_REGEX = re.compile(self.EMAIL_REGEX_STR)
        self.TWELVE_DIGITS_REGEX = re.compile(self.TWELVE_DIGITS_REGEX_STR)
        self.KZ_MOBILE_REGEX = re.compile(self.KZ_MOBILE_REGEX_STR)
        self.BIN_REGEX = re.compile(self.BIN_REGEX_STR)
        self.IIN_REGEX = re.compile(self.IIN_REGEX_STR)
        self.ONLY_RUSSIAN_KAZAKH_REGEX = re.compile(self.ONLY_RUSSIAN_KAZAKH_STR)
        self.LOGIN_REGEX = re.compile(self.LOGIN_REGEX_STR)
        self.PASSWORD_REGEX = re.compile(self.PASSWORD_STR)
        self.ALATAY_ORDER_REGEX = re.compile(self.ALATAY_ORDER_STR)


app_validation = AppValidationConstants()
