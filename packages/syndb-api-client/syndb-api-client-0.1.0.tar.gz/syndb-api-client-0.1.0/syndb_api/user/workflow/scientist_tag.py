from random import randint

from sqlalchemy.ext.asyncio import AsyncSession

from syndb_api.user.model import User


def _tag_gen():
    # Generate a random four-digit number with leading zeros
    return str(randint(0, 9999)).zfill(4)


async def ensure_unique(session: AsyncSession, scientist_tag: str) -> bool:
    return bool(await session.query(User).filter_by(scientist_tag=scientist_tag).one_or_none())


async def generate_scientist_tag(session: AsyncSession, username: str) -> str:
    """
    Generate a battle tag from the given username, ensuring it doesn't already exist in the database.

    Args:
    username: str - the desired username

    Returns:
    str - the generated battle tag
    """
    scientist_tag = f"{username}#{(_tag_gen())}"
    while await ensure_unique(session, scientist_tag):
        scientist_tag = f"{username}#{_tag_gen()}"
    return scientist_tag
