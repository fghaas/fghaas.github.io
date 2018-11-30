Title: Using coverage with multiple parallel GitLab CI jobs
Date: 2019-03-10
Slug: coverage-gitlab-ci
Tags: Python, CI, GitLab
Summary: If you ever write unit tests in Python, you are probably familiar with Ned Batchelder’s `coverage` tool. This article explains how you can use `coverage` in combination with `tox` and a GitLab CI pipeline, for coverage reports in your Python code.

If you ever write unit tests in Python, you are probably familiar with
[Ned Batchelder](https://twitter.com/nedbat)’s [`coverage`
tool](https://coverage.readthedocs.io). This article explains how you
can use `coverage` in combination with `tox` and a GitLab CI pipeline,
for coverage reports in your Python code.

## Running `coverage` from `tox`

Consider the following rather run-of-the mill `tox` configuration
(nothing very spectacular here):

```ini
[tox]
envlist = py{27,35,36,37},flake8

[coverage:run]
parallel = True
include =
  bin/*
  my_package/*.py
  tests/*.py

[testenv]
commands =
    coverage run -m unittest discover tests {posargs}
deps =
    -rrequirements/setup.txt
    -rrequirements/test.txt

[testenv:flake8]
deps = -rrequirements/flake8.txt
commands = flake8 {posargs}
```

In this configuration, `coverage run` [(which, remember, replaces
`python`)](https://coverage.readthedocs.io/en/latest/cmd.html#execution)
invokes [test
auto-discovery](https://docs.python.org/3/library/unittest.html#test-discovery)
from the `unittest` module. It looks for unit tests in the `tests`
subdirectory, runs them, and keeps track of which lines were hit and
missed by your unit tests.

The only slightly unusual bit is `parallel = True` in the
`[coverage:run]` section. This instructs `coverage` to write its
results not into one file, `.coverage`, but into multiple, named
`.coverage.<hostname>.<pid>.<randomnumber>` — meaning you get separate
results files for each `coverage` run.

Subsequently, you can combine your coverage data with `coverage
combine`, and then do whatever you like with the combined data
(`coverage report`, `coverage html`, etc.).

## GitLab CI

Now there’s a bit of a difficulty with GitLab CI, which is that your
individual `tox` `testenv`s will all run in completely different
container instances. That means that you’ll run your `py27` tests in
one container, `py35` in another, and so forth. But you can use GitLab
CI [job
artifacts](https://docs.gitlab.com/ee/user/project/pipelines/job_artifacts.html)
to pass your coverage data between one stage and another.

Here’s your `build` stage, which stores your `coverage` data in
short-lived artifacts:

```yaml
image: python

py27:
  image: 'python:2.7'
  stage: build
  script:
    - pip install tox
    - tox -e py27,flake8
  artifacts:
    paths:
      - .coverage*
    expire_in: 5 minutes

py35:
  image: 'python:3.5'
  stage: build
  script:
    - pip install tox
    - tox -e py35,flake8
  artifacts:
    paths:
      - .coverage*
    expire_in: 5 minutes

py36:
  image: 'python:3.6'
  stage: build
  script:
    - pip install tox
    - tox -e py36,flake8
  artifacts:
    paths:
      - .coverage*
    expire_in: 5 minutes

py37:
  image: 'python:3.7'
  stage: build
  script:
    - pip install tox
    - tox -e py37,flake8
  artifacts:
    paths:
      - .coverage*
    expire_in: 5 minutes
```

And here’s the `test` stage, with a single job that

* combines your coverage data,
* runs `coverage report` and parses the output — this is what goes into
  the _coverage_ column of your GitLab job report,
* runs `coverage html` and stores the resulting `htmlcov` directory
  into an artifact that you can download from GitLab for a week.

```yaml
coverage:
  stage: test
  script:
    - pip install coverage
    - python -m coverage combine
    - python -m coverage html
    - python -m coverage report
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    paths:
      - htmlcov
    expire_in: 1 week
```
