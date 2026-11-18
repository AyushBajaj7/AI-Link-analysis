"""Application configuration management via environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()

# Active LLM Provider Configuration (OpenAI is the operational implementation)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Scraper & Network Settings
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "20.0"))
MAX_WEBSITE_SIZE = int(os.getenv("MAX_WEBSITE_SIZE", str(2 * 1024 * 1024)))  # 2 MB default
MAX_REDIRECTS = int(os.getenv("MAX_REDIRECTS", "5"))

# Server Settings
PORT = int(os.getenv("PORT", "4000"))
HOST = os.getenv("HOST", "0.0.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
