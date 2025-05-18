from fastapi      import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing        import List
from .. import crud, schemas, database

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/{product_id}", response_model=schemas.Inventory)
def read_inventory(product_id: int, db: Session = Depends(database.get_db)):
    inv = crud.get_inventory(db, product_id)
    if not inv:
        raise HTTPException(404, "Inventory not found")
    return inv

@router.put("/{product_id}", response_model=schemas.Inventory)
def update_inventory(product_id: int, quantity: int, db: Session = Depends(database.get_db)):
    inv = crud.update_inventory(db, product_id, quantity)
    if not inv:
        raise HTTPException(404, "Inventory not found")
    return inv

@router.get("/low_stock/", response_model=List[schemas.Inventory])
def low_stock(threshold: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_low_stock(db, threshold)
