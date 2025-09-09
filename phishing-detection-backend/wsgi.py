import os
import logging
import signal
import sys
from app import app
from app.config import config

# Configure logging for production
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/app.log') if os.path.exists('/tmp') else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)

# Graceful shutdown handler for Oracle Cloud
def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# For Oracle Cloud Container Instances and other WSGI servers
application = app

# Log startup information
logger.info("=== Phishing Detection API Starting ===")
logger.info(f"Debug mode: {config.DEBUG}")
logger.info(f"Log level: {config.LOG_LEVEL}")
logger.info(f"Port: {config.PORT}")

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", config.PORT))
    logger.info(f"Starting development server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=config.DEBUG)