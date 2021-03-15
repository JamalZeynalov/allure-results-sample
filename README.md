## Set of tests used as examples for "Allure Docker Service UI"

Clone this GitHub project:
```shell
> git clone git@github.com:JamalZeynalov/allure-results-sample.git
```
<hr>

### Run tests locally:
```shell
> pip install -r requirements.txt
> pytest
```
Note: "alluredir" cmd option is already set in pytest.ini
<hr>

### Run tests in the docker container:
Build an image and run tests in the docker container:
```shell
> docker build -t test-image .
> sh dockerized_tests.sh test-image
```
or use pre-built image from the dockerhub:
```shell
> sh dockerized_tests.sh jamalzeinalov/test-image
```
Note: Use git bash to run shell scripts on Windows 
<hr>

### Send results:
If your "Allure Docker Service UI" is currently running on your host machine then you can run send_allure_results.py
```shell
> python send_allure_results.py
```
This script sends all files from "target/allure-results" dir to "Allure Docker Service".

---
For more information about "Allure Docker Service UI" check 
https://hub.docker.com/repository/docker/jamalzeinalov/allure_docker_service_ui
