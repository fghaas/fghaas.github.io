Title: Python package dependency checking in a CI pipeline with pipdeptree
Date: 2022-06-26 20:00
Slug: pipdeptree-ci
Tags: Python, CI
Summary: Sometimes pip behaves rather oddly when it comes to package dependency resolution. Here’s one way to catch such issues in your CI pipeline.

Recently at work we ran into rather strange-looking errors that broke
some functionality we depend on.

In an application run from a CI-built container image, we were seeing
`pkg_resources.ContextualVersionConflict` errors indicating that one of
our packages could not find a matching installed version of `protobuf`.
Specifically, that package wanted `protobuf<4` installed, but the
installed version of the `protobuf` package was 4.21.1.

This was somewhat puzzling: all Python packages in the image were
installed with `pip`, and the packages’ requirements ought to have been
in good shape.

We found another dependency that did specify `protobuf<5`, but taken
together `pip` should surely resolve that into a 3.x version of
`protobuf`, in order to satisfy both the `protobuf<4` requirement from
one package, and the `protobuf<5` one from another?

To visualize and test such dependencies, the `pipdeptree` utility comes
in quite handy.

So, I hacked up a couple of minimal `tox` testenvs:

```ini
[testenv:pipdeptree]
deps =
    pipdeptree
commands = pipdeptree -w fail

[testenv:pipdeptree-requirements]
deps =
    -rrequirements.txt
    pipdeptree
commands = pipdeptree -w fail
```

The first one, `pipdeptree`, merely installs the package being built,
obeying the `install_requires` list in its `setup.py` file. This is the
“minimal” installation.

The second one, `pipdeptree-requirements`, runs a full installation,
pulling in everything needed from the `requirements.txt` file.

`pipdeptree` generates warnings on potential version conflicts between
dependent packages. So, in both testenvs, we run `pipdeptree` in
`-w fail` mode, which turns all warnings into errors that fail the
testenv.

So now, [having added tox to both our CI and our local Git
hooks](%7Bfilename%7Duniversal-tox-tests.md), we can run these checks
locally and from GitHub Actions, and they should both fail and thereby
expose our package dependency bug, right?

Well, here is where it got weird.

Because if I ran that locally, on my Ubuntu Focal development laptop, I
got:

``` 
        - protobuf [required: >=3.15.0,<4.0.0dev, installed: 4.21.1]
      - protobuf [required: >=3.15.0,<5.0.0dev, installed: 4.21.1]
```

This is “bad” in the sense that it’s the wrong `protobuf` version, but
good in that it exposes the bug that we’re trying to fix. Progress\!

However, running the same thing from our GitHub Actions workflow,
there’s this:

``` 
          - protobuf [required: >=3.15.0,<4.0.0dev, installed: 3.20.1]
        - protobuf [required: >=3.15.0,<5.0.0dev, installed: 3.20.1]
```

So here, in GitHub Actions, we see a `protobuf` version being installed
that *doesn’t* break anything, but it also means that our test doesn’t
expose our bug, which is a problem\!

I’ll spare you the details of finding this out, but it turned out that
this is actually a `pip` problem. `pip` 20.0.2 (which is the version you
get when you run `apt install python3-pip` on Ubuntu Focal) has the
dependency resolution error, which results in a `protobuf` package that
is “too new”. If you install with `pip` version 21 or later, you get a
`protobuf` that is “old enough” to make all installed packages happy.

So, how do we test *that?*

There is a package called
[`tox-pip-version`](https://pypi.org/project/tox-pip-version/) that
comes in very handy here, in that it allows you to set an environment
variable, `TOX_PIP_VERSION`, instructing `tox` what `pip` version it
should use in order to install packages into testenvs.

This you can use from a GitHub Actions `jobs` definition, making use of
a `matrix` strategy:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version:
          - 3.8
          - 3.9
        pip-version:
          - 20.0.2
          - 22.0.4

    steps:
    - name: Check out code
      uses: actions/checkout@v1
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install tox tox-gh-actions tox-pip-version
    - env:
        TOX_PIP_VERSION: ${{ matrix.pip-version }}
      name: Test with tox (pip ${{ matrix.pip-version }})
      run: tox
```

What this does is it sets up a 2×2 matrix: run with Python 3.8 and
Python 3.9, and for both those Python versions run with `pip` 20.0.2 and
22.0.4 (these happen to be the two versions that we’re interested in).

That way, we were able to expose the package dependency bug, and then
fix it. The test now serves as a regression test, to make sure we don’t
run into a similar issue again.

If you’re curious, the full PR discussion with additional context is [on
GitHub](https://github.com/hastexo/hastexo-xblock/pull/216).
