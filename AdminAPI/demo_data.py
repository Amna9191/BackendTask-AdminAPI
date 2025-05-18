from app import crud, schemas, database, models
from datetime import datetime, timedelta


def populate_demo():
    db = next(database.get_db())

    # 1) Create products across 3 categories: Tech, Clothes, Home (5 each)
    tech_items = [
        schemas.ProductCreate(name="Smartphone X",    category="Tech",   price=699.99),
        schemas.ProductCreate(name="Laptop Pro",      category="Tech",   price=1299.00),
        schemas.ProductCreate(name="Wireless Earbuds",category="Tech",   price=149.50),
        schemas.ProductCreate(name="Smartwatch Z",    category="Tech",   price=249.99),
        schemas.ProductCreate(name="Gaming Console",  category="Tech",   price=499.00),
    ]
    clothes_items = [
        schemas.ProductCreate(name="T-Shirt Classic", category="Clothes", price=19.99),
        schemas.ProductCreate(name="Jeans Slim Fit",  category="Clothes", price=49.90),
        schemas.ProductCreate(name="Sneakers",        category="Clothes", price=89.99),
        schemas.ProductCreate(name="Hoodie",          category="Clothes", price=39.99),
        schemas.ProductCreate(name="Jacket",          category="Clothes", price=119.00),
    ]
    home_items = [
        schemas.ProductCreate(name="Coffee Maker",    category="Home",    price=79.95),
        schemas.ProductCreate(name="Blender",         category="Home",    price=59.99),
        schemas.ProductCreate(name="Vacuum Cleaner",  category="Home",    price=129.00),
        schemas.ProductCreate(name="Air Purifier",    category="Home",    price=199.99),
        schemas.ProductCreate(name="Desk Lamp",       category="Home",    price=29.50),
    ]

    # Bulk-create all items
    all_items = tech_items + clothes_items + home_items
    for item in all_items:
        crud.create_product(db, item)

    # 2) Seed inventory for each product
    for prod_id in range(1, len(all_items) + 1):
        # assign an initial stock (e.g., 100 units each)
        crud.update_inventory(db, product_id=prod_id, quantity=100)

    # 3) Record sales spanning daily, weekly, monthly, annual periods
    now      = datetime.now()
    # Daily: three sales today
    daily_dates = [now, now - timedelta(hours=2), now - timedelta(hours=5)]
    # Weekly: three sales this week (3-5 days ago)
    weekly_dates = [now - timedelta(days=3), now - timedelta(days=4), now - timedelta(days=5)]
    # Monthly: three sales this month (15, 20, 25 days ago)
    monthly_dates = [now - timedelta(days=15), now - timedelta(days=20), now - timedelta(days=25)]
    # Annual: three sales earlier this year (100, 200, 300 days ago)
    annual_dates = [now - timedelta(days=100), now - timedelta(days=200), now - timedelta(days=300)]

    sale_entries = []
    # assign product_ids 1-12 for these 12 entries
    for idx, d in enumerate(daily_dates, start=1):
        sale_entries.append({"product_id": idx,       "quantity": 2, "sale_date": d})
    for idx, d in enumerate(weekly_dates, start=4):
        sale_entries.append({"product_id": idx + 1,   "quantity": 1, "sale_date": d})
    for idx, d in enumerate(monthly_dates, start=7):
        sale_entries.append({"product_id": idx + 1,   "quantity": 3, "sale_date": d})
    for idx, d in enumerate(annual_dates, start=10):
        sale_entries.append({"product_id": idx + 1,   "quantity": 5, "sale_date": d})

    # Insert each sale with explicit sale_date, adjust inventory accordingly
    for entry in sale_entries:
        prod = crud.get_product(db, entry["product_id"])
        total = prod.price * entry["quantity"]
        sale = models.Sale(
            product_id=entry["product_id"],
            quantity=entry["quantity"],
            total_price=total,
            sale_date=entry["sale_date"]
        )
        db.add(sale)
        # decrement inventory
        inv = crud.get_inventory(db, entry["product_id"])
        if inv:
            inv.quantity -= entry["quantity"]

    # Commit all manual sales
    db.commit()

    print("Demo data populated (products, inventory, and dated sales)")


if __name__ == "__main__":
    populate_demo()
