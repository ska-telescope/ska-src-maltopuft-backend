@unit @label
Feature: Label service
    Scenario Outline: Valid css color string parsing
        Given input value <value> is provided
        Then validation with CssColorStr type is successful

        Examples:
        | value    |
        | #cccccc  |
        | cccccc   |

    Scenario Outline: Invalid css color string parsing
        Given input value <value> is provided
        Then validation with CssColorStr type is unsuccessful

        Examples:
        | value     |
        | #ccccccc  |
        | ccccccc   |
        | asd123    |
