# BackendTask-AdminAPI
---

## 📋 Prerequisites

* **Python 3.10+** installed and on your `PATH`
* **MySQL** server accessible locally or remotely
* **Git** (for cloning the repo)

## 🔧 Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/Amna9191/BackendTask-AdminAPI.git
   cd AdminAPI
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .\venv         # Windows PowerShell
   # python3 -m venv ./venv     # macOS/Linux
   ```

3. **Activate the venv**

   ```powershell
   .\venv\Scripts\Activate     # Windows PowerShell
   # source ./venv/bin/activate  # macOS/Linux
   ```

4. **Configure environment variables**
   Open the included `.env` file in the project root and replace the placeholder values with your MySQL credentials:

   ```dotenv
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=ecommerce_admin_api
   ```

5. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

6. **Seed demo data**

   ```bash
   python demo_data.py
   ```

7. **Run the API server**

   ```bash
   uvicorn app.main:app --reload
   ```

The service will be live at `http://127.0.0.1:8000/`.

---

## 🧩 Dependencies

All Python dependencies are pinned in `requirements.txt`. Key packages include:

* **FastAPI** – web framework
* **Uvicorn** – ASGI server
* **SQLAlchemy** – ORM
* **mysql-connector-python** or **PyMySQL + cryptography** – MySQL drivers
* **python-dotenv** – `.env` loader

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🚀 API Endpoints

All endpoints are mounted under `/` and use JSON.
Interactive docs are available at:

http://127.0.0.1:8000/docs


### 📦 Products

| Method | Path             | Request Body                | Description                        |
| ------ | ---------------- | --------------------------- | ---------------------------------- |
| POST   | `/products/`     | `{ name, category, price }` | Create a new product (inv qty = 0) |
| GET    | `/products/`     | —                           | List all products                  |
| GET    | `/products/{id}` | —                           | Retrieve single product by **id**  |

### 🗄️ Inventory

| Method | Path                      | Query / Body     | Description                                  |
| ------ | ------------------------- | ---------------- | -------------------------------------------- |
| GET    | `/inventory/{product_id}` | —                | Get inventory record for a product           |
| PUT    | `/inventory/{product_id}` | `?quantity=int`  | Update stock level for a product             |
| GET    | `/inventory/low_stock/`   | `?threshold=int` | List all inventory items below the threshold |

### 💰 Sales

| Method | Path                             | Request / Query Params                       | Description                                    |
| ------ | -------------------------------- | -------------------------------------------- | ---------------------------------------------- |
| POST   | `/sales/`                        | `{ product_id, quantity }`                   | Create a sale (decrements inventory)           |
| GET    | `/sales/`                        | —                                            | List all sales                                 |
| GET    | `/sales/by_date/`                | `?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | List sales in the given date range             |
| GET    | `/sales/revenue/`                | `?period=daily\|weekly\|monthly\|annual`     | Revenue summary grouped by day/week/month/year |
| GET    | `/sales/by_product/{product_id}` | —                                            | Sales history for a specific product           |
| GET    | `/sales/by_category/`            | `?category=CategoryName`                     | Sales history for a specific category          |

---

