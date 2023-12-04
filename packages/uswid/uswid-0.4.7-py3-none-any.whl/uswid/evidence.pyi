from .problem import uSwidProblem as uSwidProblem
from _typeshed import Incomplete
from datetime import datetime
from typing import List, Optional

class uSwidEvidence:
    date: Incomplete
    device_id: Incomplete
    def __init__(self, date: Optional[datetime] = ..., device_id: Optional[str] = ...) -> None: ...
    def problems(self) -> List[uSwidProblem]: ...
