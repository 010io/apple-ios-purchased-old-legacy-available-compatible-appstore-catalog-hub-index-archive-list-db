"""Main FastAPI Application

Основний файл FastAPI додатку для каталогу платних додатків iOS App Store.
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import csv
import io
from datetime import datetime

from .models import AppCatalogItem, CatalogResponse
from .database import get_database_session, SessionLocal
from .config import get_settings

# Налаштування
settings = get_settings()

# Створення FastAPI додатку
app = FastAPI(
    title="iOS App Store Catalog Hub",
    description="REST API для каталогу платних продуктів Apple Store",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Основна сторінка API"""
    return {
        "message": "iOS App Store Catalog Hub API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Перевірка стану сервісу"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ios-catalog-api"
    }


@app.get("/catalog", response_model=CatalogResponse)
async def get_catalog(
    product_type: Optional[str] = Query(None, description="Тип продукту"),
    min_ios: Optional[str] = Query(None, description="Мінімальна версія iOS"),
    price_max: Optional[float] = Query(None, description="Максимальна ціна"),
    genre: Optional[str] = Query(None, description="Жанр"),
    device: Optional[str] = Query(None, description="Пристрій"),
    format: Optional[str] = Query("json", description="Формат відповіді"),
    limit: int = Query(100, description="Кількість записів"),
    offset: int = Query(0, description="Зміщення для пагінації"),
    db: SessionLocal = Depends(get_database_session)
):
    """Отримання каталогу платних продуктів"""
    
    # TODO: реалізувати логіку запиту до бази даних
    
    # Приклад структури відповіді
    sample_items = [
        {
            "id": 284910350,
            "product_type": "software",
            "name": "Minecraft",
            "seller": "Mojang",
            "price": 6.99,
            "currency": "USD",
            "min_ios": "10.0",
            "genres": ["Games", "Adventure", "Sandbox"],
            "release_date": "2011-11-17T00:00:00Z",
            "supported_devices": ["iPhone", "iPad"]
        }
    ]
    
    if format == "csv":
        # Повернення CSV формату
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=sample_items[0].keys())
        writer.writeheader()
        writer.writerows(sample_items)
        
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=catalog.csv"}
        )
        return response
    
    return CatalogResponse(
        items=sample_items,
        total=len(sample_items),
        limit=limit,
        offset=offset
    )


@app.get("/catalog/{product_id}")
async def get_product(
    product_id: int,
    db: SessionLocal = Depends(get_database_session)
):
    """Отримання інформації про окремий продукт"""
    
    # TODO: реалізувати пошук по product_id
    
    # Приклад відповіді
    if product_id == 284910350:
        return {
            "id": 284910350,
            "product_type": "software",
            "name": "Minecraft",
            "seller": "Mojang",
            "price": 6.99,
            "currency": "USD",
            "min_ios": "10.0",
            "genres": ["Games", "Adventure", "Sandbox"],
            "release_date": "2011-11-17T00:00:00Z",
            "supported_devices": ["iPhone", "iPad"],
            "raw_json": {"fullAppleResponse": "..."}
        }
    
    raise HTTPException(status_code=404, detail="Продукт не знайдено")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
