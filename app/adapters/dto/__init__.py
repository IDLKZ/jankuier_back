"""
DTO модели с поддержкой forward references.
Этот модуль обеспечивает правильную инициализацию всех DTO моделей.
"""

def rebuild_all_models():
    """Перестройка всех DTO моделей для разрешения forward references"""
    # Импортируем все модели сначала
    from app.adapters.dto.field.field_dto import FieldWithBasicRelationsRDTO, FieldWithRelationsRDTO
    from app.adapters.dto.field_party.field_party_dto import FieldPartyWithRelationsRDTO
    from app.adapters.dto.field_party_schedule_settings.field_party_schedule_settings_dto import FieldPartyScheduleSettingsRDTO
    from app.adapters.dto.academy.academy_dto import GetFullAcademyDTO
    from app.adapters.dto.academy_gallery.academy_gallery_dto import AcademyGalleryWithRelationsRDTO
    from app.adapters.dto.academy_group.academy_group_dto import AcademyGroupWithRelationsRDTO
    
    # Перестраиваем модели в правильном порядке
    # Сначала базовые модели без forward references
    FieldWithBasicRelationsRDTO.model_rebuild()
    FieldPartyScheduleSettingsRDTO.model_rebuild()
    AcademyGalleryWithRelationsRDTO.model_rebuild()
    AcademyGroupWithRelationsRDTO.model_rebuild()
    # Затем модели, которые используют базовые
    FieldPartyWithRelationsRDTO.model_rebuild()
    # Наконец, модели со сложными зависимостями
    FieldWithRelationsRDTO.model_rebuild()
    GetFullAcademyDTO.model_rebuild()


# Автоматическая перестройка при импорте модуля
rebuild_all_models()