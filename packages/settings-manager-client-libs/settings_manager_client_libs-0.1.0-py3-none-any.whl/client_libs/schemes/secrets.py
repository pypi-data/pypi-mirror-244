from pydantic import BaseModel, ConfigDict


class SecretsModelStruct(BaseModel):
    """
    Представляет структуру модели секретов.

    :param id (uuid.UUID): Уникальный идентификатор секрета.
    :param model_config (ConfigDict): Словарь конфигурации для модели.
    :param key: Ключ к секрету.
    :param value: Значение секрета.
    """

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    key: str
    value: str
