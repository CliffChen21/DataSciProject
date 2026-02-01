# DataSciProject Development Guide

## Quick Start

### Backend Setup (macOS)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp ../.env.example .env
# Edit .env with your API keys

# Run the application
python app.py
```

The backend API will be available at `http://localhost:5000`

### Frontend Setup (Coming Soon)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## API Endpoints

### Health Check
- `GET /` - Health check endpoint

### News (New Blueprint Routes)
- `GET /api/news/fetch?keyword=<keyword>&limit=<limit>` - Fetch news articles
  - Supports multiple sources: Baidu News, Snowball (Xueqiu), RSS
- `GET /api/news/sources` - Get available news sources
  - Includes: Google News, Bing News, Baidu News (百度), Snowball/Xueqiu (雪球)

### Analysis (New Blueprint Routes)
- `POST /api/analysis/sentiment` - Sentiment analysis
  - Body: `{"texts": ["text1", "text2"]}`
- `POST /api/analysis/topic` - Topic modeling
  - Body: `{"texts": ["text1", "text2"], "num_topics": 3}`

### Visualization (New Blueprint Routes)
- `POST /api/viz/generate` - Generate chart configuration
  - Body: `{"data": [{"label": "A", "value": 10}], "chart_type": "bar"}`
- `GET /api/viz/types` - Get supported chart types

### Legacy Endpoints (Backward Compatible)
- `GET /fetch_news?keyword=<keyword>` - Fetch news (deprecated, use `/api/news/fetch`)
- `POST /analyze` - Text analysis (deprecated, use `/api/analysis/*`)
- `POST /plot` - Generate chart (deprecated, use `/api/viz/generate`)

## Project Structure

```
backend/
├── api/                    # API blueprint routes
│   ├── news.py            # News endpoints
│   ├── analysis.py        # Analysis endpoints
│   └── visualization.py   # Visualization endpoints
├── data/                  # Data fetching modules
│   ├── news_fetcher.py   # News API/RSS integration
│   └── web_scraper.py    # Web scraping utilities
├── analysis/             # Text analysis modules
│   ├── text_analyzer.py  # ML/DL analysis
│   └── text_preprocessor.py  # Text cleaning
├── visualization/        # Chart generation
│   └── chart_generator.py  # Plotly config generator
├── models/               # ML/DL model definitions
├── utils/               # Utility functions
│   ├── database.py     # Database connection
│   ├── helpers.py      # Helper functions
│   └── logger.py       # Logging setup
├── app.py              # Flask application entry
├── config.py           # Configuration
└── requirements.txt    # Python dependencies
```

## Development Workflow

1. **Local Development**: Use SQLite database and mock data
2. **API Testing**: Use curl, Postman, or Thunder Client
3. **Frontend Integration**: React app will call backend APIs
4. **Production Deploy**: Move to Ali Cloud with PostgreSQL

## Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=backend tests/
```

## Environment Variables

See `.env.example` for all available configuration options.

## Next Steps

- [ ] Implement real news API integration (Google News, Bing News)
- [ ] Add actual ML/DL models (transformers for sentiment analysis)
- [ ] Create React frontend
- [ ] Add database models and persistence
- [ ] Implement authentication
- [ ] Add comprehensive tests
- [ ] Setup CI/CD pipeline
