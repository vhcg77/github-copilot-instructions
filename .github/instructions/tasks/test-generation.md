---
applyTo: ["test", "generation", "pytest"]
description: "Instructions for generating tests"
priority: "high"
---

# Task: Test Generation with Pytest

Your task is to generate unit tests for a given Python function or class using the `pytest` framework.

## Pre-Test Generation Research Phase

Before generating tests, leverage MCP tools for comprehensive testing strategies:

1. **Context7 Research**: Use `"use context7"` for current pytest and testing framework documentation
   * Example: `"pytest fixtures and parametrization patterns, use context7"`
   * Get latest testing patterns and assertion techniques

2. **Existing Test Analysis**: Use Consult7 to analyze current test coverage and patterns
   * Review `/tests/` directory for established testing conventions
   * Identify gaps in test coverage across the codebase
   * Understand existing fixture patterns and test organization

3. **Testing Best Practices**: Use DuckDuckGo for current testing methodologies
   * Search for latest testing strategies specific to your domain
   * Example: "Python data validation testing patterns 2025"

4. **Reference Test Suites**: Use GitHub tools to study comprehensive test implementations
   * Find examples of thorough test suites in similar projects
   * Analyze testing patterns for data science and API projects

## Test Generation Rules

## Rules
1.  **File Naming**: Test files must be named `test_*.py`.
2.  **Test Function Naming**: Test functions must be named `test_*`. The name should be descriptive of what it is testing.
3.  **Arrange-Act-Assert Pattern**: Structure your tests clearly:
    - **Arrange**: Set up the test data and preconditions.
    - **Act**: Call the function or method being tested.
    - **Assert**: Check that the outcome is as expected.
4.  **Test Edge Cases**: Go beyond the "happy path." Test for:
    - Empty inputs (e.g., empty lists, empty DataFrames).
    - Invalid inputs (e.g., wrong data types).
    - Zeroes, negative numbers.
    - Any other boundary conditions.
5.  **Test for Exceptions**: Use `pytest.raises` to verify that the code raises the correct exception when it should.
    ```python
    import pytest

    def my_function(x):
        if x == 0:
            raise ValueError("Input cannot be zero")
        return 1 / x

    def test_my_function_raises_error_on_zero_input():
        # Arrange
        invalid_input = 0
        # Act & Assert
        with pytest.raises(ValueError, match="Input cannot be zero"):
            my_function(invalid_input)
    ```
6.  **Use Fixtures**: For complex setup logic or data that is reused across multiple tests, use `@pytest.fixture`.
