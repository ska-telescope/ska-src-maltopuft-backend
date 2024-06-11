"""Generic API response status codes."""

api_responses = {
    200: {"description": "Success."},
    201: {"description": "Created successfully."},
    204: {"description": "No content."},
    401: {"description": "Authentication required."},
    403: {"description": "Permission denied."},
    404: {"description": "Not found."},
    409: {"description": "Conflict."},
    422: {"description": "Validation error."},
}
