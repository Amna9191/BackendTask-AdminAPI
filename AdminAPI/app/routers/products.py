
from fastapi     import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing       import List
from .. import crud, schemas, database

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(database.get_db)
):
    return crud.create_product(db, product)

@router.get("/", response_model=List[schemas.Product])
def list_products(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(database.get_db)
):
    return crud.get_products(db, skip, limit)

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    p = crud.get_product(db, product_id)
    if not p:
        raise HTTPException(404, "Product not found")
    return p
