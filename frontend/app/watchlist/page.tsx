'use client';

import { Star } from 'lucide-react';

export default function WatchlistPage() {
  // Placeholder for watchlist functionality
  // In a full implementation, this would use LocalStorage or a backend API

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center space-x-3 mb-6">
        <Star className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-bold">Meine Watchlist</h1>
      </div>

      <div className="bg-card border rounded-lg p-12 text-center">
        <Star className="h-16 w-16 mx-auto mb-4 text-muted-foreground opacity-50" />
        <h2 className="text-xl font-semibold mb-2">Noch keine Aktien in der Watchlist</h2>
        <p className="text-muted-foreground mb-6">
          Fügen Sie Aktien zu Ihrer Watchlist hinzu, um sie schnell im Blick zu behalten.
        </p>
        <p className="text-sm text-muted-foreground">
          Klicken Sie auf das Stern-Symbol auf einer Aktien-Detailseite, um sie hinzuzufügen.
        </p>
      </div>
    </div>
  );
}
