from pydantic import BaseModel
from app.adapters.dto.file.file_dto import FileRDTO
from app.adapters.dto.pagination_dto import BasePageModel
from app.shared.dto_constants import DTOConstant


class StudentDTO(BaseModel):
    id: DTOConstant.StandardID()

    class Config:
        from_attributes = True


class StudentCDTO(BaseModel):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID фотографии студента"
    )
    created_by: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID пользователя, создавшего студента"
    )
    first_name: DTOConstant.StandardVarcharField(description="Имя")
    last_name: DTOConstant.StandardVarcharField(description="Фамилия")
    patronymic: DTOConstant.StandardNullableVarcharField(description="Отчество")
    birthdate: DTOConstant.StandardDateField(description="Дата рождения")
    reschedule_end_at: DTOConstant.StandardNullableDateTimeField(
        description="Дата окончания переноса"
    )
    gender: DTOConstant.StandardTinyIntegerField(
        description="Пол: 0-оба, 1-мужской, 2-женский"
    )
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон")
    additional_phone: DTOConstant.StandardNullableVarcharField(
        description="Дополнительный телефон"
    )
    email: DTOConstant.StandardNullableVarcharField(description="Email")
    info: DTOConstant.StandardNullableTextField(description="Дополнительная информация")

    class Config:
        from_attributes = True


class StudentRDTO(StudentDTO):
    image_id: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID фотографии студента"
    )
    created_by: DTOConstant.StandardNullableUnsignedIntegerField(
        description="ID пользователя, создавшего студента"
    )
    first_name: DTOConstant.StandardVarcharField(description="Имя")
    last_name: DTOConstant.StandardVarcharField(description="Фамилия")
    patronymic: DTOConstant.StandardNullableVarcharField(description="Отчество")
    birthdate: DTOConstant.StandardDateField(description="Дата рождения")
    reschedule_end_at: DTOConstant.StandardNullableDateTimeField(
        description="Дата окончания переноса"
    )
    gender: DTOConstant.StandardTinyIntegerField(
        description="Пол: 0-оба, 1-мужской, 2-женский"
    )
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон")
    additional_phone: DTOConstant.StandardNullableVarcharField(
        description="Дополнительный телефон"
    )
    email: DTOConstant.StandardNullableVarcharField(description="Email")
    info: DTOConstant.StandardNullableTextField(description="Дополнительная информация")

    created_at: DTOConstant.StandardCreatedAt
    updated_at: DTOConstant.StandardUpdatedAt

    class Config:
        from_attributes = True


class StudentWithRelationsRDTO(StudentRDTO):
    image: FileRDTO | None = None

    class Config:
        from_attributes = True


class StudentUpdateDTO(BaseModel):
    """DTO для обновления студента - все поля опциональные"""

    image_id: (
        DTOConstant.StandardNullableUnsignedIntegerField(
            description="ID фотографии студента"
        )
        | None
    ) = None
    first_name: DTOConstant.StandardVarcharField(description="Имя") | None = None
    last_name: DTOConstant.StandardVarcharField(description="Фамилия") | None = None
    patronymic: (
        DTOConstant.StandardNullableVarcharField(description="Отчество") | None
    ) = None
    birthdate: DTOConstant.StandardDateField(description="Дата рождения") | None = None
    reschedule_end_at: (
        DTOConstant.StandardNullableDateTimeField(description="Дата окончания переноса")
        | None
    ) = None
    gender: (
        DTOConstant.StandardTinyIntegerField(
            description="Пол: 0-оба, 1-мужской, 2-женский"
        )
        | None
    ) = None
    phone: DTOConstant.StandardNullableVarcharField(description="Телефон") | None = None
    additional_phone: (
        DTOConstant.StandardNullableVarcharField(description="Дополнительный телефон")
        | None
    ) = None
    email: DTOConstant.StandardNullableVarcharField(description="Email") | None = None
    info: (
        DTOConstant.StandardNullableTextField(description="Дополнительная информация")
        | None
    ) = None

    class Config:
        from_attributes = True


class PaginationStudentRDTO(BasePageModel):
    items: list[StudentRDTO]


class PaginationStudentWithRelationsRDTO(BasePageModel):
    items: list[StudentWithRelationsRDTO]
