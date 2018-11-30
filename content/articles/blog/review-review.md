Title: The Review Review
Date: 2022-01-29
Slug: review-review
Tags: Work, CI, Gerrit, GitLab, GitHub, Zuul 
Summary: Musings on source code management, code review, testing, deployment, and collaboration culture.

I wanted to share a few thoughts on something I consider a rather
important topic in our industry: code review and CI/CD tools, and how
they relate.

This means that I'm talking about

* **source code management:** where we store our code, and how we
  manage access to it;
* **code review:** how we coordinate changes to our code;
* **testing and gating:** how we make sure that those changes don’t
  break anything;
* **deployment:** how we push changes and updates out to the consumers
  of our code.

In case it’s not obvious, that means I’m talking about a large
fraction of the software engineering cycle. Not all of it; the part
involving “fooling around” ([creative play]({filename}creativity.md))
is perhaps excluded — but substantially everything where people can be
said to be “developing” in a software engineering organization is
encompassed in these things.

And there’s a few things that follow from that:

First, whatever tools we use in order to accomplish these four things,
they simultaneously influence and *are* influenced by our
collaboration culture.

It's ludicrous to presume that tools and culture are independent of
each other, or to categorically declare that tools must be made to fit
processes, not the other way around. That’s not how people
work. Culture and tools always have an influence on each other.

Second, the scope of these things is continually expanding as the
field evolves. To illustrate, a few years ago a CI/CD platform could
get away with supporting automated unit tests and kicking off an
Ansible playbook to deploy things to VMs. Today, what we expect out of
a continuous deployment pipeline includes support for

* a package registry (for Python packages or Node.js modules, to give
  just two examples),
* a container image registry (for Docker/Podman/OCI containers),
* a secret store,
* the ability to deploy to a Kubernetes cluster.

And that’s just a few examples. I might be forgetting others.

