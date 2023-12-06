from datetime import date, datetime, time, timezone
from typing import Annotated

from bson import ObjectId
from humps.camel import case
from pydantic import BaseModel, ConfigDict
from pydantic.functional_serializers import PlainSerializer


def to_camel(string):
    if string == "id":
        return "_id"
    if string.startswith("_"):  # "_id"
        return string
    return case(string)


DatetimeType = Annotated[
    datetime,
    PlainSerializer(
        lambda dt: dt.replace(microsecond=0, tzinfo=timezone.utc).isoformat(),
        return_type=str,
        when_used="json",
    ),
]
DateType = Annotated[date, PlainSerializer(lambda dt: dt.isoformat(), return_type=str, when_used="json")]
TimeType = Annotated[
    time,
    PlainSerializer(
        lambda dt: dt.replace(microsecond=0, tzinfo=timezone.utc).isoformat(),
        return_type=str,
        when_used="json",
    ),
]
ObjectIdType = Annotated[ObjectId, PlainSerializer(lambda oid: str(oid), return_type=str, when_used="json")]


class CamelModel(BaseModel):
    """
    Replacement for pydanitc BaseModel which simply adds a camel case alias to every field
    NOTE: This has been updated for Pydantic 2 to remove some common encoding helpers
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class FileDownloadRef(CamelModel):
    name: str
    url: str
    extension: str
    size: int
