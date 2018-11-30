Title: Configuring CLI output verbosity with logging and argparse
Date: 2019-05-01
Slug: python-cli-logging-options
Tags: Python
Series: Nifty Python tricks
Summary: Command-line interfaces frequently produce output whose verbosity your users may want to be able to tweak. Here’s a nifty way to do that.

In a Python command-line interface (CLI) utility, you will want to
inform your users about what your program is doing. Your will also
want to give your users the ability to tweak how verbose that output
is. Now there is a de-facto standard convention for doing that, which
most CLIs — Python or otherwise — tend to adhere to:

* By default, show messages only about errors and warning conditions.
* Define a `-v` or `--verbose` option that makes your program also
  show messages that are merely informative in nature.
* Optionally, allow users to repeat the `-v` option, making the
  program even more verbose (to include, for example, debug output).
* Conversely, also define a `-q` or `--quiet` (alternatively
  `-s`/`--silent`) option that, when set, makes the program suppress
  warnings and show only errors — i.e. the stuff that your program
  shows if it exits with a nonzero exit code.
* Log output that tells users about what the program is doing, as it
  goes along, to the standard error (stderr) stream, whereas the
  output related to the program’s *results* goes to standard output
  (stdout). This gives your users the ability to pipe stdout to a file
  or another program, and your progress or status messages won’t
  interfere with that.

And in Python it’s not at all difficult to do that!

## `argparse` options

First, we’ll want to define a couple of options [for our
`argparse.ArgumentParser`
object](https://docs.python.org/3/library/argparse.html), which in the
following snippet I’ve named `parser`. Define two options, like so:[^1]

```python
parser.add_argument('-v', '--verbose',
                    action='count',
                    dest='verbosity',
                    default=0,
                    help="verbose output (repeat for increased verbosity)")
parser.add_argument('-q', '--quiet',
                    action='store_const',
                    const=-1,
                    default=0,
                    dest='verbosity',
                    help="quiet output (show errors only)")
```

From this, we get two command-line options:

* `-v` or `--verbose`, which can be repeated, sets `verbosity`, which
  defaults to 0. `action='count'` means that if you invoke your CLI
  with `-v`, `verbosity` is 1, `-vv` sets `verbosity` to 2, etc.

* `-q` or `--quiet` *also* sets `verbosity`, but to a constant value,
  -1, via `store_const`.

## Setting up the `logging` subsystem

What we’ll want to do is use [the `logging`
subsystem](https://docs.python.org/3/library/logging.html) to send our
status, progress, and error messages to stderr.

First, you can translate `verbosity` into a logging level understood
by the `logging` module. Here’s a little convenience method that
achieves that:

```python
def setup_logging(verbosity):
    base_loglevel = 30
    verbosity = min(verbosity, 2)
    loglevel = base_loglevel - (verbosity * 10)
    logging.basicConfig(level=loglevel,
                        format='%(message)s')
```

Now what does this do? Python log levels go from 10 (`logging.DEBUG`)
to 50 (`logging.CRITICAL`) in intervals of 10; our `verbosity`
argument goes from -1 (`-q`) to 2 (`-vv`).[^2] We never want to
suppress error and critical messages, and default to 30
(`logging.WARNING`). So we multiply `verbosity` by 10, and subtract
that from our base loglevel of 30.

With `-v`, that sets our effective log level to 20 (`logging.INFO`);
with `-vv`, to 10 (`logging.DEBUG`). And with `-q`
(i.e. `verbosity==-1`), our log level becomes 40 (`logging.ERROR`).

Now we can use `logging.basicConfig()` to configure the logging
subsystem to send unadorned log messages with the desired loglevel or
above, to stderr: `basicConfig()`, [by
default](https://docs.python.org/3/library/logging.html#logging.basicConfig),
sets up a `StreamHandler` whose output stream is `sys.stderr`, so it
already does what we want here. And setting `format='%(message)s'`
strips the `LEVEL:logger:` prefix that `basicConfig()` would otherwise
include in the log line (and which is helpful for log files, but not
so much for CLI output).

From then on, every time your program should write an informational
message to stderr, you just use `logging.info()`, for a debug message,
`logging.debug()`, and so on.

## Adding an environment variable

In some circumstances you might *always* want debug output, and
invoking your CLI with `-vv` all the time might not be practical. (CI
systems are an example — you generally want your build logs as verbose
as possible.) You can make your users’ lives easier by optionally
fixing up your logging subsystem with an environment variable, like so:

```python
def setup_logging(verbosity):
    base_loglevel = int(os.getenv('LOGLEVEL', 30)) 
    verbosity = min(verbosity, 2)
    loglevel = base_loglevel - (verbosity * 10)
    logging.basicConfig(level=loglevel,
                        format='%(message)s')
```

This way, if you invoke your CLI with `LOGLEVEL=10` in its
environment, it will always use debug output. 

Perhaps you’d like to make this even easier, allowing your users to
also set `LOGLEVEL` to `debug`, `INFO`, `erRoR` and whatever
else. That you could do like this:[^3]

```python
def setup_logging(verbosity):
    base_loglevel = gettattr(logging, 
                             (os.getenv('LOGLEVEL', 'WARNING')).upper()) 
    verbosity = min(verbosity, 2)
    loglevel = base_loglevel - (verbosity * 10)
    logging.basicConfig(level=loglevel,
                        format='%(message)s')
```

## Parting thought

One of the many ways in which using `logging` comes in handy in a CLI
is in a catch-all exception handler:

```python
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(str(e))
        logging.debug('', exc_info=True)
        try:
            sys.exit(e.errno)
        except AttributeError:
            sys.exit(1)

```

This way, unhandled exceptions will show merely the exception message
by default, but if and only if debug logging is enabled, your users
will also see a stack trace.

[^1]: This is used
    [here](https://github.com/hastexo/olx-utils/blob/v0.3.0/olxutils/cli.py#L53).

[^2]: There is, to the best of my knowledge, no way to limit the
    number of repeats for an argument with `action='count'`. Hence the
    construct with the `min()` built-in function.

[^3]: A variation of this is used
    [here](https://github.com/hastexo/olx-utils/blob/v0.3.0/olxutils/cli.py#L284).
