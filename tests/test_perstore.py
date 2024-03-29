import allure
from requests import Response
from swagger_coverage_py.listener import CoverageListener


@allure.feature('Swagger Coverage')
@allure.story('Swagger Coverage #1')
@allure.title('Swagger Coverage test #1')
def test_response():
    response: Response = CoverageListener(
        method="get",
        base_url="https://petstore.swagger.io",
        raw_path="/pet/{petId}",
        uri_params={"petId": 1},
    ).response
    assert response.status_code


@allure.title("Test title")
def test_response_2():
    with allure.step("Step 1"):
        print(1)
        with allure.step("Step 1.1"):
            print(1)

    with allure.step("Step 2"):
        print(1)
