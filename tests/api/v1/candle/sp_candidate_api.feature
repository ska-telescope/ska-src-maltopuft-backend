@integration @candle @sp
Feature: Single pulse candidate service
    Single pulse candidate service API tests.

    Scenario: Get sp candidates with empty database
        Given an empty database
        When sp candidates are retrieved from the database
        Then a response should be returned
        And the response data should contain an empty list
        And the status code should be HTTP 200

    Scenario: Create sp candidate
        Given a sp candidate
        When an attempt is made to create the sp candidate
        Then a response should be returned
        And the response data should contain a sp candidate
        And the status code should be HTTP 201

    Scenario: Create sp candidate with null parent
        Given an empty database
        And a sp candidate with null parent candidate attribute
        When an attempt is made to create the sp candidate
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Create sp candidate with non-existent parent
        Given an empty database
        And a sp candidate with non-existent parent candidate attribute
        When an attempt is made to create the sp candidate
        Then an error response should be returned
        And the status code should be HTTP 404

    Scenario: Get sp candidates
        Given a sp candidate
        And the sp candidate exists in the database
        And a sp candidate
        And the sp candidate exists in the database
        And a sp candidate
        And the sp candidate exists in the database
        When sp candidates are retrieved from the database
        Then a response should be returned
        And the response data should contain three sp candidates
        And the status code should be HTTP 200

    Scenario: Get existing sp candidate by id
        Given a sp candidate
        And the sp candidate exists in the database
        When the sp candidate is retrieved from the database by id
        Then a response should be returned
        And the response data should not be empty
        And the status code should be HTTP 200

    Scenario: Get non-existing sp candidate by id
        Given an empty database
        When the sp candidate is retrieved from the database by id
        Then an error response should be returned
        And the status code should be HTTP 404

    Scenario: Delete sp candidate
        Given a sp candidate
        And the sp candidate exists in the database
        When an attempt is made to delete the sp candidate from the database
        Then a response should be returned
        And the status code should be HTTP 204
        When the sp candidate is retrieved from the database by id
        Then an error response should be returned
        And the status code should be HTTP 404

    Scenario: Count sp candidate
        Given a sp candidate
        And the sp candidate exists in the database
        And a sp candidate
        And the sp candidate exists in the database
        When an attempt is made to count the sp candidates
        Then a response should be returned
        And the status code should be HTTP 200
        And the response should equal 2

    Scenario: Count sp candidate after deletion
        Given a sp candidate
        And the sp candidate exists in the database
        And a sp candidate
        And the sp candidate exists in the database
        When an attempt is made to delete the sp candidate from the database
        And an attempt is made to count the sp candidates
        Then a response should be returned
        And the status code should be HTTP 200
        And the response should equal 1

    Scenario: Count sp candidates with empty database
        Given an empty database
        When an attempt is made to count the sp candidates
        Then a response should be returned
        And the status code should be HTTP 200
        And the response should equal 0

    Scenario: Count sp candidate with query parameters
        Given a sp candidate
        And the sp candidate exists in the database
        When an attempt is made to count the sp candidates
        Then a response should be returned
        And the status code should be HTTP 200
        And the response should equal 1
        When an attempt is made to count the sp candidates with non-existent query parameters
        Then a response should be returned
        And the status code should be HTTP 200
        And the response should equal 0
