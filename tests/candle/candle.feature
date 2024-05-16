@unit @candidate
Feature: Candidate handler
    Scenario Outline: RA pattern matching
        Given input value <value> is provided
        When value is pattern matched against the ra regex
        Then pattern matching should return <expected>

        Examples:
        | value       | expected |
        | 3:31:46.23  | True     |
        | 5:00:57.54  | True     |
        | 5000057054  | None     |
        | a:00:57.54  | None     |
        | 5?00:57.54  | None     |
        | 5:a0:57.54  | None     |
        | 5:00:57.aa  | None     |
        | 5:00:57:54  | None     |
        | 5.00.57.54  | None     |
        | abcdefghij  | None     |
        | £%?a"2l;2'  | None     |
        | a:cd:fg.ij  | None     |
        | -27:49:16.8 | None     |
        | -25:55:03.5 | None     |

    Scenario Outline: Dec pattern matching
        Given input value <value> is provided
        When value is pattern matched against the dec regex
        Then pattern matching should return <expected>

        Examples:
        | value       | expected |
        | -27:49:16.8 | True     |
        | -25:55:03.5 | True     |
        | ?25:55:03.5 | None     |
        | 5000057054  | None     |
        | a:00:57.54  | None     |
        | 5?00:57.54  | None     |
        | 5:a0:57.54  | None     |
        | 5:00:57.aa  | None     |
        | 5:00:57:54  | None     |
        | 5.00.57.54  | None     |
        | abcdefghij  | None     |
        | £%?a"2l;2'  | None     |
        | a:cd:fg.ij  | None     |
        | 3:31:46.23  | None     |
        | 5:00:57.54  | None     |
