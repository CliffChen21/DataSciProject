"""
Application Configuration
Uses environment variables for production/development separation
"""
import os
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).parent.parent

# Environment variables
ENV = os.getenv('FLASK_ENV', 'development')

# Database configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f'sqlite:///{BASE_DIR}/data/app.db'  # SQLite for local development
)

# API configuration
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 5000))
DEBUG = ENV == 'development'

# News API keys (load from environment variables)
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
BING_NEWS_API_KEY = os.getenv('BING_NEWS_API_KEY', '')

# LLM API configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')

# Data storage paths
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Model cache path
MODEL_DIR = BASE_DIR / 'models' / 'cache'
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Chart output path
OUTPUT_DIR = BASE_DIR / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)
