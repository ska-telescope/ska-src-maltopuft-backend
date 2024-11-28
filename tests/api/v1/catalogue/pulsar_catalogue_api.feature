@integration @catalogue @pulsar
Feature: Pulsar catalogue service
    Pulsar catalogue service API tests.

    Scenario: Get pulsars with empty database
        Given an empty database
        When pulsars are retrieved from the database
        Then a response should be returned
        And the response data should contain an empty list
        And the status code should be HTTP 200

    Scenario: Get pulsars
        Given a catalogue
        And a pulsar
        And the pulsar exists in the database
        And a pulsar
        And the pulsar exists in the database
        And a pulsar
        And the pulsar exists in the database
        When pulsars are retrieved from the database
        Then a response should be returned
        And the response data should contain 3 pulsars
        And the status code should be HTTP 200

    @skip-ci
    Scenario: Pulsar cone search with point inside circle bounds
        Given a catalogue
        And a pulsar where ("ra","dec",) is (90.75270833,-40.05644444,)
        And the pulsar exists in the database
        When the query parameters ("ra","dec","radius") have values (90.75270833,-40.05644444,1)
        And pulsars are retrieved from the database
        Then a response should be returned
        And the response data should contain 1 pulsars
        And the status code should be HTTP 200

    @skip-ci
    Scenario: Pulsar cone search with point outside circle bounds
        Given a catalogue
        And a pulsar where ("ra","dec",) is (90.75270833,-40.05644444,)
        And the pulsar exists in the database
        When the query parameters ("ra","dec","radius") have values (0,0,1)
        And pulsars are retrieved from the database
        Then a response should be returned
        And the response data should contain 0 pulsars
        And the status code should be HTTP 200
