## Set of tests used as examples for "Allure Docker Service UI"

### Verify Rules Stop

[Read the hook](.agents/hooks/verify_rules_stop.py) · [Review rules](AGENTS.md)

When Claude Code or Cursor edits files in this sample, a project hook records
the paths for that conversation. At stop it requests one review of the actual
changes against the relevant rules. For example, editing
`steps/common_steps.py` selects the shared-step checks, including whether
existing callers still match the changed signature.

The hook uses Python 3 and its standard library. Open the repository in a
client with project hooks enabled and ask it to edit a test or a step. The
review prompt appears when the agent tries to finish. Read-only turns produce
no prompt. Shell-only edits are outside the edit events this hook observes.
The agent performs the review; the hook does not certify that tests passed.

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
The Doclerfile used here is created for "arm64" version of JDK 11.<br>
So, you have to change the path in the JAVA_HOME environment variable if you use another version.
<br>

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
