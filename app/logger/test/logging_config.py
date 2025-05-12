from loguru import logger
import sys
from uuid import uuid4
from typing import Dict, Any
import re

class SensitiveDataFilter:
    @staticmethod
    def mask_user_id(data: Any) -> Any:
        masked_data = data.copy()
        if 'user_id' in masked_data:
            masked_data['user_id'] = '***'
        return masked_data

    @staticmethod
    def filter_headers(headers: Dict[str, str]) -> Dict[str, str]:
        sensitive = {'authorization', 'cookie', 'set-cookie', 'api-key'}
        return {k: ('***MASKED***' if k.lower() in sensitive else v) for k, v in headers.items()}

def configure_logging():
    logger.remove()
    
    logger.add(
        sys.stdout,
        format="{message}",
        # serialize=True,
        # backtrace=True,
        # diagnose=True,
        level="INFO",
        filter=lambda record: "sensitive" not in record["extra"]
    )
    
    logger.add(
        "logs/api_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="30 days",
        compression="zip",
        serialize=True,
        level="DEBUG"
    )
