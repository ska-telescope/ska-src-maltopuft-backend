@unit @candidate
Feature: Candidate handler
    Scenario Outline: RA pattern matching
        Given input value <value> is provided
        When value is pattern matched against the ra regex
        Then pattern matching should return <expected>

        Examples:
        | value        | expected |
        | 3h31m46.23s  | True     |
        | 5h00m57.54s  | True     |
        | 5:00:57.54   | None     |
        | 5000057054   | None     |
        | ah00m57.54s  | None     |
        | a:00:57.54   | None     |
        | 5?00:57.54   | None     |
        | 5ha0m57.54s  | None     |
        | 5:a0:57.54   | None     |
        | 5:00:57.aa   | None     |
        | 5:00:57:54   | None     |
        | 5.00.57.54   | None     |
        | abcdefghij   | None     |
        | £%?a"2l;2'   | None     |
        | ahcdmfg.ijs  | None     |
        | a:cd:fg.ij   | None     |
        | -27h49m16.8s | None     |
        | -27:49:16.8  | None     |
        | -25h55m03.5s | None     |
        | -25:55:03.5  | None     |

    Scenario Outline: Dec pattern matching
        Given input value <value> is provided
        When value is pattern matched against the dec regex
        Then pattern matching should return <expected>

        Examples:
        | value        | expected |
        | -27d49m16.8s | True     |
        | -27:49:16.8  | None     |
        | -25d55m03.5s | True     |
        | -25:55:03.5  | None     |
        | ?25:55:03.5  | None     |
        | 5000057054   | None     |
        | ad00m57.54s  | None     |
        | a:00:57.54   | None     |
        | 5?00:57.54   | None     |
        | 5:a0:57.54   | None     |
        | 5:00:57.aa   | None     |
        | 5:00:57:54   | None     |
        | 5.00.57.54   | None     |
        | abcdefghij   | None     |
        | £%?a"2l;2'   | None     |
        | adcdmfg.ijs  | None     |
        | a:cd:fg.ij   | None     |
        | 3d31m46.23s  | None     |
        | 3:31:46.23   | None     |
        | 5d00m57.54s  | None     |
        | 5:00:57.54   | None     |

    Scenario Outline: Valid RaStr type
        Given valid input value <value> is provided
        Then validation with RaStr type is successful

        Examples:
        | value        |
        | 3h31m46.23s  |
        | 5h00m57.54s  |

    Scenario Outline: Valid DecStr type
        Given valid input value <value> is provided
        Then validation with DecStr type is successful

        Examples:
        | value        |
        | -27d49m16.8s |
        | -25d55m03.5s |

    Scenario Outline: Invalid RaStr type
        Given invalid input value <value> is provided
        Then validation with RaStr type raises a ValidationError

        Examples:
        | value        |
        | 5:00:57.54   |
        | 5000057054   |
        | ah00m57.54s  |
        | a:00:57.54   |
        | 5?00:57.54   |
        | 5ha0m57.54s  |
        | 5:a0:57.54   |
        | 5:00:57.aa   |
        | 5:00:57:54   |
        | 5.00.57.54   |
        | abcdefghij   |
        | £%?a"2l;2'   |
        | ahcdmfg.ijs  |
        | a:cd:fg.ij   |
        | -27h49m16.8s |
        | -27:49:16.8  |
        | -25h55m03.5s |
        | -25:55:03.5  |

    Scenario Outline: Invalid DecStr type
        Given invalid input value <value> is provided
        Then validation with DecStr type raises a ValidationError

        Examples:
        | value       |
        | ?25:55:03.5 |
        | 5000057054  |
        | ad00m57.54s |
        | a:00:57.54  |
        | 5?00:57.54  |
        | 5:a0:57.54  |
        | 5:00:57.aa  |
        | 5:00:57:54  |
        | 5.00.57.54  |
        | abcdefghij  |
        | £%?a"2l;2'  |
        | adcdmfg.ijs |
        | a:cd:fg.ij  |
        | 3d31m46.23s |
        | 3:31:46.23  |
        | 5d00m57.54s |
        | 5:00:57.54  |
