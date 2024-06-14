@integration @user
Feature: User service
    User service API tests.

    Scenario: Get users with empty database
        Given an empty database
        When users are retrieved from the database
        Then a response should be returned
        And the response data should contain an empty list
        And the status code should be HTTP 200

    Scenario: Create user
        Given a user
        When an attempt is made to create the user
        Then a response should be returned
        And the response data should contain a user
        And the status code should be HTTP 201

    Scenario: Create user sets is_admin to False by default
        Given a user with is_admin 'None'
        When an attempt is made to create the user
        Then a response should be returned
        And the response data should contain a user
        And the value of is_admin should be False
        And the status code should be HTTP 201

    Scenario: Create user is_admin can be overridden to True
        Given a user with is_admin 'True'
        When an attempt is made to create the user
        Then a response should be returned
        And the response data should contain a user
        And the value of is_admin should be True
        And the status code should be HTTP 201

    Scenario: Create user with duplicate username
        Given a user with username 'test_user'
        And the user exists in the database
        And a user with username 'test_user'
        When an attempt is made to create the user
        Then an error response should be returned
        And the status code should be HTTP 409

    Scenario: Create user with duplicate email address
        Given a user with email address 'test@example.com'
        And the user exists in the database
        And a user with email address 'test@example.com'
        When an attempt is made to create the user
        Then an error response should be returned
        And the status code should be HTTP 409

    Scenario: Create user with duplicate uuid
        Given a user with uuid 'd9e414f3-2bee-48a1-8b4b-07ee5b50473d'
        And the user exists in the database
        And a user with uuid 'd9e414f3-2bee-48a1-8b4b-07ee5b50473d'
        When an attempt is made to create the user
        Then an error response should be returned
        And the status code should be HTTP 409

    Scenario: Create a user with invalid email address
        Given a user with email address 'this is not an email address'
        When an attempt is made to create the user
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Create a user with invalid uuid
        Given a user with uuid is 'this is not a uuid'
        When an attempt is made to create the user
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Get users
        Given a user
        And the user exists in the database
        And a user
        And the user exists in the database
        And a user
        And the user exists in the database
        When users are retrieved from the database
        Then a response should be returned
        And the response data should contain three users
        And the status code should be HTTP 200

    Scenario: Get existing user by id
        Given a user
        And the user exists in the database
        When the user is retrieved from the database by id
        Then a response should be returned
        And the response data should not be empty
        And the status code should be HTTP 200

    Scenario: Get non-existing user by id
        Given an empty database
        When the user is retrieved from the database by id
        Then an error response should be returned
        And the status code should be HTTP 404
