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
        Given observation metadata exists in the database
        And a candidate
        When an attempt is made to create the candidate
        Then a response should be returned
        And the response data should contain 1 candidates
        And the status code should be HTTP 201

    Scenario: Get candidates
        Given observation metadata exists in the database
        And a candidate
        And the candidate exists in the database
        And a candidate
        And the candidate exists in the database
        And a candidate
        And the candidate exists in the database
        When candidates are retrieved from the database
        Then a response should be returned
        And the response data should contain 3 candidates
        And the status code should be HTTP 200

    Scenario: Create a candidate with DM string
        Given observation metadata exists in the database
        And a candidate with DM string
        When an attempt is made to create the candidate
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Create a candidate with negative DM
        Given observation metadata exists in the database
        And a candidate with negative DM
        When an attempt is made to create the candidate
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Get existing candidate by id
        Given observation metadata exists in the database
        And a candidate
        And the candidate exists in the database
        When the candidate is retrieved from the database by id
        Then a response should be returned
        And the response data should not be empty
        And the status code should be HTTP 200

    Scenario: Get non-existing candidate by id
        Given observation metadata exists in the database
        And an empty database
        When the candidate is retrieved from the database by id
        Then an error response should be returned
        And the status code should be HTTP 404

    Scenario: Delete candidate
        Given observation metadata exists in the database
        And a candidate
        And the candidate exists in the database
        When an attempt is made to delete the candidate from the database
        Then a response should be returned
        And the status code should be HTTP 204
        When the candidate is retrieved from the database by id
        Then an error response should be returned
        And the status code should be HTTP 404

    @skip-ci
    Scenario: Cone search with point inside circle bounds
        Given observation metadata exists in the database
        And a candidate where ("ra","dec",) is ("6h03m00.65s","-40d03m23.2s",)
        And the candidate exists in the database
        When the query parameters ("ra","dec","radius") have values ("6h03m00.65s","-40d03m23.2s",1)
        And candidates are retrieved from the database
        Then a response should be returned
        And the response data should contain 1 candidates
        And the status code should be HTTP 200

    @skip-ci
    Scenario: Cone search with point outside circle bounds
        Given observation metadata exists in the database
        And a candidate where ("ra","dec",) is ("6h03m00.65s","-40d03m23.2s",)
        And the candidate exists in the database
        When the query parameters ("ra","dec","radius") have values ("50h03m00.65s","-50d03m23.2s",1)
        And candidates are retrieved from the database
        Then a response should be returned
        And the response data should contain 0 candidates
        And the status code should be HTTP 200
