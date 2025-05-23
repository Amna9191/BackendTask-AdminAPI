from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), index=True)
    price = Column(DECIMAL(10,2), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    inventory = relationship("Inventory", back_populates="product", uselist=False)
    sales     = relationship("Sale",      back_populates="product")

class Inventory(Base):
    __tablename__ = "inventory"
    id           = Column(Integer, primary_key=True, index=True)
    product_id   = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity     = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="inventory")

class Sale(Base):
    __tablename__ = "sales"
    id          = Column(Integer, primary_key=True, index=True)
    product_id  = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity    = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(10,2), nullable=False)
    sale_date   = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="sales")
