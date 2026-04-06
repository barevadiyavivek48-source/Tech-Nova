import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Basic gunicorn configuration
workers = int(os.environ.get('WEB_CONCURRENCY', 1))
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
timeout = 120
max_requests = 1000
max_requests_jitter = 100
