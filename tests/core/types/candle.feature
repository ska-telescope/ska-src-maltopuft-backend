@unit @candidate @candle @types
Feature: Candidate handler
    Scenario Outline: Valid RightAscensionDegrees type
        Given valid input value <value> is provided
        Then validation with RightAscensionDegrees type is successful

        Examples:
        | value       |
        | 0           |
        | 360         |
        | 0.00000     |
        | 360.00000   |

    Scenario Outline: Valid DeclinationDegrees type
        Given valid input value <value> is provided
        Then validation with DeclinationDegrees type is successful

        Examples:
        | value     |
        | -90       |
        | -90.00000 |
        | 0         |
        | 0.00000   |
        | 90        |

    Scenario Outline: Invalid RightAscensionDegrees type
        Given invalid input value <value> is provided
        Then validation with RightAscensionDegrees type raises a ValidationError

        Examples:
        | value      |
        | -0.500001  |
        | 360.500001 |

    Scenario Outline: Invalid DeclinationDegrees type
        Given invalid input value <value> is provided
        Then validation with DeclinationDegrees type raises a ValidationError

        Examples:
        | value      |
        | 90.500001  |
        | 90.1       |
        | -90.1      |
        | -90.500001 |
