import allure


@allure.step('Step one')
def step_1():
    pass


@allure.step('Step two')
def step_2():
    pass


@allure.step('Multiply by 2')
def multiply_by_2(number: int):
    return number * 2


@allure.step('Verify test result')
def verify_test_results(*args):
    print([x for x in args])
    assert True
