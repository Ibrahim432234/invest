"""News and sentiment analysis service"""
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.core.config import settings

logger = logging.getLogger(__name__)


class NewsService:
    """Service for fetching and analyzing news"""

    def __init__(self):
        self.news_api_key = settings.NEWS_API_KEY
        self.vader_analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text: str) -> tuple[float, str]:
        """
        Analyze sentiment of text using VADER

        Args:
            text: Text to analyze

        Returns:
            Tuple of (sentiment_score, sentiment_label)
        """
        try:
            # Use VADER for financial sentiment
            scores = self.vader_analyzer.polarity_scores(text)
            compound_score = scores['compound']

            # Determine label
            if compound_score >= 0.05:
                label = 'positive'
            elif compound_score <= -0.05:
                label = 'negative'
            else:
                label = 'neutral'

            return compound_score, label
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return 0.0, 'neutral'

    def fetch_stock_news(self, ticker: str, days: int = 7) -> List[Dict]:
        """
        Fetch news for a stock

        Args:
            ticker: Stock ticker symbol
            days: Number of days to look back

        Returns:
            List of news articles with sentiment
        """
        try:
            # Try NewsAPI if key is available
            if self.news_api_key:
                return self._fetch_from_newsapi(ticker, days)
            else:
                # Fallback to yfinance news
                return self._fetch_from_yfinance(ticker)
        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {e}")
            return []

    def _fetch_from_newsapi(self, ticker: str, days: int) -> List[Dict]:
        """Fetch news from NewsAPI"""
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': ticker,
            'from': from_date,
            'sortBy': 'publishedAt',
            'apiKey': self.news_api_key,
            'language': 'en',
            'pageSize': 20
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            articles = []
            for article in data.get('articles', []):
                title = article.get('title', '')
                content = article.get('description', '')
                text = f"{title}. {content}"

                sentiment_score, sentiment_label = self.analyze_sentiment(text)

                articles.append({
                    'title': title,
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'url': article.get('url', ''),
                    'content': content,
                    'author': article.get('author', ''),
                    'sentiment_score': sentiment_score,
                    'sentiment_label': sentiment_label,
                    'published_at': article.get('publishedAt', datetime.now().isoformat())
                })

            return articles
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI: {e}")
            return []

    def _fetch_from_yfinance(self, ticker: str) -> List[Dict]:
        """Fetch news from yfinance"""
        import yfinance as yf

        try:
            stock = yf.Ticker(ticker)
            news = stock.news

            articles = []
            for item in news[:20]:  # Limit to 20 articles
                title = item.get('title', '')
                content = item.get('summary', '')
                text = f"{title}. {content}" if content else title

                sentiment_score, sentiment_label = self.analyze_sentiment(text)

                # Convert timestamp
                published_at = datetime.fromtimestamp(
                    item.get('providerPublishTime', datetime.now().timestamp())
                )

                articles.append({
                    'title': title,
                    'source': item.get('publisher', 'Unknown'),
                    'url': item.get('link', ''),
                    'content': content,
                    'author': '',
                    'sentiment_score': sentiment_score,
                    'sentiment_label': sentiment_label,
                    'published_at': published_at.isoformat()
                })

            return articles
        except Exception as e:
            logger.error(f"Error fetching from yfinance: {e}")
            return []

    def calculate_sentiment_summary(self, articles: List[Dict]) -> Dict:
        """
        Calculate overall sentiment summary from articles

        Args:
            articles: List of news articles with sentiment

        Returns:
            Sentiment summary dictionary
        """
        if not articles:
            return {
                'average_score': 0.0,
                'overall_sentiment': 'neutral',
                'positive_count': 0,
                'neutral_count': 0,
                'negative_count': 0,
                'total_count': 0
            }

        scores = [a['sentiment_score'] for a in articles]
        avg_score = sum(scores) / len(scores)

        positive_count = sum(1 for a in articles if a['sentiment_label'] == 'positive')
        neutral_count = sum(1 for a in articles if a['sentiment_label'] == 'neutral')
        negative_count = sum(1 for a in articles if a['sentiment_label'] == 'negative')

        # Determine overall sentiment
        if avg_score >= 0.1:
            overall = 'positive'
        elif avg_score <= -0.1:
            overall = 'negative'
        else:
            overall = 'neutral'

        return {
            'average_score': round(avg_score, 3),
            'overall_sentiment': overall,
            'positive_count': positive_count,
            'neutral_count': neutral_count,
            'negative_count': negative_count,
            'total_count': len(articles)
        }
