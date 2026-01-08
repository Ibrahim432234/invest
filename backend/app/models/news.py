"""News model"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class News(Base):
    """News articles related to stocks"""

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(500), nullable=False)
    source = Column(String(100), nullable=True)
    url = Column(String(1000), nullable=True)
    content = Column(Text, nullable=True)
    author = Column(String(200), nullable=True)

    # Sentiment analysis (-1 to 1, where -1 is negative, 0 is neutral, 1 is positive)
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String(20), nullable=True)  # positive, neutral, negative

    published_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    stock = relationship("Stock", back_populates="news")

    # Composite index
    __table_args__ = (
        Index("idx_news_stock_published", "stock_id", "published_at"),
    )

    def __repr__(self):
        return f"<News {self.stock_id}: {self.title[:50]}>"
