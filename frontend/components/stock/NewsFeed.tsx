import { Newspaper, ExternalLink } from 'lucide-react';
import { format } from 'date-fns';
import { de } from 'date-fns/locale';

interface NewsFeedProps {
  data: any;
}

export default function NewsFeed({ data }: NewsFeedProps) {
  const { news, sentiment_summary } = data;

  const getSentimentBadge = (sentiment: string) => {
    const badges: any = {
      positive: { text: 'Positiv', color: 'bg-success text-white' },
      neutral: { text: 'Neutral', color: 'bg-muted text-muted-foreground' },
      negative: { text: 'Negativ', color: 'bg-danger text-white' },
    };
    const badge = badges[sentiment] || badges.neutral;
    return <span className={`px-2 py-1 rounded text-xs font-medium ${badge.color}`}>{badge.text}</span>;
  };

  const getSentimentIcon = (sentiment: string) => {
    if (sentiment === 'positive') return '😊';
    if (sentiment === 'negative') return '😟';
    return '😐';
  };

  return (
    <div className="bg-card border rounded-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold flex items-center space-x-2">
          <Newspaper className="h-6 w-6" />
          <span>News & Sentiment</span>
        </h2>
      </div>

      {/* Sentiment Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 p-4 bg-accent rounded-lg">
        <div>
          <div className="text-sm text-muted-foreground mb-1">Gesamtstimmung</div>
          <div className="flex items-center space-x-2">
            <span className="text-2xl">{getSentimentIcon(sentiment_summary.overall_sentiment)}</span>
            {getSentimentBadge(sentiment_summary.overall_sentiment)}
          </div>
        </div>
        <div>
          <div className="text-sm text-muted-foreground mb-1">Durchschnitt</div>
          <div className="text-xl font-bold">{sentiment_summary.average_score.toFixed(2)}</div>
        </div>
        <div>
          <div className="text-sm text-muted-foreground mb-1">Artikel</div>
          <div className="text-xl font-bold">{sentiment_summary.total_count}</div>
        </div>
        <div>
          <div className="text-sm text-muted-foreground mb-1">Verteilung</div>
          <div className="flex space-x-1 text-xs">
            <span className="text-success">+{sentiment_summary.positive_count}</span>
            <span className="text-muted-foreground">/{sentiment_summary.neutral_count}</span>
            <span className="text-danger">/-{sentiment_summary.negative_count}</span>
          </div>
        </div>
      </div>

      {/* News Articles */}
      <div className="space-y-4">
        {news.slice(0, 10).map((article: any, index: number) => (
          <div
            key={index}
            className="p-4 border rounded-lg hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-medium flex-1 pr-4">
                {article.url ? (
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-primary transition-colors inline-flex items-center space-x-1"
                  >
                    <span>{article.title}</span>
                    <ExternalLink className="h-3 w-3" />
                  </a>
                ) : (
                  article.title
                )}
              </h3>
              {getSentimentBadge(article.sentiment_label)}
            </div>

            {article.content && (
              <p className="text-sm text-muted-foreground mb-2 line-clamp-2">
                {article.content}
              </p>
            )}

            <div className="flex items-center justify-between text-xs text-muted-foreground">
              <span>{article.source}</span>
              <span>
                {format(new Date(article.published_at), 'PPp', { locale: de })}
              </span>
            </div>
          </div>
        ))}
      </div>

      {news.length === 0 && (
        <div className="text-center py-8 text-muted-foreground">
          <Newspaper className="h-12 w-12 mx-auto mb-2 opacity-50" />
          <p>Keine aktuellen Nachrichten verfügbar</p>
        </div>
      )}
    </div>
  );
}
