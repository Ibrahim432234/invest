"""Price data model"""
from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class PriceData(Base):
    """Historical and current price data for stocks"""

    __tablename__ = "price_data"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    adjusted_close = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    stock = relationship("Stock", back_populates="price_data")

    # Composite index for efficient queries
    __table_args__ = (
        Index("idx_stock_date", "stock_id", "date"),
    )

    def __repr__(self):
        return f"<PriceData {self.stock_id} @ {self.date}: {self.close}>"
