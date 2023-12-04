from botocore.client import BaseClient
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from syndb_api.common.constant import S3_BUCKET_NAME_PROFILE_PICTURE, S3_PROFILE_PICTURE_FORMAT
from syndb_api.common.s3 import PreSignedS3Schema, get_s3_client, pre_signed_s3_download_url
from syndb_api.common.tags import Tags
from syndb_api.database.setup import get_db_read_async_session
from syndb_api.user.manager import bikipy_fastapi_users, database_auth_backend
from syndb_api.user.model import User
from syndb_api.user.schema import UserCreate, UserJustRead, UserProfile
from syndb_api.user.workflow.get import get_profile_from_scientist_tag, get_profile_info_model_from_id
from syndb_api.user.workflow.s3 import presigned_profile_picture_upload_url

user_router = APIRouter(tags=[Tags.user])

user_router.include_router(
    bikipy_fastapi_users.get_auth_router(database_auth_backend),
    tags=[Tags.user, Tags.auth],
    prefix="/auth/database",
)
user_router.include_router(
    bikipy_fastapi_users.get_register_router(UserJustRead, UserCreate),
)
user_router.include_router(
    bikipy_fastapi_users.get_verify_router(UserJustRead),
)
# user_router.include_router(
#     bikipy_fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
#     prefix="/auth/google",
#     tags=["auth"],
# )


profile_router = APIRouter(prefix="/profile")


@profile_router.get("/current", response_model=UserProfile)
async def current_user_profile(
    session: AsyncSession = Depends(get_db_read_async_session),
    user: User = Depends(bikipy_fastapi_users.current_user(active=True)),
    s3: BaseClient = Depends(get_s3_client),
):
    return await get_profile_info_model_from_id(session, s3, user.id)


@profile_router.get(
    "/{scientist_tag}",
    response_model=UserProfile,
    tags=[Tags.s3],
)
async def profile_from_scientist_tag(
    scientist_tag: str,
    session: AsyncSession = Depends(get_db_read_async_session),
    s3: BaseClient = Depends(get_s3_client),
):
    lookup_user = await get_profile_from_scientist_tag(session, scientist_tag)
    return dict(
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


@profile_router.post(
    "/current/set_scientist_tag",
    name="set_scientist_tag",
    status_code=status.HTTP_200_OK,
)
async def set_scientist_tag(
    scientist_tag: str,
    session: AsyncSession = Depends(get_db_read_async_session),
    user: User = Depends(bikipy_fastapi_users.current_user(active=True)),
):
    user.scientist_tag = scientist_tag
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with science tag {scientist_tag} already exists",
        )


@profile_router.post(
    "/current/upload_url_profile_picture",
    name="set_profile_picture",
    response_model=PreSignedS3Schema,
    tags=[Tags.s3],
)
async def create_upload_profile_picture(
    user: User = Depends(bikipy_fastapi_users.current_user(active=True)),
    s3: BaseClient = Depends(get_s3_client),
):
    return {"upload_url": await presigned_profile_picture_upload_url(s3, user.id)}


user_router.include_router(profile_router)
