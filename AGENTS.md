# Reviewing changes to the Allure sample

## General review

Check the diff against the example a reader can run from README.md. If a command
or output location changed, check its documented invocation too.

## Test cases

Check that each changed Allure title describes the scenario the test exercises.
For API tests, check that the request and assertions agree on the expected result.

## Shared steps

Read the callers of each changed step. Check that its arguments and return value
still fit those calls and that its Allure label describes the action.

## Fixtures and reporting

Check setup and teardown together. Verify that the Petstore coverage reporter
still generates its report after the session and that the configured Allure
results directory agrees with the upload script.
