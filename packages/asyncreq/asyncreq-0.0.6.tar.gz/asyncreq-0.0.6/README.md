# asyncreq

`asyncreq` is a lightweight Python library for making asynchronous HTTP requests using `aiohttp`. This library provides two convenient methods for interacting with RESTful APIs in an asynchronous manner.

## Installation

To install the library, use the following pip command:

```bash
pip install asyncreq
```

## Usage

### `make_request`

The `make_request` method allows you to make asynchronous HTTP requests with flexible options. Here's an example of how to use it:

```python
from asyncreq import make_request

async def example_usage():
    url = "https://api.example.com/resource"
    method = "GET"
    headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
    
    try:
        response_data, status_code, response_headers = await make_request(
            url=url,
            method=method,
            headers=headers,
            # Add other optional parameters as needed
        )
        print(f"Response Data: {response_data}")
        print(f"Status Code: {status_code}")
        print(f"Response Headers: {response_headers}")
    except Exception as e:
        print(f"An error occurred: {e}")
```

### `request`

The `request` method is a simplified wrapper around `make_request` with added error handling. It raises appropriate exceptions for common HTTP-related errors:

```python
from asyncreq import request, HTTPException

async def example_usage():
    url = "https://api.example.com/resource"
    method = "GET"
    headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
    
    try:
        response_data, status_code, response_headers = await request(
            url=url,
            method=method,
            headers=headers,
            # Add other optional parameters as needed
        )
        print(f"Response Data: {response_data}")
        print(f"Status Code: {status_code}")
        print(f"Response Headers: {response_headers}")
    except HTTPException as e:
        print(f"An HTTP error occurred: {e}")
```

Note: make sure to use `await` as demonstrated in the examples above.

## Dependencies

- [aiohttp](https://docs.aiohttp.org/): Asynchronous HTTP client/server framework.

## Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or create a pull request on the [Git repository](https://git.slc.ar/slococo/asyncreq).

## License

This project is licensed under the MIT license.
