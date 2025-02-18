from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ProductQuery:
    id: int
    product_id: int
    anonymous_user_id: Optional[int] 
    queried_at: datetime
