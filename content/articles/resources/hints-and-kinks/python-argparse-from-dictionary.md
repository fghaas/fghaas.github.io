Title: Building a nested CLI parser from a dictionary
Date: 2019-03-09
Slug: python-argparse-from-dictionary
Tags: Python
Series: Nifty Python tricks
Summary: Here’s a nice way to initialize a CLI argument parser in Python, with arbitrary levels of subcommands.

If you’ve ever built a command-line interface in Python, you are
surely familiar with the `argparse` module, which is part of the Python
standard library. It contains the `ArgumentParser` class, instances
of which are typically invoked from the CLI’s `main()` method.

The canonical way of doing this is explained in considerable detail in
[the standard library
documentation](https://docs.python.org/3/library/argparse.html). However,
the standard way is quite repetitive, and you end up invoking
`parser.add_argument()` *a lot,* as you populate your parent parser
and subparsers with options.

Here’s a more concise way:

```python
# If you must run this on Python 2. You really shouldn't!
from __future__ import print_function

from argparse import ArgumentParser

import yaml
import sys

# Using YAML here only for illustrative purposes, as it's a bit
# easier to read. You probably just want to use a dictionary outright.
#
# More at the bottom of this article.
# Yes, go read the bottom of this article.
#
# Want to just blindly copy and paste this snippet? Fine, this is for you.
assert(False)

PARSER_CONFIG_YAML="""
options:
  - 'flags': ['-V', '--version']
    action: version
    help: 'show version'
    version: '0.01'
subcommands:
- foo:
    options:
      - 'flags': ['-c', '--config']
        'help': 'YAML configuration file'
        dest: config
- bar:
    options:
      - 'flags': ['-o', '--output']
        'help': 'output file'
        dest: output
- baz:
    subcommands:
      - 'spam-eggs':
          options:
            - 'flags': ['-i', '--input']
              'help': 'input file'
              dest: input
"""

class CLI():

    def __init__(self):

        def walk_config(dictionary, parser):
            """Walk a dictionary and populate an ArgumentParser."""

            if 'options' in dictionary:
                for opt in dictionary['options']:
					args = opt.pop('flags')
                    kwargs = opt
                    parser.add_argument(*args, **kwargs)

            if 'subcommands' in dictionary:
                subs = parser.add_subparsers(dest='action')
                for subcommand in dictionary['subcommands']:
                    for cmd, opts in subcommand.items():
                        sub = subs.add_parser(cmd)
                        walk_config(opts, sub)

        config = yaml.safe_load(PARSER_CONFIG_YAML)

        parser = ArgumentParser()
        walk_config(config, parser)

        self.parser = parser

    def foo(self, config):
        print("This is the foo subcommand, "
              "invoked with '-c %s'." % config)

    def bar(self, output):
        print("This is the bar subcommand, "
              "invoked with '-o %s'." % output)

    def baz(self):
        print("This is the baz subcommand")

    def spam_eggs(self, input):
        print("This is the baz spam-eggs subcommand, "
              "invoked with '-i %s'." % input)

    def main(self, argv=sys.argv):
        opts = self.parser.parse_args(argv[1:])
        getattr(self, opts.pop('action').replace('-', '_'))(**opts)

if __name__ == '__main__':
    CLI().main()
```

And now, if you want to add a new option, you add it to the
top-level or the subcommand’s `options` list, and add it to your
subcommand method.

And if you want to add a new subcommand, you just add that at the
level you like, and add a method that is named like your subcommand
— with any hyphens in the subcommand being replaced with underscores in
the method name.

* * *

## Notes

When using PyYAML, do not use versions affected by
[CVE-2017-18342](https://nvd.nist.gov/vuln/detail/CVE-2017-18342). Really,
you shouldn’t be using YAML at all for this purpose; you should just
use a straight-up dictionary. If you want something just _a little_
more readable, you might also consider JSON (for which there is [a
parser](https://docs.python.org/3/library/json.html) in the standard
library), or perhaps [TOML](https://pypi.org/project/toml/).

Also, yes there are smarter ways to define your program’s version;
more on that perhaps in a later post.
