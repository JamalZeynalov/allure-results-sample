## Set of tests used as examples for "Allure Docker Service UI"

#### To generate test results follow steps below:
* Clone this GitHub project:
```
git clone git@github.com:JamalZeynalov/allure-results-sample.git
```
* Install requirements:
```
pip install -r requirements.txt
```
* Run tests using pytest

Note: "alluredir" cmd option is already set in pytest.ini
```
pytest
```
* If your "Allure Docker Service UI" is currently running on your host machine then you can run send_allure_results.py
```
python send_allure_results.py
```
This script sends all files from "target/allure-results" dir to "Allure Docker Service".

---
For more information about "Allure Docker Service UI" check 
https://hub.docker.com/repository/docker/jamalzeinalov/allure_docker_service_ui
