from datetime import datetime, time, date
from decimal import Decimal
from typing import Annotated, Any, Text

from geoalchemy2 import Geometry
from sqlalchemy import (
    text,
    String,
    DateTime,
    Date,
    Time,
    BigInteger,
    Integer,
    SmallInteger,
    Boolean,
    ForeignKey,
    Computed,
    Numeric,
    ARRAY,
)
from sqlalchemy.dialects.postgresql import BYTEA, JSONB
from sqlalchemy.orm import mapped_column, relationship

from app.infrastructure.app_config import app_config
from app.shared.field_constants import FieldConstants


class DbColumnConstants:
    """
    Системные и унифицированный доступ к полям для Entities - Моделей Проекта
    """

    ID = Annotated[int, mapped_column(primary_key=True)]
    CreatedAt = Annotated[
        datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    ]
    UpdatedAt = Annotated[
        datetime,
        mapped_column(
            server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.now()
        ),
    ]
    DeletedAt = Annotated[
        datetime | None, mapped_column(DateTime(), nullable=True, default=None)
    ]
    # Аннотации для стандартных типов
    StandardVarchar = Annotated[
        str, mapped_column(String(length=FieldConstants.STANDARD_LENGTH))
    ]
    StandardVarcharIndex = Annotated[
        str, mapped_column(String(length=FieldConstants.STANDARD_LENGTH), index=True)
    ]
    StandardNullableVarchar = Annotated[
        str, mapped_column(String(length=FieldConstants.STANDARD_LENGTH), nullable=True)
    ]
    StandardNullableVarcharIndex = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), nullable=True, index=True
        ),
    ]
    StandardUniqueIIN = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.IIN_LENGTH), unique=True, index=True
        ),
    ]
    StandardIIN = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.IIN_LENGTH), unique=False, index=True
        ),
    ]
    StandardUniqueBIN = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.BIN_LENGTH), unique=True, index=True
        ),
    ]
    StandardBIN = Annotated[
        str,
        mapped_column(String(length=FieldConstants.BIN_LENGTH), index=True),
    ]
    StandardUniqueEmail = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), unique=True, index=True
        ),
    ]
    StandardEmail = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), unique=False, index=True
        ),
    ]
    StandardUniquePhone = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), unique=True, index=True
        ),
    ]
    StandardPhone = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_LENGTH), unique=False, index=True
        ),
    ]
    StandardUniqueValue = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_VALUE_LENGTH), unique=True, index=True
        ),
    ]
    StandardNotUniqueValue = Annotated[
        str,
        mapped_column(
            String(length=FieldConstants.STANDARD_VALUE_LENGTH),
            unique=False,
            index=True,
        ),
    ]
    StandardNullableText = Annotated[str, mapped_column(Text(), nullable=True)]
    StandardNullableBASE64 = Annotated[bytes, mapped_column(BYTEA(), nullable=True)]
    StandardText = Annotated[str, mapped_column(Text())]
    StandardPrice = Annotated[
        Decimal,
        mapped_column(
            Numeric(
                precision=FieldConstants.PRICE_PRECISION,
                scale=FieldConstants.PRICE_SCALE,
            )
        ),
    ]
    StandardZeroPrice = Annotated[
        Decimal,
        mapped_column(
            Numeric(
                precision=FieldConstants.PRICE_PRECISION,
                scale=FieldConstants.PRICE_SCALE,
            ),
            default=0.00,
        ),
    ]
    StandardNullablePrice = Annotated[
        Decimal | None,
        mapped_column(
            Numeric(
                precision=FieldConstants.PRICE_PRECISION,
                scale=FieldConstants.PRICE_SCALE,
            ),
            nullable=True,
        ),
    ]
    StandardDecimal = Annotated[
        Decimal,
        mapped_column(
            Numeric(
                precision=FieldConstants.PRICE_PRECISION,
                scale=FieldConstants.PRICE_SCALE,
            )
        ),
    ]
    StandardZeroDecimal = Annotated[
        Decimal,
        mapped_column(
            Numeric(
                precision=FieldConstants.PRICE_PRECISION,
                scale=FieldConstants.PRICE_SCALE,
            ),
            default=0.00,
        ),
    ]
    StandardNullableDecimal = Annotated[
        Decimal | None,
        mapped_column(
            Numeric(
                precision=FieldConstants.PRICE_PRECISION,
                scale=FieldConstants.PRICE_SCALE,
            ),
            nullable=True,
        ),
    ]

    StandardNullableDate = Annotated[date | None, mapped_column(Date(), nullable=True)]
    StandardDate = Annotated[date, mapped_column(Date())]
    StandardBirthDate = Annotated[date, mapped_column(Date())]
    StandardDateTime = Annotated[datetime, mapped_column(DateTime())]
    StandardNullableDateTime = Annotated[
        date | None, mapped_column(DateTime(), nullable=True)
    ]
    StandardNullableTime = Annotated[time | None, mapped_column(Time(), nullable=True)]
    StandardTime = Annotated[time, mapped_column(Time())]
    StandardTinyInteger = Annotated[int, mapped_column(SmallInteger())]
    StandardInteger = Annotated[int, mapped_column(Integer())]
    StandardBigInteger = Annotated[int, mapped_column(BigInteger())]
    StandardIntegerDefaultZero = Annotated[int, mapped_column(Integer(), default=0)]
    StandardNullableInteger = Annotated[
        int | None, mapped_column(Integer(), nullable=True)
    ]

    StandardBigIntegerDefaultZero = Annotated[
        int, mapped_column(BigInteger(), default=0)
    ]
    StandardNullableBigInteger = Annotated[
        int | None, mapped_column(BigInteger(), nullable=True)
    ]

    StandardBooleanTrue = Annotated[
        bool, mapped_column(Boolean(), nullable=False, default=True)
    ]
    StandardBooleanFalse = Annotated[
        bool, mapped_column(Boolean(), nullable=False, default=False)
    ]
    StandardBooleanNullable = Annotated[bool, mapped_column(Boolean(), nullable=True)]
    StandardBooleanNullableTrue = Annotated[
        bool, mapped_column(Boolean(), nullable=True, default=True)
    ]
    StandardBooleanNullableFalse = Annotated[
        bool, mapped_column(Boolean(), nullable=True, default=False)
    ]

    StandardArrayStringNullable = Annotated[
        str, mapped_column(ARRAY(String), nullable=True)
    ]

    StandardArrayString = Annotated[str, mapped_column(ARRAY(String))]
    StandardArrayIntegerNullable = Annotated[
        str, mapped_column(ARRAY(Integer), nullable=True)
    ]

    StandardArrayInteger = Annotated[str, mapped_column(ARRAY(Integer))]
    StandardNullableGeoPoint = Annotated[
        str | None,
        mapped_column(Geometry(geometry_type="POINT", srid=4326), nullable=True),
    ]
    StandardArrayDate = Annotated[list[datetime.date], mapped_column(ARRAY(Date))]
    StandardNullableArrayDate = Annotated[
        list[datetime.date] | None, mapped_column(ARRAY(Date), nullable=True)
    ]
    # ForeignKey унификации с onupdate и ondelete
    ForeignKeyInteger = (
        lambda table_name, onupdate=None, ondelete=None, foreign_column="id": Annotated[
            int,
            mapped_column(
                Integer(),
                ForeignKey(
                    f"{table_name}.{foreign_column}",
                    onupdate=onupdate,
                    ondelete=ondelete,
                ),
                nullable=False,
            ),
        ]
    )
    ForeignKeyNullableInteger = (
        lambda table_name, onupdate=None, ondelete=None, foreign_column="id": Annotated[
            int | None,
            mapped_column(
                Integer(),
                ForeignKey(
                    f"{table_name}.{foreign_column}",
                    onupdate=onupdate,
                    ondelete=ondelete,
                ),
                nullable=True,
            ),
        ]
    )

    ForeignKeyString = (
        lambda table_name, onupdate=None, ondelete=None, foreign_column="id": Annotated[
            str,
            mapped_column(
                String(length=255),
                ForeignKey(
                    f"{table_name}.{foreign_column}",
                    onupdate=onupdate,
                    ondelete=ondelete,
                ),
                nullable=False,
            ),
        ]
    )
    ForeignKeyNullableString = (
        lambda table_name, onupdate=None, ondelete=None, foreign_column="id": Annotated[
            str | None,
            mapped_column(
                String(length=255),
                ForeignKey(
                    f"{table_name}.{foreign_column}",
                    onupdate=onupdate,
                    ondelete=ondelete,
                ),
                nullable=True,
            ),
        ]
    )

    # Вычисляемые столбцы для Integer
    StandardComputedInteger = lambda table_exp, is_persisted=None: Annotated[
        int,
        mapped_column(
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            )
        ),
    ]

    # Вычисляемые столбцы для BigInteger
    StandardComputedBigInteger = lambda table_exp, is_persisted=None: Annotated[
        int,
        mapped_column(
            BigInteger(),
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            ),
        ),
    ]

    StandardComputedNullableInteger = lambda table_exp, is_persisted=None: Annotated[
        int | None,
        mapped_column(
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            ),
            nullable=True,
        ),
    ]

    # Вычисляемые столбцы для Float
    StandardComputedFloat = lambda table_exp, is_persisted=None: Annotated[
        float,
        mapped_column(
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            )
        ),
    ]

    StandardComputedNullableFloat = lambda table_exp, is_persisted=None: Annotated[
        float | None,
        mapped_column(
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            ),
            nullable=True,
        ),
    ]
    # Вычисляемые столбцы для Decimal
    StandardComputedDecimal = lambda table_exp, is_persisted=None: Annotated[
        Decimal,
        mapped_column(
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            )
        ),
    ]

    StandardComputedNullableDecimal = lambda table_exp, is_persisted=None: Annotated[
        Decimal | None,
        mapped_column(
            Computed(
                f"{table_exp}",
                persisted=is_persisted,
            ),
            nullable=True,
        ),
    ]

    StandardNullableJSONB = Annotated[dict | None, mapped_column(JSONB, nullable=True)]
    StandardJSONB = Annotated[dict, mapped_column(JSONB, nullable=False)]


