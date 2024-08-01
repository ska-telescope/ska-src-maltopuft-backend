@integration @label @entity
Feature: Entity service
    Entity service API tests.

    Scenario: Get entities with empty database
        Given an empty database
        When entities are retrieved from the database
        Then a response should be returned
        And the response data should contain an empty list
        And the status code should be HTTP 200

    Scenario: Create RFI entity
        Given an 'RFI' entity
        When an attempt is made to create the entity
        Then a response should be returned
        And the response data should contain an 'RFI' entity
        And the status code should be HTTP 201

    Scenario: Create single pulse entity
        Given a 'SINGLE_PULSE' entity
        When an attempt is made to create the entity
        Then a response should be returned
        And the response data should contain a 'SINGLE_PULSE' entity
        And the status code should be HTTP 201

    Scenario: Create periodic pulse entity
        Given a 'PERIODIC_PULSE' entity
        When an attempt is made to create the entity
        Then a response should be returned
        And the response data should contain a 'PERIODIC_PULSE' entity
        And the status code should be HTTP 201

    Scenario: Create entity with duplicate type
        Given an 'RFI' entity
        And the entity exists in the database
        And an 'RFI' entity
        When an attempt is made to create the entity
        Then an error response should be returned
        And the status code should be HTTP 409

    Scenario: Create entity with duplicate css color
        Given an entity with css_color 'cccccc'
        And the entity exists in the database
        And an entity with css_color 'cccccc'
        When an attempt is made to create the entity
        Then an error response should be returned
        And the status code should be HTTP 409

    Scenario: Get entities
        Given an 'RFI' entity
        And the entity exists in the database
        And a 'SINGLE_PULSE' entity
        And the entity exists in the database
        And a 'PERIODIC_PULSE' entity
        And the entity exists in the database
        When entities are retrieved from the database
        Then a response should be returned
        And the response data should contain 3 entities
        And the status code should be HTTP 200

    Scenario: Create an entity with invalid type
        Given an entity with invalid type
        When an attempt is made to create the entity
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Create an entity with invalid css_color
        Given an entity with invalid css_color
        When an attempt is made to create the entity
        Then a validation error response should be returned
        And the status code should be HTTP 422

    Scenario: Get existing entity by id
        Given an 'RFI' entity
        And the entity exists in the database
        When the entity is retrieved from the database by id
        Then a response should be returned
        And the response data should not be empty
        And the status code should be HTTP 200

    Scenario: Get non-existing entity by id
        Given an empty database
        When the entity is retrieved from the database by id
        Then an error response should be returned
        And the status code should be HTTP 404
