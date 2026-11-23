## Set of tests used as examples for "Allure Docker Service UI"

### Verify Rules Stop

This hook brings the project's review rules into an AI coding session at the
point when the agent is about to finish. It records the files edited through
Claude Code or Cursor and asks the agent to check its changes against the
matching sections of [AGENTS.md](AGENTS.md).

For example, an edit to [a shared test step](steps/common_steps.py) triggers
two checks. Do the callers still match the step's signature? Does its Allure
label still describe the action? The agent inspects the changes, fixes any
issues it finds, and reports what it checked.

**Try it.** With Python 3 on your PATH and project hooks enabled, open this
repository in Claude Code or Cursor. Ask the agent to edit an Allure step
label in `steps/common_steps.py` using its file editor. When it tries to
finish, look for the follow-up pointing to **Shared steps**.

The hook tracks editor events per conversation in a local SQLite database.
Read-only turns and shell-only edits produce no review prompt. A loop guard
limits the review to one follow-up. The agent is responsible for checking the
diff and running any relevant tests.

[Hook implementation](.agents/hooks/verify_rules_stop.py) ·
[Claude Code configuration](.claude/settings.json) ·
[Cursor configuration](.cursor/hooks.json)

Run the hook's regression tests with the Python standard library:

```sh
python3 -m unittest discover -s .agents/hooks/tests
```

### Set up the sample

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
