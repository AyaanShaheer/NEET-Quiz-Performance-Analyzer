import logging
import traceback
from functools import wraps
import os

class NEETAnalyticsLogger:
    @staticmethod
    def setup_logging():
        """Configure logging with multiple handlers"""
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/neet_analytics.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    @staticmethod
    def exception_handler(func):
        """Decorator for comprehensive error handling"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                logger.error(traceback.format_exc())
                raise
        return wrapper