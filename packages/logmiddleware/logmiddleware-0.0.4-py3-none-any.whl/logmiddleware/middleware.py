import json
import logging
import sys
import time
from typing import Callable
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

logging_config = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stderr,
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console"], "propagate": True},
}


class RouterLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, *, logger: logging.Logger, api_debug: bool = False) -> None:
        self._logger = logger
        self.api_debug = api_debug
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_header = request.headers.get("x-api-request-id")
        if request_header is not None:
            request_id = request_header
        else:
            request_id: str = str(uuid4())
        
        logging_dict = {"X-API-REQUEST-ID": request_id}

        if self.api_debug:
            await self.set_body(request)

        response, response_dict = await self._log_response(
            call_next, request, request_id
        )
        request_dict = await self._log_request(request)
        logging_dict["request"] = request_dict
        logging_dict["response"] = response_dict

        self._logger.info(logging_dict)

        return response

    async def set_body(self, request: Request):
        _receive = await request._receive()

        async def receive() -> Message:
            return _receive

        request._receive = receive

    async def _log_request(self, request: Request) -> str:
        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"

        request_logging = {
            "method": request.method,
            "path": path,
            "ip": request.client.host,
        }

        if self.api_debug:
            try:
                body = await request.json()
                request_logging["body"] = body
            except ValueError:
                body = None

        return request_logging

    async def _log_response(
        self, call_next: Callable, request: Request, request_id: str
    ) -> Response:
        start_time = time.perf_counter()
        response = await self._execute_request(call_next, request, request_id)
        finish_time = time.perf_counter()

        overall_status = "successful" if response.status_code < 400 else "failed"
        execution_time = finish_time - start_time

        response_logging = {
            "status": overall_status,
            "status_code": response.status_code,
            "time_taken": f"{execution_time:0.4f}s",
        }

        if self.api_debug and response.status_code != 204:
            resp_body = [
                section async for section in response.__dict__["body_iterator"]
            ]
            response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))

            try:
                resp_body = json.loads(resp_body[0].decode())
            except ValueError:
                resp_body = str(resp_body)

            response_logging["body"] = resp_body

        return response, response_logging

    async def _execute_request(
        self, call_next: Callable, request: Request, request_id: str
    ) -> Response:
        try:
            request.state.request_id = request_id
            response: Response = await call_next(request)

            response.headers["X-API-Request-ID"] = request_id
            return response

        except Exception as e:
            self._logger.exception(
                {"path": request.url.path, "method": request.method, "reason": e}
            )


class AsyncIteratorWrapper:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
