import { TrendingUp, Clock, Target } from 'lucide-react';

interface RecommendationProps {
  data: any;
  timeframe: string;
  onTimeframeChange: (timeframe: string) => void;
}

export default function Recommendation({ data, timeframe, onTimeframeChange }: RecommendationProps) {
  const timeframes = [
    { value: 'short', label: 'Kurzfristig (1-4 Wochen)' },
    { value: 'mid', label: 'Mittelfristig (1-6 Monate)' },
    { value: 'long', label: 'Langfristig (6+ Monate)' },
  ];

  const actionBadges: any = {
    strong_buy: { text: 'STARKES KAUFSIGNAL', color: 'bg-success text-white', icon: '📈' },
    buy: { text: 'KAUFSIGNAL', color: 'bg-success/80 text-white', icon: '📊' },
    hold: { text: 'HALTEN', color: 'bg-muted text-muted-foreground', icon: '⏸️' },
    sell: { text: 'VERKAUFSSIGNAL', color: 'bg-danger/80 text-white', icon: '📉' },
    strong_sell: { text: 'STARKES VERKAUFSSIGNAL', color: 'bg-danger text-white', icon: '🔻' },
  };

  const badge = actionBadges[data.action] || actionBadges.hold;

  return (
    <div className="bg-card border rounded-lg p-6">
      <h2 className="text-xl font-bold mb-4">Empfehlung</h2>

      {/* Timeframe Selection */}
      <div className="mb-6">
        <label className="text-sm font-medium text-muted-foreground mb-2 block">Anlagehorizont</label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
          {timeframes.map((tf) => (
            <button
              key={tf.value}
              onClick={() => onTimeframeChange(tf.value)}
              className={`p-3 rounded-lg text-sm font-medium transition-colors ${
                timeframe === tf.value
                  ? 'bg-primary text-white'
                  : 'bg-secondary hover:bg-secondary/80'
              }`}
            >
              {tf.label}
            </button>
          ))}
        </div>
      </div>

      {/* Recommendation Card */}
      <div className={`p-6 rounded-lg ${badge.color} mb-6`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <span className="text-4xl">{badge.icon}</span>
            <div>
              <div className="text-2xl font-bold">{badge.text}</div>
              <div className="text-sm opacity-90 mt-1">Konfidenz: {(data.confidence * 100).toFixed(0)}%</div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm opacity-90">Score</div>
            <div className="text-3xl font-bold">{data.score.toFixed(1)}</div>
          </div>
        </div>
      </div>

      {/* Summary */}
      <div className="mb-6 p-4 bg-accent rounded-lg">
        <p className="text-sm">{data.summary}</p>
      </div>

      {/* Price Targets */}
      {data.target_price && (
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="p-4 border rounded-lg">
            <div className="text-sm text-muted-foreground mb-1 flex items-center space-x-2">
              <Target className="h-4 w-4" />
              <span>Aktueller Kurs</span>
            </div>
            <div className="text-2xl font-bold">${data.current_price.toFixed(2)}</div>
          </div>
          <div className="p-4 border rounded-lg bg-primary/5">
            <div className="text-sm text-muted-foreground mb-1 flex items-center space-x-2">
              <TrendingUp className="h-4 w-4" />
              <span>Kursziel</span>
            </div>
            <div className="text-2xl font-bold text-primary">${data.target_price.toFixed(2)}</div>
            <div className="text-sm text-muted-foreground mt-1">
              {((data.target_price - data.current_price) / data.current_price * 100).toFixed(1)}% Potenzial
            </div>
          </div>
        </div>
      )}

      {/* Score Breakdown */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <ScoreCard
          label="Technisch"
          score={data.technical_score}
          color="text-blue-600"
        />
        <ScoreCard
          label="Fundamental"
          score={data.fundamental_score}
          color="text-purple-600"
        />
        <ScoreCard
          label="Sentiment"
          score={data.sentiment_score}
          color="text-green-600"
        />
      </div>

      {/* Reasons */}
      <div className="mb-6">
        <h3 className="font-semibold mb-3">Begründung</h3>
        <div className="space-y-2">
          {data.reasons.slice(0, 5).map((reason: any, index: number) => (
            <div
              key={index}
              className="flex items-start space-x-2 p-2 rounded hover:bg-accent transition-colors"
            >
              <span className={`mt-0.5 ${reason.impact === 'positive' ? 'text-success' : 'text-danger'}`}>
                {reason.impact === 'positive' ? '✓' : '✗'}
              </span>
              <div className="flex-1">
                <div className="text-sm font-medium">{reason.indicator}</div>
                <div className="text-xs text-muted-foreground">
                  {reason.value} - {reason.category}
                </div>
              </div>
              <div className="text-xs text-muted-foreground">
                {(reason.weight * 100).toFixed(0)}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Risks */}
      {data.risks && data.risks.length > 0 && (
        <div className="p-4 bg-warning/10 border border-warning/30 rounded-lg">
          <h3 className="font-semibold text-warning mb-2 flex items-center space-x-2">
            <span>⚠️</span>
            <span>Risiken</span>
          </h3>
          <ul className="space-y-1">
            {data.risks.map((risk: string, index: number) => (
              <li key={index} className="text-sm text-muted-foreground">
                • {risk}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function ScoreCard({ label, score, color }: { label: string; score: number; color: string }) {
  return (
    <div className="p-3 border rounded-lg text-center">
      <div className="text-sm text-muted-foreground mb-1">{label}</div>
      <div className={`text-2xl font-bold ${color}`}>{score.toFixed(1)}</div>
    </div>
  );
}
