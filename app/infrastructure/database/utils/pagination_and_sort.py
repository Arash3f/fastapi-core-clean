from collections.abc import Mapping
from enum import Enum
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shared.dto.pagination_dto import PaginatedResult
from app.domain.shared.dto.sorter_dto import SortOrderField


async def paginate_and_sort(
    *,
    model: type,
    stmt: Select,
    session: AsyncSession,
    page: int,
    page_size: int,
    sort_by: Enum,
    offset: int,
    sort_order: SortOrderField,
    sortable_columns: Mapping[Enum, Any],
) -> PaginatedResult[Any]:
    count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
    total = (await session.execute(count_stmt)).scalar_one()

    column = sortable_columns[sort_by]
    order_expr = column.desc() if sort_order == SortOrderField.DESC else column.asc()
    stmt = stmt.order_by(order_expr).offset(offset).limit(page_size)

    result = await session.execute(stmt)
    items = list(result.scalars().all())

    return PaginatedResult(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )
