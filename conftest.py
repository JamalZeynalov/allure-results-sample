import random

import pytest
from dotenv import load_dotenv
from swagger_coverage_py.reporter import CoverageReporter

load_dotenv(".env")


@pytest.fixture
def random_int_fixture():
    return random.randint(0, 999999)


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="petstore", host="https://petstore.swagger.io")
    reporter.cleanup_input_files()
    reporter.setup("/v2/swagger.yaml")

    yield
    reporter.generate_report()
