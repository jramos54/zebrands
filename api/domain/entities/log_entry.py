from dataclasses import dataclass,field
from datetime import datetime
from typing import Dict
from typing import Optional


@dataclass
class LogEntry:
    admin_id: int 
    target_id: int  
    action: str  # ('created', 'updated', 'deleted', 'activated', 'deactivated')
    changes: Dict 
    created_at: datetime
    id: Optional[int] = field(default=None)
