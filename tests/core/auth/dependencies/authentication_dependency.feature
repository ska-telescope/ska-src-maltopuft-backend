Feature: Authenticated Dependency

    Scenario: User is authenticated
        Given an authenticated token
        And a request object containing an authenticated user
        Then the Authenticated dependency should be created without errors

    Scenario: User is not authenticated
        Given an authenticated token
        And a request object containing an unauthenticated user
        Then creating an Authenticated dependency instance should raise an AuthenticationRequiredError

    Scenario: Missing token info
        Given a missing token
        And a request object containing an authenticated user
        Then creating an Authenticated dependency instance should raise an AuthenticationRequiredError

    Scenario: Missing user info
        Given a request object contains no user information
        And an authenticated token
        Then creating an Authenticated dependency instance should raise an AuthenticationRequiredError
