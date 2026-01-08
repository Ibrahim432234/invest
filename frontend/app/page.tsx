'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { TrendingUp, BarChart3, Newspaper, Target } from 'lucide-react';

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/stock/${searchQuery.toUpperCase()}`);
    }
  };

  const popularStocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA'];

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center space-y-6 py-12">
        <h1 className="text-4xl md:text-6xl font-bold">
          Intelligente <span className="text-primary">Aktienanalyse</span>
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Treffen Sie informierte Investmententscheidungen mit technischer und fundamentaler Analyse
        </p>

        {/* Search */}
        <form onSubmit={handleSearch} className="max-w-md mx-auto mt-8">
          <div className="relative">
            <input
              type="text"
              placeholder="Aktie suchen (z.B. AAPL, MSFT)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-6 py-4 text-lg border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />
            <button
              type="submit"
              className="absolute right-2 top-1/2 transform -translate-y-1/2 px-6 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors"
            >
              Suchen
            </button>
          </div>
        </form>

        {/* Popular Stocks */}
        <div className="flex flex-wrap justify-center gap-2 mt-6">
          <span className="text-sm text-muted-foreground mr-2">Beliebt:</span>
          {popularStocks.map((ticker) => (
            <button
              key={ticker}
              onClick={() => router.push(`/stock/${ticker}`)}
              className="px-3 py-1 text-sm border rounded-full hover:bg-accent transition-colors"
            >
              {ticker}
            </button>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <FeatureCard
          icon={<BarChart3 className="h-8 w-8" />}
          title="Technische Analyse"
          description="RSI, MACD, Bollinger Bänder und mehr"
        />
        <FeatureCard
          icon={<TrendingUp className="h-8 w-8" />}
          title="Fundamentalanalyse"
          description="KGV, Dividendenrendite, Wachstum"
        />
        <FeatureCard
          icon={<Newspaper className="h-8 w-8" />}
          title="News & Sentiment"
          description="Aktuelle Nachrichten mit KI-Sentiment"
        />
        <FeatureCard
          icon={<Target className="h-8 w-8" />}
          title="Empfehlungen"
          description="Zeitraum-basierte Kauf/Verkauf-Signale"
        />
      </section>

      {/* How it works */}
      <section className="bg-accent rounded-lg p-8">
        <h2 className="text-3xl font-bold text-center mb-8">So funktioniert es</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <StepCard
            number="1"
            title="Aktie suchen"
            description="Geben Sie den Ticker oder Namen einer Aktie ein"
          />
          <StepCard
            number="2"
            title="Analyse erhalten"
            description="Umfassende technische und fundamentale Analyse"
          />
          <StepCard
            number="3"
            title="Informiert entscheiden"
            description="Nutzen Sie die Erkenntnisse für Ihre Investmentstrategie"
          />
        </div>
      </section>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="p-6 border rounded-lg hover:shadow-lg transition-shadow">
      <div className="text-primary mb-3">{icon}</div>
      <h3 className="font-bold text-lg mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}

function StepCard({
  number,
  title,
  description,
}: {
  number: string;
  title: string;
  description: string;
}) {
  return (
    <div className="text-center">
      <div className="w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
        {number}
      </div>
      <h3 className="font-bold text-lg mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}
