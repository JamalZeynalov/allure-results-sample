import random

import pytest
from swagger_coverage_py.reporter import CoverageReporter


@pytest.fixture
def random_int_fixture():
    return random.randint(0, 999999)


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="petstore", host="https://petstore.swagger.io")
    reporter.cleanup_input_files()
    reporter.setup("/v2/swagger.json")

    yield
    reporter.generate_report()
