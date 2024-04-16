@integration
@database
Feature: Backend-database connection
    Tests related to connecting the backend service to the database.

    Scenario: Application can query an available database
        Given the application is configured with a valid connection string
        Then a minimal database operation should return a valid result

    Scenario: Connection to invalid database host
        Given an invalid database hostname in the connection string
        Then a 'Database unavailable' error message is raised

    Scenario: Connection to invalid database port
        Given an invalid database port in the connection string
        Then a 'Database unavailable' error message is raised

    Scenario: Connection to invalid database user
        Given an invalid database user in the connection string
        Then a 'Database unavailable' error message is raised
