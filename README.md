# SmartInvest Analyzer

Eine webbasierte Investment-Beratungsplattform für technische und fundamentale Aktienanalyse.

## ⚠️ Rechtlicher Hinweis

**KEINE ANLAGEBERATUNG**: Diese Plattform dient ausschließlich zu Informationszwecken. Es werden keine rechtlich bindenden Anlageempfehlungen gegeben. Vergangene Performance ist keine Garantie für zukünftige Ergebnisse. Investieren Sie nur Geld, dessen Verlust Sie sich leisten können.

## Features

### Muss-Kriterien (Phase 1)
- ✅ **Aktiensuche**: Suche nach Ticker, ISIN, WKN, Name mit Filtern
- ✅ **Echtzeit-Kursdaten**: Aktuelle und historische Kurse (1D - 5Y)
- ✅ **Technische Analyse**: RSI, MACD, SMA, Bollinger Bänder, Support/Resistance
- ✅ **Fundamentalanalyse**: KGV, KBV, Dividendenrendite, Branchenvergleich
- ✅ **Zeitraum-Empfehlungen**: Kurzfristig (technisch) vs. Langfristig (fundamental)
- ✅ **News & Sentiment**: Aktuelle Nachrichten mit Sentiment-Analyse
- ✅ **Watchlist**: Persönliche Aktien-Watchlist
- ✅ **Compliance**: Disclaimer auf allen Seiten

### Soll-Kriterien (Phase 2)
- 🔄 Portfolio-Tracker
- 🔄 Vergleichsfunktion
- 🔄 Backtesting
- 🔄 AI-gestützte Analyse

## Technologie-Stack

### Backend
- **Framework**: Python 3.11+ mit FastAPI
- **Datenbank**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Migration**: Alembic
- **Caching**: Redis
- **APIs**: yfinance, Alpha Vantage, NewsAPI

### Frontend
- **Framework**: Next.js 14 (App Router) mit TypeScript
- **Styling**: TailwindCSS + shadcn/ui
- **Charts**: Recharts / Lightweight Charts
- **State**: Zustand
- **API Client**: Axios

### DevOps
- **Containerisierung**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Deployment**: Vercel (Frontend) + Railway (Backend)

## Schnellstart

### Voraussetzungen
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+ (optional, wenn Docker verwendet wird)

### Installation

#### 1. Repository klonen
```bash
git clone <repo-url>
cd invest
```

#### 2. Umgebungsvariablen einrichten
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

Bearbeiten Sie die `.env` Dateien und fügen Sie Ihre API-Keys hinzu:
- Alpha Vantage: https://www.alphavantage.co/support/#api-key
- NewsAPI: https://newsapi.org/register

#### 3. Mit Docker starten (Empfohlen)
```bash
docker-compose up -d
```

Die Anwendung läuft nun auf:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

#### 4. Manuelle Installation

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API-Dokumentation

Nach dem Start des Backends finden Sie die interaktive API-Dokumentation unter:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Hauptendpunkte

```
GET  /api/v1/stocks/search?q={query}
GET  /api/v1/stocks/{ticker}
GET  /api/v1/stocks/{ticker}/quote
GET  /api/v1/stocks/{ticker}/historical?period={1d|1w|1m|3m|1y|5y}
GET  /api/v1/stocks/{ticker}/technicals
GET  /api/v1/stocks/{ticker}/fundamentals
GET  /api/v1/stocks/{ticker}/recommendation?timeframe={short|mid|long}
GET  /api/v1/stocks/{ticker}/news
POST /api/v1/watchlist
GET  /api/v1/watchlist
DELETE /api/v1/watchlist/{ticker}
```

## Entwicklung

### Backend-Tests ausführen
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend-Tests ausführen
```bash
cd frontend
npm run test
```

### Linting
```bash
# Backend
cd backend
flake8 app/
black app/ --check
mypy app/

# Frontend
cd frontend
npm run lint
npm run type-check
```

## Datenmodell

```
┌─────────────┐       ┌──────────────┐       ┌────────────────────┐
│   Stock     │──────<│  PriceData   │       │  TechnicalIndicator│
├─────────────┤       ├──────────────┤       ├────────────────────┤
│ id          │       │ id           │       │ id                 │
│ ticker      │       │ stock_id     │       │ stock_id           │
│ name        │       │ date         │       │ date               │
│ isin        │       │ open         │       │ rsi                │
│ sector      │       │ high         │       │ macd               │
│ country     │       │ low          │       │ sma_50             │
└─────────────┘       │ close        │       │ sma_200            │
                      │ volume       │       └────────────────────┘
                      └──────────────┘

┌─────────────────┐   ┌──────────────┐       ┌────────────────┐
│ Fundamentals    │   │  News        │       │  Watchlist     │
├─────────────────┤   ├──────────────┤       ├────────────────┤
│ id              │   │ id           │       │ id             │
│ stock_id        │   │ stock_id     │       │ user_id        │
│ pe_ratio        │   │ title        │       │ stock_id       │
│ pb_ratio        │   │ source       │       │ added_at       │
│ dividend_yield  │   │ url          │       └────────────────┘
│ market_cap      │   │ sentiment    │
└─────────────────┘   │ published_at │
                      └──────────────┘
```

## Projektstruktur

```
invest/
├── backend/
│   ├── app/
│   │   ├── api/          # API-Endpunkte
│   │   ├── core/         # Konfiguration, Sicherheit
│   │   ├── models/       # SQLAlchemy-Modelle
│   │   ├── schemas/      # Pydantic-Schemas
│   │   ├── services/     # Business-Logik
│   │   └── utils/        # Hilfsfunktionen
│   ├── tests/            # Backend-Tests
│   ├── alembic/          # Datenbank-Migrationen
│   └── requirements.txt
├── frontend/
│   ├── app/              # Next.js App Router
│   ├── components/       # React-Komponenten
│   ├── lib/              # Utilities, API-Client
│   ├── public/           # Statische Assets
│   └── package.json
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── docker-compose.yml
└── README.md
```

## Deployment

### Vercel (Frontend)
```bash
cd frontend
vercel --prod
```

### Railway (Backend)
1. Erstellen Sie ein neues Projekt auf Railway
2. Verbinden Sie Ihr GitHub-Repository
3. Fügen Sie PostgreSQL und Redis Services hinzu
4. Setzen Sie Umgebungsvariablen
5. Deploy wird automatisch ausgelöst

## Lizenz

MIT License - Siehe LICENSE Datei

## Kontakt

**Projekt**: SmartInvest Analyzer
**Version**: 1.0.0
**Erstellt**: Januar 2026

---

**Haftungsausschluss**: Dieses Tool dient ausschließlich zu Bildungs- und Informationszwecken. Es stellt keine Anlageberatung im Sinne des WpHG dar und ersetzt nicht die Beratung durch einen zugelassenen Finanzberater.
