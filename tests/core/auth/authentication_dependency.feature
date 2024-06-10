@unit @auth
Feature: Authenticated Dependency

    Scenario: User is authenticated
        Given authentication is enabled
        And an authenticated token
        And a request object containing an authenticated user
        Then the Authenticated dependency should be created without errors

    Scenario: User is not authenticated
        Given authentication is enabled
        And an authenticated token
        And a request object containing an unauthenticated user
        Then creating an Authenticated dependency instance should raise an AuthenticationRequiredError

    Scenario: Missing token info
        Given authentication is enabled
        And a missing token
        And a request object containing an authenticated user
        Then creating an Authenticated dependency instance should raise an AuthenticationRequiredError

    Scenario: Missing user info
        Given authentication is enabled
        And a request object contains no user information
        And an authenticated token
        Then creating an Authenticated dependency instance should raise an AuthenticationRequiredError
