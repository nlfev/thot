"""
Application main entry point
"""

import logging
from app.main import app
from app.logging_config import logger
from scripts.init_db import init_database, seed_database
from config import config

if __name__ == "__main__":
    logger.info(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    logger.info(f"Environment: {config.__class__.__name__}")

    # Initialize database
    try:
        logger.info("Initializing database...")
        init_database()
        seed_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}", exc_info=True)
        exit(1)

    # Start server
    import uvicorn

    logger.info("Starting Uvicorn server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG,
        log_config=None,  # Use our logging config
    )
