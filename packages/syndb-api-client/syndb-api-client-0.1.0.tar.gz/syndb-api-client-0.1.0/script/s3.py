import asyncio

import aioboto3

from syndb_api.common.s3 import connection_kwargs
from syndb_api.user.workflow.s3 import presigned_profile_picture_upload_url


async def p_url():
    session = aioboto3.Session()
    async with session.client(**connection_kwargs) as s3_client:
        t = await presigned_profile_picture_upload_url(s3_client, "0648fdda-73b2-7892-8000-1c0b904bf6dd")

    print(t)


asyncio.run(p_url())
