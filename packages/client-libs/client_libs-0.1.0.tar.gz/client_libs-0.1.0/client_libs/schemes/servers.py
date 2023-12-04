from __future__ import annotations

import configparser
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .secrets import SecretsModelStruct
from .systems import SystemModelStruct


class ServerModelStruct(BaseModel):
    """
     Представляет структуру модели сервера.

    :param id (uuid.UUID): Уникальный идентификатор сервера.
    :param model_config (ConfigDict): Словарь конфигурации для модели.
    :param name (str, optional): Название модели сервера.
    :param description (str, optional): Описание модели сервера.
    :param systems (list[SystemModelStruct]): Список структур модели системы, связанных с моделью сервера.
    """

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    name: Optional[str] = None
    description: Optional[str] = None
    systems: list[SystemModelStruct] = []

    @classmethod
    def from_ini_file(cls, filename, server_name) -> ServerModelStruct:
        config = configparser.ConfigParser()
        config.read(filename)

        server: ServerModelStruct = cls(name=server_name)
        for el in config.sections():
            system = SystemModelStruct()
            system.name = el
            for sec in config[el]:
                system.secrets.append(
                    SecretsModelStruct(
                        key=sec,
                        value=config[el][sec],
                    ),
                )
            server.systems.append(system)

        return server
