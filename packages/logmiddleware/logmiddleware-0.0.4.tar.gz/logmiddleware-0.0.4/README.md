# logmiddleware

`logmiddleware` is a Python library designed for use with FastAPI to simplify the logging of incoming requests and outgoing responses. It includes a middleware component that adds essential information to logs, such as request and response details, and supports debugging features.

## Features

- **Middleware for request and response logging:** The library provides a middleware component, `RouterLoggingMiddleware`, to log incoming requests and outgoing responses. It includes features to capture request details, response information, and execution times.

- **Request ID generation:** Automatically generates a unique request ID for each incoming request. If the request includes an `x-api-request-id` header, it uses that value; otherwise, it generates a new UUID.

- **Debugging support:** Enables debugging of response bodies through the use of the `api_debug` flag. When enabled, the response body is included in the logs.

- **JSON logging configuration:** Utilizes the `python-json-logger` library to configure JSON logging. This allows for structured and easily parsable log entries.

## Installation

To install the library, use the following pip command:

```bash
pip install logmiddleware
```

## Usage

### Setting up middleware

```python
import logging
from fastapi import FastAPI
from logmiddleware import RouterLoggingMiddleware, logging_config

# Configure JSON logging
logging.config.dictConfig(logging_config)

app = FastAPI()
# Add the middleware to your FastAPI app
app.add_middleware(
    RouterLoggingMiddleware,
    logger=logging.getLogger(__name__),  # Pass your logger instance
    api_debug=True,  # Set to True to enable debugging of response bodies
)
```

### Accessing request ID in the called function

The `execute_request` method has been updated to set the `request_id` in the `request.state`. You can now access it in the called function using `request.state.request_id`. Here is an example:

```python
# ...

@app.get("/example")
async def example_route(request: Request):
    # Accessing the request_id in the called function
    request_id = request.state.request_id
    return {"message": "Hello, world!", "request_id": request_id}
```

## Configuration

The library relies on a logging configuration dictionary (`logging_config`) to set up JSON logging. Because of that, it includes a default logging configuration (`logging_config`), which you can import for easy setup. Ensure this configuration is properly set before adding the middleware to your FastAPI app.

## Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or create a pull request on the [Git repository](https://git.slc.ar/slococo/logmiddleware).

## License

This project is licensed under the MIT license.
