"""
Application configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = DATA_DIR / "database"
CACHE_DIR = DATA_DIR / "cache"
RESOURCES_DIR = BASE_DIR / "src" / "resources"

# Database
DATABASE_PATH = DATABASE_DIR / "healthtrack.db"

# API Keys (from .env file)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# App Settings
APP_VERSION = "1.0.0"
APP_NAME = "HealthTrack AI Pro"
COMPANY_NAME = "HealthTrack"

# Theme
DEFAULT_THEME = "dark"  # 'dark' or 'light'

# AI Settings
AI_MODEL = "gpt-4"
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 1000

# Smartwatch Settings
SYNC_INTERVAL = 300  # seconds (5 minutes)
REALTIME_UPDATE_INTERVAL = 5  # seconds

# Health Targets (default)
DEFAULT_STEPS_GOAL = 10000
DEFAULT_CALORIES_GOAL = 2000
DEFAULT_WATER_GOAL = 2000  # ml
DEFAULT_SLEEP_GOAL = 8  # hours
