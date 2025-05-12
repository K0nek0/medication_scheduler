from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
from uuid import uuid4
import time
from app.logger.test.logging_config import SensitiveDataFilter

class APILoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get('x-trace-id', str(uuid4()))
        context = {
            "trace_id": trace_id,
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get('user-agent')
            # "endpoint": request.url.path
        }

        await self._log_request(request, context)
        
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            await self._log_response(response, context, process_time)
            return response
        except HTTPException as e:
            process_time = time.time() - start_time
            logger.bind(
                **context,
                status_code=e.status_code,
                error_detail=SensitiveDataFilter.mask_user_id(e.detail),
                process_time=process_time
            ).error("API Error")
            raise
        except Exception as e:
            process_time = time.time() - start_time
            logger.bind(
                **context,
                status_code=500,
                error_type=type(e).__name__,
                error_msg=str(e),
                process_time=process_time,
                exc_info=True
            ).error("Unexpected Error")
            raise

    async def _log_request(self, request: Request, context: dict):
        log_data = {
            "method": request.method,
            "url": str(request.url),
            "headers": SensitiveDataFilter.filter_headers(dict(request.headers)),
            "query_params": SensitiveDataFilter.mask_user_id(dict(request.query_params)),
            "timestamp": time.time()
        }
        
        if request.method != "GET":
            try:
                body = await request.json()
                log_data["body"] = SensitiveDataFilter.mask_user_id(body)
            except:
                body = await request.body()
                if body:
                    log_data["body"] = SensitiveDataFilter.mask_user_id(body.decode('utf-8'))
        
        logger.bind(**context, **log_data).info("API Request")

    async def _log_response(self, response: Response, context: dict, process_time: float):
        response_size = len(response.body) if hasattr(response, 'body') else 0
        
        log_data = {
            "status_code": response.status_code,
            "process_time": round(process_time, 4),
            "response_size": response_size,
            "timestamp": time.time()
        }
        
        logger.bind(**context, **log_data).info("API Response")
