@unit @auth
Feature: Authorization Dependency
    Scenario Outline: Valid authorization scopes
        Given a request object containing valid <scopes>
        When the AuthorizationChecker checks for valid <required>
        Then the AuthorizationChecker dependency should be called without errors

        Examples:
        | scopes                 | required            |
        | src                    | src                 |
        | src/maltopuft/admin    | src/maltopuft/admin |
        | src,src/maltopuft      | src/maltopuft       |


    Scenario Outline: Invalid authorization scopes
        Given a request object containing invalid <scopes>
        When the AuthorizationChecker checks for invalid <required>
        Then the AuthorizationChecker dependency should raise a PermissionDeniedError

        Examples:
        | scopes                 | required            |
        | src,src/maltopuft/user | src/maltopuft       |
        | src/maltopuft/admin    | src                 |
