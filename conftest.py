import random

import pytest


@pytest.fixture
def random_int_fixture():
    return random.randint(0, 999999)
