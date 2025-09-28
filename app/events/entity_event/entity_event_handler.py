from sqlalchemy import event
from sqlalchemy.orm import Mapper

class EntityEventHandler:
    """
    Базовый обработчик событий ORM.
    Чтобы слушать события, наследник должен вызвать register(cls).
    """

    @classmethod
    def register(cls, entity_cls):
        """Подключить слушатели к конкретной Entity"""
        event.listen(entity_cls, "before_insert", cls.before_insert)
        event.listen(entity_cls, "after_insert", cls.after_insert)
        event.listen(entity_cls, "before_update", cls.before_update)
        event.listen(entity_cls, "after_update", cls.after_update)
        event.listen(entity_cls, "before_delete", cls.before_delete)
        event.listen(entity_cls, "after_delete", cls.after_delete)

    # 🔹 Методы-хуки (по умолчанию ничего не делают)
    @staticmethod
    def before_insert(mapper: Mapper, connection, target): ...
    @staticmethod
    def after_insert(mapper: Mapper, connection, target): ...
    @staticmethod
    def before_update(mapper: Mapper, connection, target): ...
    @staticmethod
    def after_update(mapper: Mapper, connection, target): ...
    @staticmethod
    def before_delete(mapper: Mapper, connection, target): ...
    @staticmethod
    def after_delete(mapper: Mapper, connection, target): ...