Third, this is a classic example of where we must apply *[systems
thinking](https://youtu.be/EbLh7rZ3rhU):* since substantially
everything the organization does is connected to the toolchain, we
**cannot make changes to one part of the system without considering
the consequences for the system as a whole.** That is not to say that
we cannot make incremental changes, just that we can’t pretend that
anything in the system stands alone.

To illustrate what I mean, consider the example of an automotive
engineer implementing a design change for an engine. If the design
change makes the engine so much more efficient that it means a range
extension by 10% then that’s excellent. But if in the process the
designer has made it impossible to connect the engine to its battery
(or the fuel line, if we’re talking about obsolescent technology),
then installing the new engine doesn’t just not improve anything — it
renders the vehicle immobile.


## Responsibility

<!-- Note -->
Now, what does that mean about responsibility? Who is ultimately in
charge of the system consisting of source code management and review
tools, and your CI/CD pipeline? The answer is hopefully a no-brainer:
since everything I talk about *including* your organizational culture
encompasses substantially all of your engineering organization, the
responsibility rests with whoever is in charge of your engineering
organization (in most companies, that’s often the CTO). And if you’re
a software technology company so your *entire* enterprise is
substantially a software engineering organization, it’s your CEO’s or
MD’s responsibility.

Of course, that person may delegate some of the *tasks* and details of
running your source code management and code review and CI/CD
platform, but *responsibility* stays with them.

And that responsibility requires both an understanding [of the
technology itself]({filename}non-technical.md), *and* an understanding
of how it interacts with your engineering culture. A *profound*
understanding. 

And I’d go so far as to say if you head up a software engineering
organization and you *don’t* have a profound understanding of this
toolchain and its mutual influence on your culture, you should find
another job.

And if you work *in* a software engineering organization and the
person in charge lacks precisely that profound understanding, you
should *also* find another job, because you deserve better.

So having said all that, we can start talking about tools.

And I’m going to talk about three of them, all of which I use in some
professional capacity on an at-least-weekly basis.


<!-- .slide: data-timing="20" -->
# GitHub

The first one is the toolchain that — I think — a majority of open
source developers will be most familiar with: GitHub, whose
collaboration model is based on the *Pull Request* (PR).

Now the GitHub PR model was strongly influenced by the distributed
development model of the Linux kernel. The kernel project is what Git
was originally written for, so naturally it is also where the original
convention for pull requests emerged.

In kernel development, during a kernel merge window, subsystem
maintainers fix up a publicly accessible Git tree for Linus to pull
from. They then send a message that follows a conventional format to
the `linux-kernel` mailing list (the LKML) outlining the purpose of
the changes they want merged. This email contains a summary of the
changes, and then an enumeration of each commit to be merged. (There’s
a `git` subcommand, `git request-pull`, to format such a message.)

The review then proceeds in an email exchange on LKML. Once Linus is
happy with the change, he pulls from the subsystem maintainer’s branch
and informs them that their changes have merged.

Individual subsystem maintainers replicate this model, perhaps with
small modifications, for contributions to the subsystems they are
responsible for.

## GitHub Pull Requests (PRs)

GitHub replicates some features of the kernel’s model:

* The collaboration model is generally, “fork and pull”. Individuals
  maintain their own forks of an upstream codebase, and then send pull
  requests when they are ready to review. (However, the review process
  then uses a web interface, rather than a mailing list — in
  principle, a GitHub reviewer can do a complete review within the
  GitHub web interface and source code browser and would never even
  need to check out the repository locally.)
* Each PR generally consists of *multiple* commits, which however are
  expected to closely relate and serve a common purpose.
* That common purpose is enumerated in a summary at the top of the
  pull request. GitHub calls this the PR description.
* Submitters can mark a PR as a draft, with which they indicate that
  the PR is not ready to be merged yet. When drafts [became
  available](https://github.blog/2019-02-14-introducing-draft-pull-requests/)
  in 2019, they replaced an emerging convention in which PR
  descriptions would be prefixed by `WIP` *(work in progress)* or
  `DNM` *(do not merge)*.

GitHub PRs can be *approved,* *rejected* or *commented on* by
maintainers or other contributors, and an approval can be made a
mandatory requirement for merging, but by default GitHub will let
anyone merge the PR who has write permissions to the repository that
the PR targets. This includes the possibility for a maintainer to
merge the contributor’s remote branch to their own local checkout, and
then pushing the merged branch to he target repo of the PR. Such an
event will automatically close the PR and mark it as merged.


## GitHub Actions

GitHub has, for a long time, allowed maintainers to require that PRs
pass automated testing. However, until rather recently, it relied on
them to run (or interface with) a separate testing infrastructure
outside of GitHub to do that. Typical examples for this included
CircleCI, or Travis, or Jenkins. It was only [in
2019](https://github.blog/2019-08-08-github-actions-now-supports-ci-cd/)
that GitHub announced automated testing via GitHub Actions.

At the time of writing however, GitHub Actions workflows are in
widespread use for CI/CD, *but* it is still quite common for
GitHub-hosted projects to allow maintainers to circumvent CI/CD tests
and merge directly. When this happens, it often creates a rather
unpleasant situation in which CI/CD testing is only run for
contributions by “outsiders” or “newbies”, whereas maintainers get to
break things with impunity. This means that issues are often not
detected until a casual contributor sends a PR, at which point the
test breaks and leave the contributor confused (and sometimes lead to
the change not even being considered because, well, “it makes the
tests break.”)

Another thing that comes bundled with GitHub (and GitHub workflow
actions) is the ability to maintain your own package registry [and
push artifacts to it from your
workflow](https://docs.github.com/en/packages/managing-github-packages-using-github-actions-workflows/publishing-and-installing-a-package-with-github-actions). Interestingly,
at the time of writing, GitHub’s definition of “packages” includes
container images, Ruby gems, and npm modules [among
others](https://docs.github.com/en/packages/working-with-a-github-packages-registry),
but presently does not include Python modules — although you do, of
course, have the option to [push your packages to PyPI from your
workflow](https://github.com/marketplace/actions/pypi-publish).

# GitLab

The equivalent to the GitHub *pull request (PR)* is the GitLab *merge
request (MR)*. In principle, a GitLab MR is quite similar to a GitHub
PR, albeit with a few noticeable differences:

* The “fork and pull” model is less prevalent on GitLab. Instead, it
  is far more common for collaborators to work on one project, and
  then create topic branches within that project for each set of
  changes.
* Since the project repo is shared, this facilitates collaboration on
  a single changeset by multiple people: if two or more people wish to
  collaborate on a change, they simply push additional squash or fixup
  commits on the topic branch. They can *also* agree to force-push
  amended commits to the topic branch, in which the GitLab web
  interface will helpfully point out differences between individual
  *versions* of a commit (something that GitHub presently cannot do in
  a PR).
* As in a GitHub PR, a GitLab MR is generally expected to include one
  or more commits.
* Also as in a GitHub PR, an MR is expected to contain a summary that
  outlines its purpose.
* GitLab MRs have a Draft status just like GitHub PRs do, and they
  were introduced about the same time in both products, but GitLab had
  a preceding feature called work-in-progress MRs (WIP MRs). GitLab
  has the handy feature that MRs are *automatically* marked as drafts
  once any commit with `squash:` or `fixup:` in the commit message
  ends up in the topic branch — GitLab rightfully infers that the
  branch still needs a squash rebase prior to merge.
* GitLab MRs can be reviewed in full using the web interface alone:
  the review interface and the source code browser are closely
  integrated, just like in GitHub.


## GitLab CI

CI/CD has been an intrinsic part of the GitLab review
experience for years, since GitLab includes full CI integration via
the `.gitlab-ci.yml` configuration file.

Since GitLab CI has been around for quite a while, and it has a
multitude of ways to be used, it “feels” more intrinsic to the review
process than GitHub Actions do, which to me still leave an impression
of being bolted on. In addition, GitLab CI comes with multiple options
of using the CI *runner:*

* You can use *shared runners,* which GitLab operates for you. These
  are Docker containers that GitLab spins up on your behalf in the
  cloud, and which you share with other GitLab subscription customers.
* You can also host your own runners. You can do that in Docker
  containers, in Kubernetes clusters, in virtual machines, and even on
  bare metal. The runners need no incoming network connectivity; they
  simply connect to a service on your GitLab host and then poll
  whether jobs wait for them.
* You can also specify runners that are exclusive to a project, or to
  a group or subgroup of projects.

GitLab also comes with a [package
registry](https://docs.gitlab.com/ee/user/packages/package_registry/),
to which you can push packages from CI pipelines. This differs from
GitHub in such a way that it [includes more package different
formats](https://docs.gitlab.com/ee/user/packages/package_registry/#supported-package-managers),
including a private PyPI workalike for Python packages. In addition,
there’s also a separate [container
registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
for container images.


# Gerrit/Zuul

Now, it feels a bit awkward to call this one “Gerrit/Zuul” when I’ve
called the others just “GitHub” and “GitLab” respectively, and tacitly
included the corresponding CI integrations (GitHub Actions and GitLab
CI, respectively) in them. There are a couple of reasons for that:

* Zuul is a CI/CD framework that is, in principle, not tied to Gerrit,
  whereas GitHub Actions only apply to GitHub, and GitLab CI only to
  GitLab. Gerrit/Zuul is a particular combination that was largely
  popularized by the OpenStack community, which is why a lot of people
  who are or were part of that community intuitively associate Gerrit
  with Zuul and vice versa.
  <!-- It should be noted that Zuul was not the original CI/CD framework in
  the OpenStack community. It was *developed* (and adopted) by that
  community when it found that it was outgrowing the boundaries of its
  original CI/CD platform (Jenkins). -->
	
* Likewise, Gerrit is not tied to a specific CI/CD framework. It’s
  perfectly feasible to run code reviews in Gerrit and use a different
  CI/CD pipeline (or even none at all).

And Gerrit/Zuul does differ quite notably from GitHub and GitLab,
whose features often map quite closely to each other, and I’d like to
highlight some of those differences.

## Gerrit reviews

The Gerrit review process differs in a few crucial points from the one
we know from GitHub and GitLab:

* You don’t ask someone to pull from a branch or a fork or
  yours. Instead, you run `git review` and Gerrit will *make a branch
  for you.* Everything else flows from there.

* Unlike a GitHub PR and GitLab MR, which both typically contain a
  series of commits to be taken as a whole, a Gerrit *change* is
  really just that: one change. 
  
* Which, of course, also means that we don’t need a separate summary
  for the change: the summary is the commit message.
 
* It’s still possible to submit a series of commits in the course of a
  Gerrit review. However, Gerrit simply sees those as a series of
  changes that all depend on one another.

* Dependencies between changes can also be expressed explicitly, by
  including appropriate keywords in commit messages. Crucially, these
  dependencies *can cross project boundaries.* That is to say, a
  change in one Git repository can depend on a change in *another* Git
  repository, so long as they both use the same Gerrit instance for
  review.
* And we also have the equivalent of a Draft PR/MR; in Gerrit that’s
  called a work-in-progress change.

Because of this, when used in combination with CI such as Zuul, a
Gerrit-reviewed project generally expects CI tests to pass *on every
commit,* without exceptions. This is in contrast to many GitHub or
GitLab managed projects, which typically only expect the head commit
of the topic branch associated with a PR/MR to pass CI.

In Gerrit/Zuul managed projects, it’s also Zuul that merges the
commit. This is also in contrast to projects that live in GitHub or
GitLab: in those, the pipeline run results are generally advisory in
nature, and a successful pipeline run must still be confirmed by a
human clicking a *Merge* button (or running a `git merge` command
locally, and then pushing to the repository). In addition, even a
failing CI run can generally be overridden by a “core committer” who
has the ability to merge the PR/MR anyway.

A Gerrit/Zuul project typically has no such shortcuts, meaning the
*only* way to get changes into the repo is to pass both peer review,
and the CI pipeline. In my experience, this tends to create a climate
of leadership by example, which has a beneficial effect on both
experienced developers (“seniors” in a corporate setting) and
newcomers (“juniors”).


### Speculative merging

There is one other property that Gerrit/Zuul has that sets it apart
from other review/CI toolchains: *speculative merging.* This involves
the [parallel execution of CI jobs for interdependent
changes](https://zuul-ci.org/docs/zuul/3.10.2/user/gating.html#testing-in-parallel). With
speculative merging, even complex, long-running CI/CD pipelines don’t
hold up the development process — and this massively enhances project
scalability.


### No direct repo browser integration

Notably, in Gerrit/Zuul there is no close integration with repository
browsing. Gerrit does include the
[Gitiles](https://gerrit.googlesource.com/gitiles/) plugin for the
purpose, but its user experience is rudimentary at best. A popular
alternative is to deploy Gerrit with [Gitea](https://gitea.io/en-us/),
but again, that’s not built-in and your trusted Gerrit/Zuul admin has
to set it up for you. In addition, while source code browsing in
GitHub and GitLab is tightly integrated with project permissions, and
that is also true for Gitiles, there is a certain amount of
administrative duplication to make your Gerrit repository and project
permissions apply to Gitea.


### No built-in package registries

There’s another difference in the Gerrit/Zuul stack when compared to
GitHub and GitLab, and that is its absence of built-in package
registries. Zuul has ready-to-use *jobs* for [pushing to a container
registry](https://zuul-ci.org/docs/zuul-jobs/docker-image.html), or to
[PyPI](https://zuul-ci.org/docs/zuul-jobs/python-jobs.html#job-python-upload-pypi),
but you do have to either push to upstream public registries, or build
your own. Zuul does not come bundled with multitenant private
registries the way GitHub and GitLab do.


### Administrative complexity

In view of the above, there's another thing that you might want to
consider, which in my humble opinion is an important reason why the
Gerrit/Zuul combination has less uptake than it deserves on its
technical merits. And this may sound overly dramatic, but: people like
to be in charge of their own actions, and software developers are
people. And here’s an issue with Zuul: there are quite a few things a
developer can do on their own in GitHub Actions or GitLab CI that
they’d need to ask an admin’s help for in Zuul.

Creating a relatively standard workflow of building a private
container image, pushing it to your own registry, and then rolling out
that image to a Kubernetes deployment, is something you can do in
GitHub or GitLab as a project owner. With Zuul, you’ll need an admin
at least to set up and manage your container registry. Rerunning a
pipeline, a simple click of a button or API call in GitHub or GitLab,
is something you trigger via a Gerrit keyword (typically `recheck`)
for Zuul — but only on the pipelines where [your admin has defined
that
trigger](https://zuul-ci.org/docs/zuul/3.11.0/admin/drivers/gerrit.html#reference-pipelines-configuration).


# So, which one’s best?

So you want to know which one of these *you* should choose (or
advocate for)? That’s surprisingly difficult to answer, and greatly
depends on your priorities. And I’ll give you this from four angles.

* When it comes to *scalability* — the ability to adapt to massive
  organizational sizes, and/or rapid project growth, or an obscenely
  large number or projects within an organization — the Gerrit/Zuul
  combination wins hands down **if** you have a competent, responsive,
  and dedicated crew to manage it.

* When it’s about *getting started quickly* — helping a project get
  off the ground with a good, usable, easily manageable review and
  fully integrated CI/CD structure — you can’t beat GitLab.

* In terms of *beneficial effect on your development culture,*
  Gerrit/Zuul again probably scores best. If you have a team that’s
  great at reviews and commit and CI and doesn’t cut corners, or you
  want to build a team like that, Gerrit/Zuul can really help.

* And when it’s about *giving developers the lowest barrier to entry*
  — meaning using tools that they’re most likely already familiar with
  — GitHub is your platform of choice.
