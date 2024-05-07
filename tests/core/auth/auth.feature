@unit
@auth
Feature: TokenBearerAuthBackend
    Scenario: Valid bearer token extraction
        Given an authentication header with a valid bearer token
        Then the token is extracted and returned

    Scenario: Invalid or unsupported authentication scheme
        Given an authentication header with an invalid authentication scheme
        Then an AuthenticationError is raised for invalid or unsupported authentication scheme
        And on_auth_error returns a JSONResponse with HTTP 401 status code

    Scenario: Missing authorization header returns unauthenticated user
        Given no authorization header is present in the request
        When the authentication middleware is executed
        Then nothing is returned

    Scenario: Valid bearer token returns authenticated user
        Given an authentication header with a valid bearer token
        When the authentication middleware is executed
        Then authenticated user data is parsed
