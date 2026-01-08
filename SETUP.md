# SmartInvest Analyzer - Setup Guide

## Quick Start mit Docker (Empfohlen)

### Voraussetzungen
- Docker Desktop installiert
- Git installiert

### Installation

1. **Repository klonen:**
```bash
git clone <repository-url>
cd invest
```

2. **Umgebungsvariablen einrichten:**
```bash
# Backend .env erstellen
cp backend/.env.example backend/.env

# Frontend .env.local erstellen
cp frontend/.env.example frontend/.env.local
```

3. **Optional: API-Keys hinzufügen (für vollständige Funktionalität):**

Bearbeiten Sie `backend/.env` und fügen Sie Ihre API-Keys hinzu:
```
ALPHA_VANTAGE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

API-Keys erhalten Sie kostenlos bei:
- Alpha Vantage: https://www.alphavantage.co/support/#api-key
- NewsAPI: https://newsapi.org/register

**HINWEIS:** Die App funktioniert auch ohne API-Keys, nutzt dann aber nur yfinance.

4. **Anwendung starten:**
```bash
docker-compose up -d
```

Die Anwendung ist nun verfügbar unter:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Dokumentation:** http://localhost:8000/docs

5. **Logs anzeigen:**
```bash
docker-compose logs -f
```

6. **Anwendung stoppen:**
```bash
docker-compose down
```

## Manuelle Installation (ohne Docker)

### Voraussetzungen
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis (optional)

### Backend Setup

1. **Virtual Environment erstellen:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Dependencies installieren:**
```bash
pip install -r requirements.txt
```

3. **Datenbank erstellen:**
```bash
# PostgreSQL Terminal
createdb smartinvest_db
```

4. **Umgebungsvariablen konfigurieren:**
```bash
cp .env.example .env
# Bearbeiten Sie .env und passen Sie DATABASE_URL an
```

5. **Datenbank-Migrationen ausführen:**
```bash
alembic upgrade head
```

6. **Backend starten:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Dependencies installieren:**
```bash
cd frontend
npm install
```

2. **Umgebungsvariablen konfigurieren:**
```bash
cp .env.example .env.local
```

3. **Frontend starten:**
```bash
npm run dev
```

Frontend läuft auf: http://localhost:3000

## Entwicklung

### Backend Tests ausführen
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Linting
```bash
cd frontend
npm run lint
npm run type-check
```

### Datenbank Migration erstellen
```bash
cd backend
alembic revision --autogenerate -m "Migration message"
alembic upgrade head
```

## Beispiel-Aktien zum Testen

Probieren Sie diese Ticker aus:
- **US-Aktien:** AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA
- **Deutsche Aktien:** SAP.DE, VOW3.DE, BMW.DE
- **ETFs:** SPY, QQQ, VTI

## Troubleshooting

### Backend startet nicht
- Prüfen Sie, ob PostgreSQL läuft: `pg_isready`
- Prüfen Sie die DATABASE_URL in `.env`
- Schauen Sie in die Logs: `docker-compose logs backend`

### Frontend zeigt keine Daten
- Prüfen Sie, ob Backend erreichbar ist: http://localhost:8000/health
- Öffnen Sie Browser DevTools (F12) für Fehler
- Prüfen Sie NEXT_PUBLIC_API_URL in `.env.local`

### API Fehler "Stock not found"
- Verwenden Sie gültige Ticker-Symbole (z.B. AAPL statt Apple)
- Versuchen Sie es mit einem anderen Ticker
- yfinance hat manchmal Rate Limits - warten Sie kurz und versuchen Sie es erneut

### Docker Container startet nicht
- Prüfen Sie, ob Ports bereits belegt sind: `lsof -i :8000,3000,5432`
- Löschen Sie alte Container: `docker-compose down -v`
- Starten Sie Docker Desktop neu

## Produktiv-Deployment

### Backend (Railway/Render)
1. Erstellen Sie neues Projekt
2. Verbinden Sie GitHub Repository
3. Fügen Sie PostgreSQL Service hinzu
4. Setzen Sie Umgebungsvariablen (siehe `.env.example`)
5. Deploy wird automatisch getriggert

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

Oder verbinden Sie GitHub Repository mit Vercel Dashboard.

## Support

Bei Fragen oder Problemen:
- GitHub Issues: https://github.com/your-repo/issues
- Email: info@smartinvest.de

## Lizenz

MIT License - Siehe LICENSE Datei
