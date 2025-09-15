from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

Base = declarative_base()

class App(Base):
    __tablename__ = "apps"
    
    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    developer = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(Text)
    version = Column(String)
    release_date = Column(DateTime)
    last_updated = Column(DateTime)
    rating = Column(Float)
    price = Column(Float, default=0.0)
    is_available = Column(Boolean, default=True)
    ios_version_required = Column(String)
    file_size = Column(String)
    bundle_id = Column(String)
    icon_url = Column(String)
    screenshot_urls = Column(Text)  # JSON string
    app_store_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    purchases = relationship("Purchase", back_populates="app")
    compatibility_checks = relationship("CompatibilityCheck", back_populates="app")

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(String, ForeignKey("apps.app_id"))
    purchase_date = Column(DateTime)
    user_id = Column(String, index=True)
    price_paid = Column(Float)
    device_info = Column(String)
    ios_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    app = relationship("App", back_populates="purchases")

class CompatibilityCheck(Base):
    __tablename__ = "compatibility_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(String, ForeignKey("apps.app_id"))
    ios_version = Column(String)
    device_model = Column(String)
    is_compatible = Column(Boolean)
    check_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    # Relationships
    app = relationship("App", back_populates="compatibility_checks")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic schemas for API
class AppBase(BaseModel):
    app_id: str
    name: str
    developer: str
    category: str
    description: Optional[str] = None
    version: Optional[str] = None
    rating: Optional[float] = None
    price: float = 0.0
    is_available: bool = True
    ios_version_required: Optional[str] = None
    file_size: Optional[str] = None
    bundle_id: Optional[str] = None
    icon_url: Optional[str] = None
    app_store_url: Optional[str] = None

class AppCreate(AppBase):
    pass

class AppUpdate(BaseModel):
    name: Optional[str] = None
    developer: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    rating: Optional[float] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    ios_version_required: Optional[str] = None
    file_size: Optional[str] = None
    icon_url: Optional[str] = None
    app_store_url: Optional[str] = None

class AppResponse(AppBase):
    id: int
    release_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class PurchaseBase(BaseModel):
    app_id: str
    purchase_date: datetime
    user_id: str
    price_paid: float
    device_info: Optional[str] = None
    ios_version: Optional[str] = None

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseResponse(PurchaseBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class CompatibilityCheckBase(BaseModel):
    app_id: str
    ios_version: str
    device_model: str
    is_compatible: bool
    notes: Optional[str] = None

class CompatibilityCheckCreate(CompatibilityCheckBase):
    pass

class CompatibilityCheckResponse(CompatibilityCheckBase):
    id: int
    check_date: datetime
    
    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
