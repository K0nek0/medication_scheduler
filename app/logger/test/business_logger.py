from loguru import logger
from functools import wraps
from app.logger.test.logging_config import SensitiveDataFilter

def business_logger(operation_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            context = {
                "operation": operation_name,
                "input_params": SensitiveDataFilter.mask_user_id(kwargs)
            }
            
            try:
                result = await func(*args, **kwargs)
                logger.bind(
                    **context,
                    status="success",
                    result=SensitiveDataFilter.mask_user_id(result) if result else None
                ).info(f"{operation_name} completed")
                return result
            except Exception as e:
                logger.bind(
                    **context,
                    status="failed",
                    error_type=type(e).__name__,
                    error_msg=str(e),
                    exc_info=True
                ).error(f"{operation_name} failed")
                raise
        return wrapper
    return decorator
