Title: Making docs with MkDocs
Date: 2023-02-23 21:00
Slug: mkdocs
Summary: At work, my team and I built and launched a new documentation website, built on Material for MkDocs.

This week, [work](https://cleura.com) [launched](https://cleura.com/articles/docs-cleura-cloud-open-source-documentation-for-all-things-cleura/) a new documentation web site ([Cleura Docs](https://docs.cleura.cloud)) which my team and I had been building for several months.
Since this was my first foray into any significant tech writing in about 7 years, it was a fun exercise to see what tools are now available to the community, and how the technical landscape has changed in the interim.

This post is a summary of the technical considerations that went into creating that site, and the functional decisions that we made building it.

# What we use

We had, early on, made the decision that the site would use Markdown as its primary documentation format.
This is because Markdown strikes a nice balance between richness of expression, and ease of use.

[reST](https://en.wikipedia.org/wiki/ReStructuredText) and [DocBook](https://en.wikipedia.org/wiki/DocBook) are probably much more appealing to the die-hard tech writer, but they are also somewhat impenetrable and difficult to grok.
[AsciiDoc](https://asciidoc.org/) is just as expressive as DocBook (and indeed is semantically equivalent to it), but it is also somewhat obscure and niche.
Markdown, in contrast, is ubiquitous and comparatively intuitive, which makes it accessible to contributors who *aren't* full-time professional writers, which is exactly what we were looking for.[^formats]

[^formats]: Lest you think I am bashing something I am clueless about, I have used all the mentioned formats for technical documentation in a professional capacity:
    reST (with Sphinx) for contributions to the Ceph and OpenStack docs, AsciiDoc in the context of Linux-HA, and DocBook XML for ancient versions of the Pacemaker documentation and, believe it or not, for my thesis.
    And Markdown, obviously, for too many things to count. 

What we also wanted was a static site generator that could be kicked off from a CI run, with the ability to host the results pretty much anywhere.
We currently run on GitHub Pages, but there is nothing that keeps us from running anywhere else.

So the combination of those factors quickly led to the selection of [MkDocs](https://www.mkdocs.org/), which I had last used in 2016 or thereabouts, and *holy mackerel* has it come a long way since.
This is in no small part due to [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) (also known as mkdocs-material), which is a *staggeringly excellent* way to render MkDocs sources, and has become something of a contemporary de-facto standard for technical documentation in the industry.

Finally, as a *theoretical* documentation framework we adopted [Diátaxis](https://diataxis.fr/), which is also becoming something of an industry default.

We furthermore decided that *within* the Diátaxis framework, we would follow this order of priorities:
How-to guides would come first, followed by the necessary amount of reference material.
Once those bits were considered *sufficient to be useful* (not "complete" --- documentation is never complete), we would be ready to drop the "beta" warnings from the site and announce it publicly.
Then we would start adding background explanations, and finally, tutorials.

As I write this article, [the site is out of beta](https://github.com/citynetwork/docs/pull/124), we have [just started on the background bits](https://docs.cleura.cloud/background/), and no tutorials do as yet exist --- although we do have [academy.cleura.cloud](https://academy.cleura.cloud) which has full-blown training courses.

# How we use it

A *non-technical* decision that we also made early on is that the documentation should be available under a Creative Commons license, and that its whole build chain should be publicly available.
This is nice, because it allows me to go into the nitty-gritty of some technical details.[^github]

[^github]: You are welcome to take a peek at the [GitHub repo](https://github.com/citynetwork/docs/) where we maintain the documentation sources and CI infrastructure.

So, I am next going to go into a few elements of our MkDocs configuration that we found particularly useful.

## Plugins

There is an inordinate number of plugins available for MkDocs (and some, specifically, for mkdocs-material), of which we use a handful.

### macros

This is a plugin that allows you to use Jinja2 expressions in your Markdown sources.
It's exceedingly useful because product and service names, and other terms that may be relevant to your technical documentation, change.
Whenever that happens, you normally hear tech writers groan because they now need to dust off their `grep` and `sed` skills and embark on a massive search-and-replace effort.

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
The `git-authors` plugin lets you do that quite nicely.
And it even gave me the opportunity to make [a tiny code contribution](https://github.com/timvink/mkdocs-git-authors-plugin/pull/66) in the process of incorporating it into our build.

```yaml
plugins:
  - git-authors:
      enabled: true
      show_email_address: false
```

You can take a look at [any random page](https://docs.cleura.cloud/howto/openstack/octavia/lbaas-l7pol/) on the site for the inconspicuous "Authors" list at the bottom of the page.

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

Note that this can add a *significant* amount of time to the build (up to 50 seconds, in our case), so we find it helpful to be able to disable external link checking when we run `mkdocs serve` locally.
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

## Content tabs

A feature in mkdocs-material that has proven to be very useful are [content tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/).

It turns out that more often than not, particularly when dealing with an infrastructure platform, there's more than one way to do something.
Then, you often end up interspersing explanatory content (which is the same regardless of the tool you use) with command examples (which are of course tool-specific).
The use of content tabs makes this kind of content a breeze to write and maintain.

For example, we expose an S3-compatible object store API with [Ceph radosgw](https://docs.ceph.com/en/latest/radosgw/), and there you can frequently do things just as well with `aws s3api` or `s3cmd` or `mc`.
With content tabs, we are able to explain complex features in a relatively uncluttered and compact way, without losing the necessary detail.

This comes in handy even if we want to be specific about some functionality *not* being available in a particular tool.
Consider this example from the page on [S3 bucket versioning](https://docs.cleura.cloud/howto/object-storage/s3/versioning/):

```markdown
## Enabling bucket versioning

To enable versioning in a bucket, use one of the following commands:

=== "aws"
    ```bash
    aws --profile <region> \
      s3api put-bucket-versioning \
      --versioning-configuration Status=Enabled \
      --bucket <bucket-name>
    ```
=== "mc"
    ```bash
    mc version enable <region>/<bucket-name>
    ```
=== "s3cmd"
    This functionality is not available with the `s3cmd` command.
```

## Git integration

Material for MkDocs has [excellent integration](https://squidfunk.github.io/mkdocs-material/setup/adding-a-git-repository/) with GitHub, GitLab, and other Git-based revision control and collaboration platforms.

We chose to use that to its fullest extent, to the point where every single page has an edit button, and things are made as easy as possible for drive-by contributors.
We also wrote a [guide for submitting changes](https://docs.cleura.cloud/contrib/modifications/), and a general [contribution guide](https://docs.cleura.cloud/contrib/).

For people who don't want to write a patch but do want to report a problem or bug, we implemented [GitHub issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms) (currently in beta, we hope they stay) --- and wrote a [separate guide](https://docs.cleura.cloud/contrib/issues/) for using those, too.

## CI and deployment automation

Our test/build/deploy pipeline runs from `tox`, very similar to [what I've covered in some detail before]({filename}../resources/hints-and-kinks/universal-tox-tests.md).
This means that we can ship [a `.githooks` directory](https://github.com/citynetwork/docs/tree/main/.githooks) enabling documentation contributors to run the full test suite on every commit and push, that we can keep our [GitHub Actions workflows](https://github.com/citynetwork/docs/tree/main/.github/workflows) rather simple and lean, and that we can switch to a different build platform (such as GitLab) quite easily if we choose.

## Analytics

At work we are acutely GDPR conscious, so Google Analytics were a non-starter.
Thankfully, there is a European, privacy-preserving, lightweight site analytics solution in [Plausible](https://plausible.io) (which I also use for [my site](/privacy)), which you can incorporate into mkdocs-material with a very tiny theme override.
Feel free to take a look at [the PR](https://github.com/citynetwork/docs/pull/59) if you want to do something similar.


# How it's going

Overall, feedback on the new site has been unanimously positive.
This is nice, but what is even better (and highly important, in the long run) is that people evidently find it very straightforward to make contributions.
Our colleagues no longer even ask how they can help out --- they just do it, some of them making extremely impressive content additions even on their first PR.

So that feels very promising.
