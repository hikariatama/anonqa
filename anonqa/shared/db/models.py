import os
import sys
from typing import Union

import databases
import ormar
import sqlalchemy

try:
    from .. import config
except ImportError:
    import sys

    sys.path.insert(
        0,
        os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../",
            )
        ),
    )
    import config

POSTGRES_URI = config.parse(os.environ["CONFIG_PATH"]).main.postgres_uri

database = databases.Database(POSTGRES_URI)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "bot_users"

    user_id: int = ormar.BigInteger(primary_key=True)
    user_hash: str = ormar.String(min_length=64, max_length=64)

    @classmethod
    async def is_registered(cls, user_id: int) -> Union["User", bool]:
        return (await cls.objects.get_or_none(user_id=user_id)) or False

    @classmethod
    async def register(cls, user_id):
        from ..misc import get_hash

        return await cls.objects.create(user_id=user_id, user_hash=get_hash(user_id))

    @classmethod
    async def get_count(cls) -> int:
        return await cls.objects.count()


async def init():
    engine = sqlalchemy.create_engine(POSTGRES_URI)
    metadata.create_all(engine)
    await database.connect()
