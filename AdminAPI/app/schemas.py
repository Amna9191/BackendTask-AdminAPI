from pydantic import BaseModel
from datetime import datetime
from typing   import Optional

# ── Products ────────────────────────────────────────────────────
class ProductBase(BaseModel):
    name: str
    category: Optional[str]
    price: float

class ProductCreate(ProductBase):
    ...

class Product(ProductBase):
    id: int
    time_created: datetime

    class Config:
        orm_mode = True

# ── Inventory ───────────────────────────────────────────────────
class InventoryBase(BaseModel):
    product_id: int
    quantity: int

class InventoryCreate(InventoryBase):
    ...

class Inventory(InventoryBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True

# ── Sales ───────────────────────────────────────────────────────
class SaleBase(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(SaleBase):
    ...

class Sale(SaleBase):
    id: int
    total_price: float
    sale_date: datetime

    class Config:
        orm_mode = True
