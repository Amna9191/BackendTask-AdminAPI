from fastapi import FastAPI
from .database import engine, Base
from .routers  import products, inventory, sales

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Admin API")

app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(sales.router)
