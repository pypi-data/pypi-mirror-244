from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

if TYPE_CHECKING:
    from syndb_api.user.model import OwnerGroup


async def resolve_groups_from_names(session: AsyncSession, group_names: list[str]) -> list["OwnerGroup"]:
    from syndb_api.user.model import OwnerGroup

    if group_names:
        groups = (await session.scalars(select(OwnerGroup).where(OwnerGroup.name.in_(group_names)))).all()
        if len(groups) != len(group_names):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataset, with names {(', '.join(g.name for g in groups))}, could not be found",
            )
    else:
        groups = []

    return groups
