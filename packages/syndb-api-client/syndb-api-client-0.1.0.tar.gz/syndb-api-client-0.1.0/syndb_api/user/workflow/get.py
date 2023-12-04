from uuid import UUID

from botocore.client import BaseClient
from fastapi import HTTPException
from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from syndb_api.common.constant import S3_BUCKET_NAME_PROFILE_PICTURE, S3_PROFILE_PICTURE_FORMAT
from syndb_api.common.s3 import pre_signed_s3_download_url
from syndb_api.user.model import User
from syndb_api.user.schema import UserProfile


def _error_if_no_row(lookup_user, lookup_string: str):
    if not lookup_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {lookup_string} could not be found",
        )


async def get_profile_from_scientist_tag(session: AsyncSession, scientist_tag: str) -> Row:
    lookup_user = (
        await session.execute(
            select(User.scientist_tag, User.is_superuser, User.has_profile_picture).where(
                User.scientist_tag == scientist_tag
            )
        )
    ).one_or_none()

    _error_if_no_row(lookup_user, f"scientist_tag={scientist_tag}")

    return lookup_user


async def get_profile_from_id(session: AsyncSession, user_id: UUID | str) -> Row:
    lookup_user = (
        await session.execute(
            select(User.scientist_tag, User.is_superuser, User.has_profile_picture).where(User.id == user_id)
        )
    ).one_or_none()

    _error_if_no_row(lookup_user, f"id={user_id}")

    return lookup_user


async def get_profile_info_model_from_id(session: AsyncSession, s3: BaseClient, user_id: UUID | str) -> UserProfile:
    lookup_user = await get_profile_from_id(session, user_id)
    return UserProfile(
        id=lookup_user.id,
        scientist_tag=lookup_user.scientist_tag,
        is_superuser=lookup_user.is_superuser,
        profile_picture_link=await pre_signed_s3_download_url(
            s3,
            S3_BUCKET_NAME_PROFILE_PICTURE,
            f"{lookup_user.id}.{S3_PROFILE_PICTURE_FORMAT}",
        )
        if lookup_user.has_profile_picture
        else None,
    )
