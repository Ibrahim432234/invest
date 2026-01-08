import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface TechnicalIndicatorsProps {
  data: any;
}

export default function TechnicalIndicators({ data }: TechnicalIndicatorsProps) {
  const { indicators, signals, overall_signal, score } = data;

  const getSignalIcon = (signal: string) => {
    if (signal === 'buy') return <TrendingUp className="h-4 w-4 text-success" />;
    if (signal === 'sell') return <TrendingDown className="h-4 w-4 text-danger" />;
    return <Minus className="h-4 w-4 text-muted-foreground" />;
  };

  const getSignalBadge = (signal: string) => {
    const badges: any = {
      strong_buy: { text: 'Starkes Kaufsignal', color: 'bg-success text-white' },
      buy: { text: 'Kaufsignal', color: 'bg-success/80 text-white' },
      neutral: { text: 'Neutral', color: 'bg-muted text-muted-foreground' },
      sell: { text: 'Verkaufssignal', color: 'bg-danger/80 text-white' },
      strong_sell: { text: 'Starkes Verkaufssignal', color: 'bg-danger text-white' },
    };
    const badge = badges[signal] || badges.neutral;
    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium ${badge.color}`}>
        {badge.text}
      </span>
    );
  };

  return (
    <div className="bg-card border rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4">Technische Analyse</h2>

      {/* Overall Signal */}
      <div className="flex items-center justify-between mb-6 p-4 bg-accent rounded-lg">
        <div>
          <div className="text-sm text-muted-foreground mb-1">Gesamtbewertung</div>
          {getSignalBadge(overall_signal)}
        </div>
        <div className="text-right">
          <div className="text-sm text-muted-foreground mb-1">Score</div>
          <div className="text-2xl font-bold">{score}</div>
        </div>
      </div>

      {/* Key Indicators */}
      <div className="space-y-3 mb-6">
        <h3 className="font-semibold text-sm text-muted-foreground">Kernindikatoren</h3>
        {indicators.rsi_14 !== null && (
          <IndicatorRow
            label="RSI (14)"
            value={indicators.rsi_14.toFixed(2)}
            description={getRSIDescription(indicators.rsi_14)}
          />
        )}
        {indicators.macd !== null && (
          <IndicatorRow
            label="MACD"
            value={indicators.macd.toFixed(4)}
            description={indicators.macd_histogram > 0 ? 'Bullish' : 'Bearish'}
          />
        )}
        {indicators.sma_50 !== null && (
          <IndicatorRow label="SMA 50" value={`$${indicators.sma_50.toFixed(2)}`} />
        )}
        {indicators.sma_200 !== null && (
          <IndicatorRow label="SMA 200" value={`$${indicators.sma_200.toFixed(2)}`} />
        )}
      </div>

      {/* Signals */}
      <div className="space-y-2">
        <h3 className="font-semibold text-sm text-muted-foreground mb-3">Signale</h3>
        {signals.map((signal: any, index: number) => (
          <div
            key={index}
            className="flex items-start space-x-2 p-2 rounded hover:bg-accent transition-colors"
          >
            {getSignalIcon(signal.signal)}
            <div className="flex-1">
              <div className="font-medium text-sm">{signal.indicator}</div>
              <div className="text-xs text-muted-foreground">{signal.description}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function IndicatorRow({
  label,
  value,
  description,
}: {
  label: string;
  value: string;
  description?: string;
}) {
  return (
    <div className="flex items-center justify-between p-2 rounded hover:bg-accent transition-colors">
      <span className="text-sm font-medium">{label}</span>
      <div className="text-right">
        <div className="text-sm font-bold">{value}</div>
        {description && <div className="text-xs text-muted-foreground">{description}</div>}
      </div>
    </div>
  );
}

function getRSIDescription(rsi: number): string {
  if (rsi < 30) return 'Überverkauft';
  if (rsi > 70) return 'Überkauft';
  return 'Neutral';
}
