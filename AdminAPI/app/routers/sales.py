from fastapi      import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing        import List
from datetime import date, datetime, time
from .. import crud, schemas, database

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(database.get_db)):
    if not crud.get_product(db, sale.product_id):
        raise HTTPException(404, "Product not found")
    return crud.create_sale(db, sale)

@router.get("/", response_model=List[schemas.Sale])
def list_sales(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_sales(db, skip, limit)

@router.get("/by_date/", response_model=List[schemas.Sale])
def sales_by_date(
    *,
    start_date: date = Query(..., description="Start date, format YYYY-MM-DD"),
    end_date:   date = Query(..., description="End date,   format YYYY-MM-DD"),
    db: Session = Depends(database.get_db)
):
    # Convert to datetimes covering the whole day
    start_dt = datetime.combine(start_date, time.min)  # 00:00:00
    end_dt   = datetime.combine(end_date,   time.max)  # 23:59:59.999999

    results = crud.get_sales_by_date(db, start_dt, end_dt)
    if not results:
        raise HTTPException(404, f"No sales found between {start_date} and {end_date}")
    return results

@router.get("/revenue/", response_model=List[dict])
def revenue_summary(
    period: str = Query("daily", regex="^(daily|weekly|monthly|annual)$"),
    db: Session = Depends(database.get_db)
):
    return crud.get_revenue_summary(db, period)

@router.get("/by_product/{product_id}", response_model=List[schemas.Sale])
def sales_by_product(product_id: int, db: Session = Depends(database.get_db)):
    return crud.get_sales_by_product(db, product_id)

@router.get("/by_category/", response_model=List[schemas.Sale])
def sales_by_category(category: str, db: Session = Depends(database.get_db)):
    return crud.get_sales_by_category(db, category)
