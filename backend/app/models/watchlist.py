"""Watchlist model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Watchlist(Base):
    """User watchlist for tracking stocks"""

    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)  # Simple user identifier (session-based or user ID)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)

    notes = Column(String(500), nullable=True)
    target_price = Column(String(20), nullable=True)

    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    stock = relationship("Stock", back_populates="watchlist_entries")

    # Composite unique index to prevent duplicates
    __table_args__ = (
        Index("idx_watchlist_user_stock", "user_id", "stock_id", unique=True),
    )

    def __repr__(self):
        return f"<Watchlist user={self.user_id} stock={self.stock_id}>"
