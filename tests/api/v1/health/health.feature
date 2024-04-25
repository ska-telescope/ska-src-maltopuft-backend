@integration
@health
Feature: Health check
    Tests related to running service health checks.

    Scenario: /ping endpoint returns ok
        When the /ping endpoint is called
        Then an empty response with HTTP 204 status code is returned

    Scenario: /health/app endpoint returns service health check
        When the /health/app endpoint is called
        Then a successful response with service information is returned

    Scenario: /health/db endpoint returns healthy status if db is available
        Given a database is available
        When the /health/db endpoint is called
        Then a successful response with healthy status is returned

    Scenario: /health/db endpoint returns unhealthy status if db is unavailable
        Given a database is unavailable
        When the /health/db endpoint is called from client to unavailable DB
        Then a successful response with unhealthy status is returned
