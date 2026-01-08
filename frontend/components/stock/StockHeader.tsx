import { Star } from 'lucide-react';
import { formatCurrency, formatPercent, getChangeColor } from '@/lib/utils';

interface StockHeaderProps {
  quote: any;
}

export default function StockHeader({ quote }: StockHeaderProps) {
  const changeColor = getChangeColor(quote.change_percent);

  return (
    <div className="bg-card border rounded-lg p-6">
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center space-x-3">
            <h1 className="text-3xl font-bold">{quote.ticker}</h1>
            <button
              className="p-2 hover:bg-accent rounded-full transition-colors"
              title="Zur Watchlist hinzufügen"
            >
              <Star className="h-5 w-5" />
            </button>
          </div>
          <p className="text-muted-foreground mt-1">{quote.name}</p>
        </div>

        <div className="text-right">
          <div className="text-3xl font-bold">{formatCurrency(quote.price)}</div>
          <div className={`text-lg font-medium ${changeColor}`}>
            {formatPercent(quote.change_percent)} ({formatCurrency(quote.change)})
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t">
        <StatItem label="Open" value={formatCurrency(quote.open)} />
        <StatItem label="High" value={formatCurrency(quote.day_high)} />
        <StatItem label="Low" value={formatCurrency(quote.day_low)} />
        <StatItem label="Volume" value={quote.volume.toLocaleString()} />
        {quote.market_cap && (
          <StatItem label="Market Cap" value={formatMarketCap(quote.market_cap)} />
        )}
        {quote.pe_ratio && <StatItem label="P/E Ratio" value={quote.pe_ratio.toFixed(2)} />}
        {quote.dividend_yield && (
          <StatItem
            label="Dividend Yield"
            value={`${(quote.dividend_yield * 100).toFixed(2)}%`}
          />
        )}
        <StatItem label="Prev Close" value={formatCurrency(quote.previous_close)} />
      </div>
    </div>
  );
}

function StatItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-sm text-muted-foreground">{label}</div>
      <div className="font-medium">{value}</div>
    </div>
  );
}

function formatMarketCap(value: number): string {
  if (value >= 1e12) {
    return `$${(value / 1e12).toFixed(2)}T`;
  } else if (value >= 1e9) {
    return `$${(value / 1e9).toFixed(2)}B`;
  } else if (value >= 1e6) {
    return `$${(value / 1e6).toFixed(2)}M`;
  } else {
    return `$${value.toFixed(2)}`;
  }
}
