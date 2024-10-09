@integration @auth
Feature: User login
    Scenario: Token user first login
        Given an empty database
        And a valid auth token
        When the token user is retrieved from the database
        Then a user should be returned

    Scenario: Token user login
        Given a user where ("uuid",) is ("d9e414f3-2bee-48a1-8b4b-07ee5b50473d",)
        And the user exists in the database
        And a valid auth token
        When the token user is retrieved from the database
        Then a user should be returned

    Scenario: Test user first login
        Given an empty database
        When the test user is retrieved from the database
        Then a user should be returned

    Scenario: Test user login
        Given a user where ("username",) is ("admin",)
        And the user exists in the database
        When the test user is retrieved from the database
        Then a user should be returned
