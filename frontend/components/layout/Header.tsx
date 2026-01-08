'use client';

import Link from 'next/link';
import { TrendingUp, Search, Star } from 'lucide-react';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Header() {
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/stock/${searchQuery.toUpperCase()}`);
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center space-x-2 font-bold text-xl">
          <TrendingUp className="h-6 w-6 text-primary" />
          <span className="hidden sm:inline">SmartInvest Analyzer</span>
          <span className="sm:hidden">SIA</span>
        </Link>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="flex-1 max-w-md mx-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Aktie suchen (z.B. AAPL, MSFT)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </form>

        {/* Navigation */}
        <nav className="flex items-center space-x-4">
          <Link
            href="/watchlist"
            className="flex items-center space-x-1 px-3 py-2 rounded-md hover:bg-accent transition-colors"
            title="Watchlist"
          >
            <Star className="h-5 w-5" />
            <span className="hidden sm:inline">Watchlist</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}
