@integration @database
Feature: Database initialisation
    Tests related to populating the database with data during initialisation.

    Scenario: Label entities populated during initialisation
        Given an empty database
        When the database is initialised
        Then the label entities should be created

    Scenario: Label entities deleted during deinitialisation
        Given an empty database
        When the database is initialised
        And the database is deinitialised
        Then there should be no label entities in the database
