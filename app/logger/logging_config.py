import structlog
import logging
from typing import Dict, Any
from datetime import datetime

def mask_sensitive_data(event_dict: Dict[str, Any]) -> Dict[str, Any]:
    if 'user_id' in event_dict:
        event_dict['user_id'] = '***'
    return event_dict

def add_timestamp(logger, method_name, event_dict) -> Dict[str, Any]:
    event_dict['timestamp'] = datetime.utcnow().isoformat()
    return event_dict

def setup_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            add_timestamp,
            mask_sensitive_data,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
        handlers=[logging.StreamHandler()]
    )
    logging.getLogger().handlers = []
    logging.getLogger().addHandler(logging.StreamHandler())

setup_logging()
logger = structlog.get_logger()
