@echo off
REM VS Code debug environment for DataSciProject (Windows)

set FLASK_ENV=development
set API_HOST=127.0.0.1
set API_PORT=5000
set DATABASE_URL=sqlite:///data/app.db

REM Optional API keys
REM set NEWS_API_KEY=
REM set BING_NEWS_API_KEY=
REM set OPENAI_API_KEY=

REM Optional paths
REM set DATA_DIR=./data
REM set MODEL_DIR=./models/cache
REM set OUTPUT_DIR=./output

echo VS Code debug environment variables set.
