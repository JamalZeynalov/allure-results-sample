import allure

from steps.common_steps import step_1, step_2, verify_test_results


@allure.feature('Settings Feature')
@allure.story('Global Settings')
@allure.title('Admin settings are successfully updated by the admin')
@allure.description("""
    feature('Settings Feature')
    story('Global Settings')
    title('Admin settings are successfully updated by the admin')
""")
def test_admin_settings_1():
    step_1()
    step_2()
    verify_test_results()


@allure.feature('Settings Feature')
@allure.story('Global Settings')
@allure.title('Admin settings cannot be updated by a user')
@allure.description("""
    feature('Settings Feature')
    story('Global Settings')
    title('Admin settings cannot be updated by a user')
""")
def test_admin_settings_2():
    step_1()
    step_2()
    verify_test_results()


@allure.feature('Settings Feature')
@allure.story('User Settings')
@allure.title('User Settings are successfully updated by the admin')
@allure.description("""
    feature('Settings Feature')
    story('User Settings')
    title('User settings are successfully updated by the admin')
""")
def test_user_settings_1():
    step_1()
    step_2()
    verify_test_results()


@allure.feature('Settings Feature')
@allure.story('User Settings')
@allure.title('User settings are successfully updated by the user')
@allure.description("""

""")
def test_user_settings_2():
    step_1()
    step_2()
    verify_test_results()
