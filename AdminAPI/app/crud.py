from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime   import datetime
from . import models, schemas

# ── Products ────────────────────────────────────────────────────
def get_product(db: Session, product_id: int):
    return db.query(models.Product).get(product_id)

def get_products(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, p: schemas.ProductCreate):
    dbp = models.Product(name=p.name, category=p.category, price=p.price)
    db.add(dbp); db.commit(); db.refresh(dbp)
    # initialize inventory
    inv = models.Inventory(product_id=dbp.id, quantity=0)
    db.add(inv); db.commit()
    return dbp

# ── Inventory ───────────────────────────────────────────────────
def get_inventory(db: Session, product_id: int):
    return db.query(models.Inventory).filter_by(product_id=product_id).first()

def update_inventory(db: Session, product_id: int, quantity: int):
    inv = get_inventory(db, product_id)
    if inv:
        inv.quantity = quantity
        db.commit()
        db.refresh(inv)
    return inv

def get_low_stock(db: Session, threshold: int=10):
    return db.query(models.Inventory).filter(models.Inventory.quantity < threshold).all()

# ── Sales ───────────────────────────────────────────────────────
def create_sale(db: Session, s: schemas.SaleCreate):
    prod = get_product(db, s.product_id)
    total = prod.price * s.quantity
    dbs = models.Sale(product_id=s.product_id, quantity=s.quantity, total_price=total)
    db.add(dbs)
    # decrement inventory
    inv = get_inventory(db, s.product_id)
    if inv:
        inv.quantity -= s.quantity
    db.commit(); db.refresh(dbs)
    return dbs

def get_sales(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Sale).offset(skip).limit(limit).all()

def get_sales_by_date(db: Session, start_date: datetime, end_date: datetime):
    return db.query(models.Sale).filter(
      models.Sale.sale_date >= start_date,
      models.Sale.sale_date <= end_date
    ).all()

def get_revenue_summary(db: Session, period: str):
    fmt_map = {
      "daily":   "%Y-%m-%d",
      "weekly":  "%Y-%u",
      "monthly": "%Y-%m",
      "annual":  "%Y"
    }
    if period not in fmt_map:
        raise ValueError("Invalid period")
    fmt = fmt_map[period]
    rows = db.query(
      func.date_format(models.Sale.sale_date, fmt).label("period"),
      func.sum(models.Sale.total_price).label("revenue")
    ).group_by("period").all()
    return [{"period": r.period, "revenue": float(r.revenue)} for r in rows]

def get_sales_by_product(db: Session, product_id: int):
    return db.query(models.Sale).filter_by(product_id=product_id).all()

def get_sales_by_category(db: Session, category: str):
    return db.query(models.Sale).join(models.Product).filter(models.Product.category == category).all()
