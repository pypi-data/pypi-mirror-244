from .container import uSwidContainer as uSwidContainer
from .enums import USWID_HEADER_MAGIC as USWID_HEADER_MAGIC, uSwidHeaderFlags as uSwidHeaderFlags, uSwidPayloadCompression as uSwidPayloadCompression
from .errors import NotSupportedError as NotSupportedError
from .format import uSwidFormatBase as uSwidFormatBase
from .format_coswid import uSwidFormatCoswid as uSwidFormatCoswid
from .identity import uSwidIdentity as uSwidIdentity
from _typeshed import Incomplete
from typing import Optional

class uSwidFormatUswid(uSwidFormatBase):
    compression: Incomplete
    def __init__(self, compress: bool = ..., compression: uSwidPayloadCompression = ...) -> None: ...
    @property
    def compress(self) -> bool: ...
    def load(self, blob: bytes, path: Optional[str] = ...) -> uSwidContainer: ...
    def save(self, container: uSwidContainer) -> bytes: ...
