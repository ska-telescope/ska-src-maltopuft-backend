@integration @auth
Feature: User login
    Scenario: First login
        Given an empty database
        And a valid auth token
        When the token user is retrieved from the database
        Then a user should be returned

    Scenario: Login
        Given a user where ("uuid",) is ("d9e414f3-2bee-48a1-8b4b-07ee5b50473d",)
        And the user exists in the database
        And a valid auth token
        When the token user is retrieved from the database
        Then a user should be returned