'use client';

import { AlertTriangle } from 'lucide-react';
import { useState } from 'react';

export default function Disclaimer() {
  const [isVisible, setIsVisible] = useState(true);

  if (!isVisible) return null;

  return (
    <div className="bg-warning/10 border-y border-warning/30">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-start space-x-3">
          <AlertTriangle className="h-5 w-5 text-warning flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-medium">
              <strong>HAFTUNGSAUSSCHLUSS:</strong> Diese Plattform dient ausschließlich zu Informationszwecken.
              Es werden keine rechtlich bindenden Anlageempfehlungen gegeben. Vergangene Performance ist keine
              Garantie für zukünftige Ergebnisse. Investieren Sie nur Geld, dessen Verlust Sie sich leisten können.
            </p>
          </div>
          <button
            onClick={() => setIsVisible(false)}
            className="text-muted-foreground hover:text-foreground transition-colors flex-shrink-0"
            aria-label="Hinweis schließen"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  );
}
