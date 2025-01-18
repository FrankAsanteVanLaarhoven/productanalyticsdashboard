# airflow_project/dags/amazon_sales_etl/utils/logger.py
import logging
import json
from typing import Dict, Any

class ETLLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging format"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def log_stats(self, stats: Dict[str, Any], stage: str):
        """Log statistics with proper formatting"""
        self.logger.info(f"{stage} statistics: {json.dumps(stats, indent=2)}")
    
    def log_error(self, error: Exception, stage: str):
        """Log errors with full traceback"""
        self.logger.error(f"{stage} failed: {str(error)}", exc_info=True)