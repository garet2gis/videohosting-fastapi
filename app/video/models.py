from datetime import datetime, timezone
from typing import Dict, Optional, Union

from app.db import database, metadata
from app.user.models import User

import ormar
from ormar import Model


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Video(Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: Optional[str] = ormar.String(max_length=500, nullable=True)
    file: str = ormar.String(max_length=1000)
    create_at: datetime = ormar.DateTime(default=lambda: datetime.now(timezone.utc))
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, nullable=True)
