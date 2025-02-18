from dataclasses import dataclass,field
from datetime import datetime
from typing import Optional

@dataclass
class User:
    
    username: str
    email: str
    password: str  
    role: str  # ('super_admin', 'admin', 'anonymous')
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    last_login: Optional[datetime] = None
    token: Optional[str] = None 
    id: Optional[int] = field(default=None)
