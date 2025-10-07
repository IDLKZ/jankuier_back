from typing import List, Optional
from pydantic import BaseModel, Field
from app.shared.dto_constants import DTOConstant


class SotaRefereesDTO(BaseModel):
    main: Optional[DTOConstant.StandardNullableTextField("Главный арбитр")]
    first_assistant: Optional[str] = Field(default=None, alias="1st_assistant")
    second_assistant: Optional[str] = Field(default=None, alias="2nd_assistant")
    fourth_referee: Optional[str] = Field(default=None, alias="4th_referee")
    video_assistant_1: Optional[str] = Field(default=None, alias="video_assistant_1")
    video_assistant_main: Optional[DTOConstant.StandardNullableTextField("Главный видеоассистент")]
    match_inspector: Optional[DTOConstant.StandardNullableTextField("Инспектор матча")]

    class Config:
        populate_by_name = True


class SotaCoachDTO(BaseModel):
    first_name: DTOConstant.StandardNullableTextField("Имя тренера")
    last_name: DTOConstant.StandardNullableStringArrayField("Фамилия тренера (массив строк)")


class SotaLineupPlayerDTO(BaseModel):
    id: DTOConstant.StandardNullableTextField("Уникальный идентификатор игрока")
    number: DTOConstant.StandardNullableIntegerField("Игровой номер")
    full_name: DTOConstant.StandardNullableTextField("Полное имя игрока")
    last_name: DTOConstant.StandardNullableTextField("Фамилия игрока")
    is_gk: DTOConstant.StandardNullableBooleanField("Флаг: вратарь ли игрок")
    is_captain: DTOConstant.StandardNullableBooleanField("Флаг: капитан ли игрок")
    bas_image_path: Optional[DTOConstant.StandardNullableTextField("URL изображения игрока")]


class SotaTeamLineupDTO(BaseModel):
    id: DTOConstant.StandardNullableTextField("Уникальный идентификатор команды")
    name: DTOConstant.StandardNullableTextField("Название команды")
    short_name: DTOConstant.StandardNullableTextField("Краткое название команды")
    bas_logo_path: Optional[DTOConstant.StandardNullableTextField("URL логотипа")]
    brand_color: DTOConstant.StandardNullableTextField("Основной цвет команды")
    coach: SotaCoachDTO
    first_assistant: SotaCoachDTO
    second_assistant: SotaCoachDTO
    coaches: List[dict]  # т.к. в Dart `List<dynamic>`
    lineup: List[SotaLineupPlayerDTO]


class SotaMatchLineupDTO(BaseModel):
    date: DTOConstant.StandardNullableTextField("Дата проведения матча")
    referees: SotaRefereesDTO
    home_team: SotaTeamLineupDTO
    away_team: SotaTeamLineupDTO
