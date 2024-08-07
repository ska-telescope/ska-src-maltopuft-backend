@unit @candidate @candle @types
Feature: Candidate handler
    Scenario Outline: RA pattern matching
        Given input value <value> is provided
        When value is pattern matched against the ra regex
        Then pattern matching should return <expected>

        Examples:
        | value        | expected |
        | 0h12m34s     | True     |
        | 1h01m01s     | True     |
        | 9h59m59s     | True     |
        | 10h10m10s    | True     |
        | 0h00m00s     | True     |
        | 1h23m45.6s   | True     |
        | 2h34m56.78s  | True     |
        | 0h12m34.9s   | True     |
        | 3h45m67.01s  | True     |
        | 7h08m09.0s   | True     |
        | 0h00m00.00s  | True     |
        | 9h59m59.99s  | True     |
        | h12m34s      | None     |
        | 0h12m34      | None     |
        | 0h12m        | None     |
        | 0h123m45s    | None     |
        | 0h12m345s    | None     |
        | 0h12m34.s    | None     |
        | 0h12m34xs    | None     |
        | ah12m34s     | None     |
        | 0h00m00.000s | None     |

    Scenario Outline: Dec pattern matching
        Given input value <value> is provided
        When value is pattern matched against the dec regex
        Then pattern matching should return <expected>

        Examples:
        | value        | expected |
        | 0d12m34s     | True     |
        | 1d01m01s     | True     |
        | 9d59m59s     | True     |
        | 10d10m10s    | True     |
        | -0d00m00s    | True     |
        | -9d23m45s    | True     |
        | 1d23m45.6s   | True     |
        | 2d34m56.7s   | True     |
        | 0d12m34.9s   | True     |
        | -3d45m67.0s  | True     |
        | 7d08m09.5s   | True     |
        | 0d00m00.0s   | True     |
        | 9d59m59.9s   | True     |
        | -9d59m59.9s  | True     |
        | d12m34s      | None     |
        | 0d12m34      | None     |
        | 0d12m        | None     |
        | 0d123m45s    | None     |
        | 0d12m345s    | None     |
        | 0d12m34.s    | None     |
        | 0d12m34xs    | None     |
        | ad12m34s     | None     |
        | 0d00m00.00s  | None     |
        | 0d00m00.000s | None     |

    Scenario Outline: Valid RaStr type
        Given valid input value <value> is provided
        Then validation with RaStr type is successful

        Examples:
        | value       |
        | 0h12m34s    |
        | 1h01m01s    |
        | 9h59m59s    |
        | 10h10m10s   |
        | 0h00m00s    |
        | 1h23m45.6s  |
        | 2h34m56.78s |
        | 0h12m34.9s  |
        | 3h45m67.01s |
        | 7h08m09.0s  |
        | 0h00m00.00s |
        | 9h59m59.99s |

    Scenario Outline: Valid DecStr type
        Given valid input value <value> is provided
        Then validation with DecStr type is successful

        Examples:
        | value       |
        | 0d12m34s    |
        | 1d01m01s    |
        | 9d59m59s    |
        | 10d10m10s   |
        | -0d00m00s   |
        | -9d23m45s   |
        | 1d23m45.6s  |
        | 2d34m56.7s  |
        | 0d12m34.9s  |
        | -3d45m67.0s |
        | 7d08m09.5s  |
        | 0d00m00.0s  |
        | 9d59m59.9s  |
        | -9d59m59.9s |

    Scenario Outline: Invalid RaStr type
        Given invalid input value <value> is provided
        Then validation with RaStr type raises a ValidationError

        Examples:
        | value        |
        | h12m34s      |
        | 0h12m34      |
        | 0h12m        |
        | 0h123m45s    |
        | 0h12m345s    |
        | 0h12m34.s    |
        | 0h12m34xs    |
        | ah12m34s     |
        | 0h00m00.000s |

    Scenario Outline: Invalid DecStr type
        Given invalid input value <value> is provided
        Then validation with DecStr type raises a ValidationError

        Examples:
        | value        |
        | d12m34s      |
        | 0d12m34      |
        | 0d12m        |
        | 0d123m45s    |
        | 0d12m345s    |
        | 0d12m34.s    |
        | 0d12m34xs    |
        | ad12m34s     |
        | 0d00m00.00s  |
        | 0d00m00.000s |
