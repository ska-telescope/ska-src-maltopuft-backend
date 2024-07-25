@integration @observation
Feature: Observation service
    Observation service API tests.

    Scenario: Get observations with empty database
        Given an empty database
        When observations are retrieved from the database
        Then a response should be returned
        And the response data should contain an empty list
        And the status code should be HTTP 200

    Scenario: Get observations
        Given an observation
        And the observation exists in the database
        And an observation
        And the observation exists in the database
        And an observation
        And the observation exists in the database
        When observations are retrieved from the database
        Then a response should be returned
        And the response data should contain 3 observations
        And the status code should be HTTP 200

    Scenario: Get observation subset by time interval
        Given an observation where ("t_min", "t_max") is ("1900-01-01T00:00:00", "1900-01-02T00:00:00")
        And the observation exists in the database
        And an observation where ("t_min", "t_max") is ("2023-01-01T00:00:00", "2023-01-02T00:00:00")
        And the observation exists in the database
        And an observation where ("t_min", "t_max") is ("2023-01-01T00:00:00", "2023-01-02T00:00:00")
        And the observation exists in the database
        When the query parameters ("t_min", "t_max") have values ("2023-01-01T00:00:00", "2023-01-02T00:00:00")
        And observations are retrieved from the database 
        Then a response should be returned
        And the response data should contain 2 observations
        And the status code should be HTTP 200
