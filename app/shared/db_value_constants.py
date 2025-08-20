from slugify import slugify

from app.shared.field_constants import FieldConstants


class DbValueConstants:
    # Роли
    AdminRoleConstantID = 1
    AdminRoleConstantValue = "system_admin"

    ClientRoleConstantID = 2
    ClientRoleConstantValue = "client"

    # Языки
    RussianLanguageConstantID = 1
    RussianLanguageConstantValue = "russian_language"
    KazakhLanguageConstantID = 2
    KazakhLanguageConstantValue = "kazakh_language"
    EnglishLanguageConstantID = 3
    EnglishLanguageConstantValue = "english_language"

    @staticmethod
    def get_value(title: str):
        return slugify(
            title,
            max_length=FieldConstants.STANDARD_VALUE_LENGTH,
            separator="_",
            lowercase=True,
        )
