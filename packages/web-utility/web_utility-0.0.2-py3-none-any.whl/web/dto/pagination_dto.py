from typing import Any

from app.dto.common_dto import CommonDto


class PaginationDto(CommonDto):
    page: int
    total: int
    items: list[Any]