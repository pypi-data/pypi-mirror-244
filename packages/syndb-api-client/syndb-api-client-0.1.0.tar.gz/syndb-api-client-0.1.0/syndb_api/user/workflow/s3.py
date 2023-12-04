from uuid import UUID

from botocore.client import BaseClient

from syndb_api.common.constant import S3_BUCKET_NAME_PROFILE_PICTURE, S3_PROFILE_PICTURE_FORMAT, S3_SIGNED_LINK_TTL


async def presigned_profile_picture_upload_url(s3: BaseClient, user_id: UUID) -> str:
    conditions = {"acl": "public-read", "Content-Type": "image/webp"}
    return await s3.generate_presigned_post(
        S3_BUCKET_NAME_PROFILE_PICTURE,
        f"{user_id}.{S3_PROFILE_PICTURE_FORMAT}",  # this is a full key now
        Fields=conditions,
        Conditions=[conditions, ["content-length-range", 0, 1000000]],
        ExpiresIn=S3_SIGNED_LINK_TTL,
    )
