from datetime import datetime, timezone
from typing import Optional, Union, Dict, List
import ormar
from ormar import Model
from db import metadata, database


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100)


class Video(Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    file: str = ormar.String(max_length=1000)
    create_at: datetime = ormar.DateTime(default=lambda: datetime.now(timezone.utc))
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, nullable=True)
