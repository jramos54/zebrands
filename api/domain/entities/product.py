from dataclasses import dataclass,field
from datetime import datetime
from typing import Optional

@dataclass
class Product:
    
    sku: str
    name: str
    price: float
    brand: str
    category: str
    stock: int
    short_description: str
    long_description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    id: Optional[int] = field(default=None)