class DbRelationshipConstants:
    @staticmethod
    def one_to_many(  # noqa:ANN205
        target: str,
        back_populates: str,
        foreign_keys: str | list | None = None,
        cascade: str = "none",
        lazy: str = "select",
        overlaps: str | None = None,
    ):
        """
        Унифицированное создание отношения один-ко-многим.

        Args:
            target (str): Целевая модель.
            back_populates (str): Связанное поле в целевой модели.
            foreign_keys (list): Список внешних ключей, если нужно.
            cascade (str): Стратегия каскадного удаления.
            lazy (str): Стратегия загрузки.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Настроенное отношение.
        """
        return relationship(
            target,
            back_populates=back_populates,
            foreign_keys=foreign_keys,
            cascade=cascade,
            lazy=lazy,
        )

    @staticmethod
    def one_to_one(  # noqa:ANN205
        target: str,
        back_populates: str,
        foreign_keys: str | list | None = None,
        cascade: str = "none",
        lazy: str = "select",
        overlaps: str | None = None,
    ):
        """
        Создает отношение один-к-одному.

        Args:
            target (str): Целевая модель.
            back_populates (str): Связанное поле в целевой модели.
            foreign_keys (list): Внешние ключи.
            cascade (str): Стратегия каскадирования.
            lazy (str): Стратегия загрузки данных.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Настроенное отношение.
        """
        return relationship(
            target,
            back_populates=back_populates,
            foreign_keys=foreign_keys,
            cascade=cascade,
            lazy=lazy,
            uselist=False,  # Ключевой параметр для один-к-одному
            overlaps=overlaps,
        )

    @staticmethod
    def many_to_one(  # noqa:ANN205
        target: str,
        back_populates: str,
        foreign_keys: str | list | None = None,
        cascade: str = "none",
        lazy: str = "select",
        overlaps: str | None = None,
    ):
        """
        Унифицированное создание отношения многие-к-одному.

        Args:
            target (str): Целевая модель.
            back_populates (str): Связанное поле в целевой модели.
            cascade (str): Стратегия каскадного удаления.
            lazy (str): Стратегия загрузки.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Настроенное отношение.
        """
        return relationship(
            target,
            back_populates=back_populates,
            cascade=cascade,
            lazy=lazy,
            foreign_keys=foreign_keys,
            overlaps=overlaps,
        )

    @staticmethod
    def many_to_many(  # noqa:ANN205
        target: str,
        secondary: str,
        back_populates: str,
        cascade: str = "all",
        lazy: str = "select",
        overlaps: str | None = None,
    ):
        """
        Унифицированное создание отношения многие-ко-многим.

        Args:
            target (str): Целевая модель.
            secondary (str): Связующая таблица для отношения многие-ко-многим.
            back_populates (str): Связанное поле в целевой модели.
            cascade (str): Стратегия каскадного удаления.
            lazy (str): Стратегия загрузки.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Настроенное отношение.
        """
        return relationship(
            target,
            secondary=secondary,
            back_populates=back_populates,
            cascade=cascade,
            lazy=lazy,
            overlaps=overlaps,
        )

    @staticmethod
    def self_referential(  # noqa:ANN205
        target: str,
        back_populates: str,
        foreign_keys: list | str | None = None,
        cascade: str = "none",
        lazy: str = "select",
        passive_deletes: bool = True,
        post_update: bool = True,
        remote_side: str | None = None,
        overlaps: str | None = None,
    ):
        """
        Creates a self-referential relationship.

        Args:
            target (str): The target model for the relationship.
            back_populates (str): The field in the target model to map back.
            foreign_keys (list): The foreign key(s) defining the relationship.
            cascade (str): Cascade behavior for the relationship.
            lazy (str): The loading strategy for the relationship.
            passive_deletes (bool): If True, avoids cascading deletes.
            post_update (bool): If True, synchronizes updates after a delete.
            remote_side (str): Specifies the "remote" side of the relationship.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Configured relationship.
        """
        return relationship(
            target,
            back_populates=back_populates,
            foreign_keys=foreign_keys,
            cascade=cascade,
            lazy=lazy,
            passive_deletes=passive_deletes,
            post_update=post_update,
            remote_side=remote_side,
            overlaps=overlaps,
        )

    @staticmethod
    def self_referential(  # noqa:ANN205,F811
        target: str,
        foreign_keys: list | str,
        remote_side: str,
        lazy: str = "select",
        cascade: str = "none",
        post_update: bool = True,
        overlaps: str | None = None,
    ):
        """
        Создаёт самоссылающееся отношение.

        Args:
            target (str): Имя целевой модели.
            foreign_keys (list): Внешние ключи для отношения.
            remote_side (str): Поле на удалённой стороне для установления связи.
            lazy (str): Стратегия загрузки.

        Returns:
            sqlalchemy.orm.RelationshipProperty: Настроенное отношение.
        """
        return relationship(
            target,
            foreign_keys=foreign_keys,
            remote_side=remote_side,
            lazy=lazy,
            cascade=cascade,
            post_update=post_update,
            overlaps=overlaps,
        )

    @staticmethod
    def one_to_many_with_condition(  # noqa:ANN205
        target: str,
        back_populates: str,
        foreign_keys: str | list | None = None,
        cascade: str = "none",
        lazy: str = "select",
        filter_condition: Any = None,  # <-- добавили!
        viewonly: bool = False,  # для фильтрованных связей
        overlaps: str | None = None,
    ):
        """
        Унифицированное создание отношения один-ко-многим с возможной фильтрацией.

        Args:
            target (str): Целевая модель.
            back_populates (str): Обратное поле.
            foreign_keys (list | str): Внешние ключи.
            cascade (str): Поведение каскада.
            lazy (str): Загрузка.
            filter_condition (Any): Условие фильтрации (primaryjoin).
            viewonly (bool): Только для чтения, без изменений.

        Returns:
            sqlalchemy.orm.RelationshipProperty
        """
        return relationship(
            target,
            back_populates=back_populates,
            foreign_keys=foreign_keys,
            cascade=cascade,
            lazy=lazy,
            primaryjoin=filter_condition,
            viewonly=viewonly if filter_condition else False,
            overlaps=overlaps,
        )


class DbComputedConstants:
    @property
    def trip_total_price(self) -> str:
        """Вычисление Total Price."""
        if app_config.app_database == "postgresql":
            return "(price + accommodation_price)::DOUBLE PRECISION"
        return "(price + accommodation_price)"


app_db_computed = DbComputedConstants()
