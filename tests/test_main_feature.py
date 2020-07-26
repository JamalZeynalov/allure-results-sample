import allure

from steps.common_steps import step_1, step_2, multiply_by_2, verify_test_results


@allure.feature('Main Feature')
@allure.story('Story #1')
@allure.title('Main web application feature is working correctly in Google Chrome')
@allure.description("""
    feature('Main Feature')
    story('Story #1')
    title('Main web application feature is working correctly in Google Chrome')
""")
def test_main_feature1(random_int_fixture):
    step_1()
    step_2()
    number: int = multiply_by_2(random_int_fixture)
    verify_test_results(number)


@allure.feature('Main Feature')
@allure.story('Story #1')
@allure.title('Main web application feature is working correctly in Firefox')
@allure.description("""
    feature('Main Feature')
    story('Story #1')
    title('Main web application feature is working correctly in Firefox')
""")
def test_main_feature2():
    step_1()
    step_2()
    verify_test_results()
