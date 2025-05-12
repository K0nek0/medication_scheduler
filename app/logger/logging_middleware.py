import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.logger.logging_config import logger
import structlog


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get('X-TRACE-ID', 'unknown')
        
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            trace_id=trace_id,
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get('user-agent'),
        )

        start_time = time.time()
        logger.info(
            "Incoming request",
            method=request.method,
            url=str(request.url),
            headers={k: v for k, v in request.headers.items() if k.lower() not in ['authorization', 'cookie']},
            query_params=dict(request.query_params),
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.error(
                "Request failed",
                exc_info=exc,
                status_code=500,
            )
            raise exc from None

        process_time = time.time() - start_time
        response.headers["X-TRACE-ID"] = trace_id
        
        logger.info(
            "Outgoing response",
            status_code=response.status_code,
            process_time=f"{process_time:.4f}s",
            response_size=response.headers.get('content-length', 0),
        )

        return response
