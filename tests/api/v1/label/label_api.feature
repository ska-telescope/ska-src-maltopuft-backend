@integration @label
Feature: Label service
    Label service API tests.

    Scenario: Get labels with empty database
        Given an empty database
        When labels are retrieved from the database
        Then a response should be returned
        And the response data should contain an empty list
        And the status code should be HTTP 200

    Scenario: Create label
        Given a label
        When an attempt is made to create the label
        Then a response should be returned
        And the response data should contain a label
        And the status code should be HTTP 201

    Scenario: Create many labels
        Given a label
        And the labels are combined into one list
        And a label
        And the labels are combined into one list
        And a label
        And the labels are combined into one list
        When an attempt is made to create the labels
        Then a response should be returned
        And the response data should contain three label ids
        And the status code should be HTTP 201

    Scenario: Create label with null parent entity fails
        Given an empty database
        And a label
        And parent entity is None
        When an attempt is made to create the label
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Create label with null parent labeller fails
        Given an empty database
        And a label
        And parent labeller is None
        When an attempt is made to create the label
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Create label with null parent candidate fails
        Given an empty database
        And a label
        And parent candidate is None
        When an attempt is made to create the label
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Create label with non-existent parent entity fails
        Given an empty database
        And a label
        And parent entity attribute is non-existent
        When an attempt is made to create the label
        Then an error response should be returned
        And the status code should be HTTP 404

    Scenario: Create label with non-existent parent labeller fails
        Given an empty database
        And a label
        And parent labeller attribute is non-existent
        When an attempt is made to create the label
        Then an error response should be returned
        And the status code should be HTTP 404

    Scenario: Get labels
        Given a label
        And the label exists in the database
        And a label
        And the label exists in the database
        And a label
        And the label exists in the database
        When labels are retrieved from the database
        Then a response should be returned
        And the response data should contain three labels
        And the status code should be HTTP 200

    Scenario: Get existing label by id
        Given a label
        And the label exists in the database
        When the label is retrieved from the database by id
        Then a response should be returned
        And the response data should not be empty
        And the status code should be HTTP 200

    Scenario: Get non-existing label by id
        Given an empty database
        When the label is retrieved from the database by id
        Then an error response should be returned
        And the status code should be HTTP 404

    Scenario: Create duplicate label
        Given a label
        And the label exists in the database
        And a label
        And the label is for a candidate which the labeller has already labelled
        When an attempt is made to create the label
        Then an error response should be returned
        And the status code should be HTTP 409

    Scenario: Update label
        Given an 'RFI' entity
        And the entity exists in the database
        And a 'SINGLE_PULSE' entity
        And the entity exists in the database
        And a 'PERIODIC_PULSE' entity
        And the entity exists in the database
        And a label
        And the label exists in the database
        And an updated label
        When an attempt is made to update the label
        Then a response should be returned
        And the response data should contain a label
        And the status code should be HTTP 200
        When the label is retrieved from the database by id
        Then a response should be returned
        And the response data should contain the updated data
