Title: Universal tox tests (from just about any CI)
Date: 2021-10-17
Tags: CI, Python, GitLab, GitHub, Zuul
Slug: universal-tox-tests
Summary: I like tox. A lot. I use it all the time. This is a quick summary on how to use it in such a way that it becomes a central anchor point that you can use from all your CI systems.

I like `tox`. A lot. I use it all the time. This is a quick summary on
how to use it in such a way that it becomes a central anchor point that
you can use from all your CI systems.

## What’s tox for?

Normally `tox` is used to run tests for Python projects, and it’s very
well suited for that. You can use it with Python libraries, Django
projects, scripts you use for system automation, whatever. But you can
use it just the same for code that isn’t a Python application or
library itself, but a Python application just happens to come in handy
for testing that code.

In this example, I’ll describe a super simple use case: using a
barebones `tox` configuration that lints YAML configurations. Suppose
you’ve got a Git repo that’s full of YAML files. And you want to make
sure, for example, that all your
[truthy](https://yamllint.readthedocs.io/en/stable/rules.html#module-yamllint.rules.truthy)
values are `true` or `false` and never `yes`, `no`, `on` or `off`. Or
that your
[indentation](https://yamllint.readthedocs.io/en/stable/rules.html#module-yamllint.rules.indentation)
is always consistent.

## `tox.ini`

There first thing you’ll do is create `tox.ini`, the central tox
configuration file, in the top level directory of your
repository. Here’s a tiny example:

```ini
[tox]
envlist = py{3,36,39}
skipsdist = True

[testenv]
deps = yamllint
commands = yamllint {toxinidir}
```

That’s it. What this’ll do, when invoked as simply `tox`, is

* create a Python 3 venv,
* `pip`-install the latest version of
  [`yamllint`](https://yamllint.readthedocs.io/en/stable/),
* invoke the `yamllint` command, which will recursively check for all
  `.yml`, `.yaml`, and `.yamllint` files in the directory where the
  `tox.ini` file itself lives.

What's helpful here is that `tox` does a little bit of magic with the
testenv names. tox
[knows](https://tox.wiki/en/latest/example/basic.html#a-simple-tox-ini-default-environments)
that if you call a testenv `py36`, you want to test with Python 3.6
(more precisely, [CPython](https://en.wikipedia.org/wiki/CPython)
3.6). `py39`, that's Python 3.9. Just `py3` means whatever Python
version maps to the `python3` binary on your system.[^python-versions] 

[^python-versions]: Testing with multiple Python versions may seem
    less than useful when you’re dealing with just one upstream
    package, `yamllint`. I use that here as an oversimplified
    example. As soon as you add your own Python scripts or modules to
    the `tox` checks, you may very well be interested in multiple
    python versions.

## Running `tox` on every commit

Now the first thing you might want to do is run `tox` on every commit,
and encourage your collaborators to do the same. You can easily do
that by dropping this tiny shell script[^shell-script] into your repo
as a file named `pre-commit` in the `.githooks` directory:

[^shell-script]: If you're being a purist, you could also invoke the
    tox runner from a Python script. I prefer the shell `exec`
    one-liner.


```bash
#!/bin/sh

exec tox -e py3
```

Add that file to your repository as `.githooks/pre-commit`, and make
it executable. Also, add a little note to your README explaining that,
to enable the pre-commit hook, all your collaborators can simply run

```bash
git config core.hooksPath .githooks
```

Easy, right? And once you’ve run that command, every `git commit` will
kick off a `tox` run and you’ll never commit borked YAML again.[^py3]

[^py3]: In this case, for testing locally, we're not going to care
    about a specific installed Python version. We'll just make sure
    that the commit doesn't obviously break anything. In my humble
    opinion it's OK to catch version-specific issues in CI, but we
    shouldn't feed the CI code that's outright broken.

Now of course, using those hooks is entirely optional, and can be
overridden with `--no-verify`. So, for those slackers that can’t be
bothered to use them, you also want to check centrally. Here’s where
your CI comes in.

## Running `tox` on every GitHub PR

If you collaborate via GitHub, you can run `tox` on every PR, with a
simple [GitHub Actions](https://docs.github.com/en/actions)
workflow. To use it, you’ll need a small addition to your `tox.ini`
file:

```ini
[tox]
envlist: py{3,36,39}
skipsdist = True

[gh-actions]
python =
    3.6: py36
    3.9: py39

[testenv]
deps = yamllint
commands = yamllint {toxinidir}
```

And then, you add a workflow to `.github/workflows`, say
`.github/workflows/tox.yml`:

```yaml
---
name: Test with tox
'on':
  - push
  - pull_request
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version:
          - 3.6
          - 3.9
    steps:
      - name: Checkout
        uses: actions/checkout@v2
        with:
          submodules: true
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install tox tox-gh-actions
      - name: Test with tox
        run: tox
```

So that sets up your workflow so that it tests with two different
Python versions that you care about, and then runs a test with each of
them.

It does this via a combination of the information contained in the
`[gh-actions]` section of `tox.ini`, and the `matrix` strategy defined
in the workflow. The `tox-gh-action` plugin then pulls that
information together and sets up testenvs as needed.

And it runs these checks every time you push to a branch (topic branch
or default branch), and also on every pull request.

## Running `tox` from GitLab CI

So you’re either using only GitLab and not GitHub, or you’re mirroring
a GitHub repo to a self-hosted GitLab and want to run your pipelines
there as well? Easy. Here’s the exact same functionality for your
`.gitlab-ci.yml` file:[^docker-runners]

[^docker-runners]: This example assumes that you’re either using
    shared GitLab runners using Docker, or a self-hosted runner on
    Kubernetes.

```yaml
---
py36:
  image: python:3.6
  stage: build
  script:
    - pip install tox
    - tox -e py36

py39:
  image: python:3.9
  stage: build
  script:
    - pip install tox
    - tox -e py39
```

In [GitLab CI](https://docs.gitlab.com/ee/ci/) I know of no elegant
`matrix` syntax to map the image version to the testenv. But on the
other hand there's a bunch of things that "just happen" in a GitLab CI
pipeline, which you specifically need to define in a GitHub Actions
workflow definition. So overall your `.gitlab-ci.yml` ends up shorter
than your GitHub Actions `tox.yml`.

## Running `tox` from Zuul

If you’re running a `tox` testenv from [Zuul](https://zuul-ci.org/),
you would use the built-in tox jobs in your pipeline, as referenced in
`.zuul.yaml`:

```yaml
---
- project:
    check:
      jobs:
        - tox-py36
        - tox-py39
    gate:
      jobs:
        - tox-py36
        - tox-py39
```

Here, the `tox-py36` and `tox-py39` environments are both derivatives
of the base
[tox](https://zuul-ci.org/docs/zuul-jobs/python-jobs.html#job-tox)
job, which will run with cPython versions 3.6 and 3.9, and by default
invoke testenvs called `py36` and `py39`, respectively.

## And now?

Now that all of your Python testing standardizes on tox, you can go to
town. Add more tests, add more testenvs, more Python versions,
whatever.

You might need to make minimal changes, like add one line for each new
Python version you want to support, to all your CI definitions. But if
your project moves from GitHub to GitLab or from GitLab to
Gerrit/Zuul, or your entire company goes on a great big CI migration,
then you'll have one less thing to worry about, because your tests
already run anywhere.

> **By the way:** when you set up your `tox.ini` and your CI
> configuration files as shown in this article, then `yamllint` *will*
> of course also lint your YAML CI configuration files
> themselves. Which comes in handy; I found 4 yamllint warnings and
> one error while testing the examples I’ve given here.
