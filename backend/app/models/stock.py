"""Stock model"""
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Stock(Base):
    """Stock entity representing a tradable stock"""

    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    isin = Column(String(12), unique=True, index=True, nullable=True)
    wkn = Column(String(6), index=True, nullable=True)
    sector = Column(String(100), index=True, nullable=True)
    industry = Column(String(100), nullable=True)
    country = Column(String(2), index=True, nullable=True)  # ISO 3166-1 alpha-2
    exchange = Column(String(50), nullable=True)
    currency = Column(String(3), nullable=True)
    market_cap = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    price_data = relationship("PriceData", back_populates="stock", cascade="all, delete-orphan")
    fundamentals = relationship("Fundamental", back_populates="stock", cascade="all, delete-orphan")
    technical_indicators = relationship("TechnicalIndicator", back_populates="stock", cascade="all, delete-orphan")
    news = relationship("News", back_populates="stock", cascade="all, delete-orphan")
    watchlist_entries = relationship("Watchlist", back_populates="stock", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Stock {self.ticker}: {self.name}>"
