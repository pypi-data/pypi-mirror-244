from typing import Optional

from fa_common import CamelModel, sizeof_fmt


# Shared properties
class File(CamelModel):
    size: Optional[str] = None  # e.g. '3 KB'
    size_bytes: Optional[int] = None
    url: Optional[str] = None  # download url
    gs_uri: Optional[str] = None  # GSC Uri
    id: Optional[str] = None  # id can be path or database id
    dir: bool = False
    path: Optional[str] = None  # path to current item (e.g. /folder1/someFile.txt)
    # optional (but we are using id as name if name is not present) (e.g. someFile.txt)
    name: str
    content_type: Optional[str] = None

    def set_size(self, bytes: int):  # noqa: A002
        self.size = sizeof_fmt(bytes)
        self.size_bytes = bytes
