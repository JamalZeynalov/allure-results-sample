import allure

from steps.common_steps import step_1, step_2, verify_test_results


@allure.feature('Advanced Feature')
@allure.story('Story #1')
@allure.title('Advanced web application feature is working correctly in Google Chrome')
@allure.description("""
    feature('Advanced Feature')
    story('Story #1')
    title('Advanced web application feature is working correctly in Google Chrome')
""")
def test_advanced_feature_1():
    step_1()
    step_2()
    verify_test_results()


@allure.feature('Advanced Feature')
@allure.story('Story #1')
@allure.title('Advanced web application feature is working correctly in Google Firefox')
@allure.description("""
    feature('Advanced Feature')
    story('Story #1')
    title('Advanced web application feature is working correctly in Google Firefox')
""")
def test_advanced_feature2():
    step_1()
    step_2()
    verify_test_results()


@allure.feature('Advanced Feature')
@allure.story('Story #2')
@allure.title('Advanced mobile application feature is working correctly with Wi-Fi connection')
@allure.description("""
    feature('Advanced Feature')
    story('Story #2')
    title('Advanced mobile application feature is working correctly with Wi-Fi connection')
""")
def test_advanced_feature3():
    step_1()
    step_2()
    verify_test_results()


@allure.feature('Advanced Feature')
@allure.story('Story #2')
@allure.title('Advanced mobile application feature is working correctly with LTE connection')
@allure.description("""
    feature('Advanced Feature')
    story('Story #2')
    title('Advanced mobile application feature is working correctly with LTE connection')
""")
def test_advanced_feature4():
    step_1()
    step_2()
    verify_test_results()
