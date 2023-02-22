Title: Launching a brand-new documentation platform in 2023
Date: 2023-03-23 10:30
Slug: mkdocs
Summary: At work, my team and I built and launched a new documentation website, built on mkdocs-material.

This week, [work](https://cleura.com) launched a new documentation web site ([Cleura Docs](https://docs.cleura.cloud)) which my team and I had been building for several months.
Since this was my first foray into any significant tech writing in about 7 years, it was a fun exercise to see what tools are now available to the community, and how the technical landscape has changed in the interim.

This post is a summary of the technical considerations that went into creating that site, and the functional decisions that we made building it.

# What we use

We had early on made the decision that the site would use Markdown as its primary documentation format.
This is because Markdown strikes a nice balance between richness of expression, and ease of use.

[reST](https://en.wikipedia.org/wiki/ReStructuredText) and [DocBook](https://en.wikipedia.org/wiki/DocBook) are probably much more appealing to the die-hard tech writer, but they are also somewhat impenetrable and difficult to grok.
[AsciiDoc](https://asciidoc.org/) is just as expressive as DocBook (and indeed is semantically equivalent to it), but it is also somewhat obscure and niche.
Markdown, in contrast, is ubiquitous and comparatively intuitive, which makes it accessible to contributors who *aren't* full-time professional writers, which is exactly what we were looking for.

What we also wanted was a static site generator that could be kicked off from a CI run, with the ability to host the results pretty much anywhere (we currently run on GitHub Pages, but there is nothing that keeps us from running anywhere else).

So the combination of those factors quickly led to the selection of [MkDocs](https://www.mkdocs.org/), which I had last used in 2016 or thereabouts, and *holy mackerel* has it come a long way since.
This is in no small part due to [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) (also known as mkdocs-material), which is a *staggeringly excellent* way to render MkDocs sources, and has become something of a contemporary de-facto standard for technical documentation in the industry.

# How we use it

A *non-technical* decision that we also made early on is that the documentation should be available under a Creative Commons license, and that its whole build chain should be publicly available.
This is nice, because it allows me to go into the nitty-gritty of some technical details.[^github]

[^github]: You are welcome to take a peek at the [GitHub repo](https://github.com/citynetwork/docs/) where we maintain the documentation sources and CI infrastructure.

So, I am next going to go into a few elements of our MkDocs configuration that we found particularly useful.

## Plugins

There is an inordinate number of plugins available for MkDocs (and some, specifically, for mkdocs-material), of which we use a handful.

### macros

This is a plugin that allows you to use Jinja2 plugins in your Markdown sources.
It's exceedingly useful because product and service names, and other terms that may be relevant to your technical documentation, change.
Whenever that happens, you normally hear tech writers groan because they now need to dust of their `grep` and `sed` skills and embark on a massive search-and-replace effort.

With `mkdocs-macros`, you just define a variable under the `extra` key of your `mkdocs.yml` dictionary, and you're off. Like so:

```yaml
extra:
  support: "Service Desk"
plugins:
  - macros:
      # These settings are helpful because you want your build to fail if you're using an undefined macro.
      on_error_fail: true
	  on_undefined: "strict"
```

And then you can do this, in your Markdown sources:

```markdown
## Getting Help

For any further questions, contact our {{support}}.
```

Then when your support team decides they want to rename from "Service Desk" to "Service Center", you change just one line in your configuration.

### git-authors

I think it's always valuable to credit people's contributions individually.
The `git-authors` plugin lets you do that quite nicely (and it even gave me the opportunity to make [a tiny code contribution](https://github.com/timvink/mkdocs-git-authors-plugin/pull/66) in the process of incorporating it into our build).

```yaml
plugins:
  - git-authors:
      enabled: true
      show_email_address: false
```

You can take a look at [any random page](https://docs.cleura.cloud/howto/openstack/octavia/lbaas-l7pol/) for the inconspicuous "Authors" list at the bottom of the page.

### htmlproofer

One of the things that everyone hates when perusing documentation is when it contains dead links.
I think it is therefore incumbent on us documentation authors to employ a link checker, run it on every build, and not publish documentation that links to HTTP 404s.
The `htmlproofer` plugin lets us do just that:

```yaml
plugins:
  - htmlproofer:
      # We want dead links to fail the build, not just produce a warning.
      raise_error: true
	  validate_external_urls: true
```

Note that this can add a *significant* amount of time to the build (up to 50 seconds, in our case), so we find it helpful to be able to disable external link checking when we run `mkdocs serve`.
We can do that by adding one more line to the configuration:

```yaml
plugins:
  - htmlproofer:
      enabled: !ENV [DOCS_ENABLE_HTMLPROOFER, True]
      raise_error: true
	  validate_external_urls: true
```

Now if we don't do anything specific, links will be checked.
This is also what we use in CI runs.

However, we can also do this, which greatly facilitates work-in-progress:

```bash
export DOCS_ENABLE_HTMLPROOFER=false
mkdocs serve
```

## Analytics

At work we are acutely GDPR conscious so Google Analytics were a non-starter.
Thankfully, there is a European, privacy preserving, lightweight site analytics solution in [Plausible](https://plausible.io) (which I also use for [my site](/privacy)), which you can incorporate into mkdocs-material with a very tiny theme override.
Feel free to take a look at [the PR](https://github.com/citynetwork/docs/pull/59) if you want to do something similar.


## CI and deployment automation

Our test/build/deploy pipeline runs from `tox`, very similar to [what I've covered in some detail before]({filename}../resources/hints-and-kinks/universal-tox-tests.md).
This means that we can ship [a `.githooks` directory](https://github.com/citynetwork/docs/tree/main/.githooks) enabling documentation contributors to run the full test suite on every commit and push, that we can keep our [GitHub Actions workflows](https://github.com/citynetwork/docs/tree/main/.github/workflows) rather simple and lean, and that we can switch to a different build platform (such as GitLab) quite easily if we choose.


