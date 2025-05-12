import grpc
from loguru import logger
from uuid import uuid4
import time
from app.logger.test.logging_config import SensitiveDataFilter

class LoggingInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        trace_id = str(uuid4())
        
        # Логирование входящего запроса
        logger.bind(
            type="grpc_request",
            trace_id=trace_id,
            method=method,
            timestamp=time.time()
        ).info("gRPC request received")

        start_time = time.time()
        
        try:
            response = await continuation(handler_call_details)
            process_time = time.time() - start_time
            
            # Логирование успешного ответа
            logger.bind(
                type="grpc_response",
                trace_id=trace_id,
                method=method,
                status_code="OK",
                process_time=round(process_time, 4),
                timestamp=time.time()
            ).info("gRPC response sent")
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            status_code = getattr(e, 'code', grpc.StatusCode.INTERNAL)
            
            logger.bind(
                type="grpc_error",
                trace_id=trace_id,
                method=method,
                status_code=str(status_code),
                error_type=type(e).__name__,
                error_msg=SensitiveDataFilter.mask_user_id(str(e)),
                process_time=round(process_time, 4),
                exc_info=True,
                timestamp=time.time()
            ).error("gRPC processing error")
            
            raise

    def _mask_request_data(self, request):
        if hasattr(request, 'user_id'):
            request.user_id = "***USER_ID***"
        return request
