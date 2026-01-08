'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { api } from '@/lib/api';
import StockHeader from '@/components/stock/StockHeader';
import PriceChart from '@/components/stock/PriceChart';
import TechnicalIndicators from '@/components/stock/TechnicalIndicators';
import FundamentalData from '@/components/stock/FundamentalData';
import Recommendation from '@/components/stock/Recommendation';
import NewsFeed from '@/components/stock/NewsFeed';
import { Loader2 } from 'lucide-react';

export default function StockPage() {
  const params = useParams();
  const ticker = params.ticker as string;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [quote, setQuote] = useState<any>(null);
  const [historicalData, setHistoricalData] = useState<any>(null);
  const [technicals, setTechnicals] = useState<any>(null);
  const [fundamentals, setFundamentals] = useState<any>(null);
  const [recommendation, setRecommendation] = useState<any>(null);
  const [news, setNews] = useState<any>(null);
  const [timeframe, setTimeframe] = useState('mid');
  const [period, setPeriod] = useState('1y');

  useEffect(() => {
    loadStockData();
  }, [ticker]);

  useEffect(() => {
    if (ticker) {
      loadRecommendation();
    }
  }, [timeframe]);

  useEffect(() => {
    if (ticker) {
      loadHistoricalData();
    }
  }, [period]);

  const loadStockData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load all data in parallel
      const [quoteData, histData, techData, fundData, newsData, recData] = await Promise.all([
        api.getQuote(ticker),
        api.getHistoricalData(ticker, period),
        api.getTechnicals(ticker),
        api.getFundamentals(ticker),
        api.getNews(ticker),
        api.getRecommendation(ticker, timeframe),
      ]);

      setQuote(quoteData);
      setHistoricalData(histData);
      setTechnicals(techData);
      setFundamentals(fundData);
      setNews(newsData);
      setRecommendation(recData);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Fehler beim Laden der Daten');
      console.error('Error loading stock data:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadHistoricalData = async () => {
    try {
      const histData = await api.getHistoricalData(ticker, period);
      setHistoricalData(histData);
    } catch (err) {
      console.error('Error loading historical data:', err);
    }
  };

  const loadRecommendation = async () => {
    try {
      const recData = await api.getRecommendation(ticker, timeframe);
      setRecommendation(recData);
    } catch (err) {
      console.error('Error loading recommendation:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="h-12 w-12 animate-spin text-primary" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-danger mb-4">Fehler</h2>
        <p className="text-muted-foreground">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Stock Header */}
      {quote && <StockHeader quote={quote} />}

      {/* Chart */}
      {historicalData && (
        <PriceChart
          data={historicalData.data}
          period={period}
          onPeriodChange={setPeriod}
        />
      )}

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Technical Indicators */}
        {technicals && <TechnicalIndicators data={technicals} />}

        {/* Fundamental Data */}
        {fundamentals && <FundamentalData data={fundamentals} />}
      </div>

      {/* Recommendation */}
      {recommendation && (
        <Recommendation
          data={recommendation}
          timeframe={timeframe}
          onTimeframeChange={setTimeframe}
        />
      )}

      {/* News Feed */}
      {news && <NewsFeed data={news} />}
    </div>
  );
}
