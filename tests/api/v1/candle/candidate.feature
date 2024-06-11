@integration @candle @candidate
Feature: Candidate service
    Candidate service API tests.

    Scenario: Get candidates with empty database
        Given an empty database
        When candidates are retrieved from the database
        Then a response should be returned
        And the response data should contain an empty list
        And the status code should be HTTP 200

    Scenario: Create candidate
        Given a candidate
        When an attempt is made to create the candidate
        Then a response should be returned
        And the response data should contain a candidate
        And the status code should be HTTP 201

    Scenario: Get candidates
        Given a candidate
        And the candidate exists in the database
        And a candidate
        And the candidate exists in the database
        And a candidate
        And the candidate exists in the database
        When candidates are retrieved from the database
        Then a response should be returned
        And the response data should contain three candidates
        And the status code should be HTTP 200

    Scenario: Create a candidate with DM string
        Given a candidate with DM string
        When an attempt is made to create the candidate
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Create a candidate with negative DM
        Given a candidate with negative DM
        When an attempt is made to create the candidate
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Get existing candidate by id
        Given a candidate
        And the candidate exists in the database
        When the candidate is retrieved from the database by id
        Then a response should be returned
        And the response data should not be empty
        And the status code should be HTTP 200

    Scenario: Get non-existing candidate by id
        Given an empty database
        When the candidate is retrieved from the database by id
        Then an error response should be returned
        And the status code should be HTTP 404

    Scenario: Delete candidate
        Given a candidate
        And the candidate exists in the database
        When an attempt is made to delete the candidate from the database
        Then a response should be returned
        And the status code should be HTTP 204
        When the candidate is retrieved from the database by id
        Then an error response should be returned
        And the status code should be HTTP 404
