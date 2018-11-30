Title: The Review Review
Date: 2021-10-07
Tags: Conference, GitLab, GitHub, Zuul
Slug: review-review
Summary: A talk I submitted to DevOpsDays Tel Aviv 2021 and DevConf.CZ 2022

This is a talk I submitted[^1] to
[DevConf.CZ](https://www.devconf.info/cz/) 2022, which used a
non-anonymized CfP process via [Red Hat’s CfP
website](https://cfp.devconf.info). For that conference, it was
selected as the lead talk in the Modern Software Development track.  I
had previously submitted this talk to DevOpsDays Tel Aviv 2021, which
used a non-anonymized CfP process via
[PaperCall](https://www.papercall.io/). That submission was rejected.

[^1]: If you’re curious why this is here, please read
    [this]({filename}../../blog/talk-submissions.md).

## Title

*The Review Review: comparing code review, testing, staging and
deployment across development collaboration platforms*

## Elevator Pitch

> You have 300 characters to sell your talk. This is known as the
> "elevator pitch". Make it as exciting and enticing as possible.

GitHub, GitLab, Gerrit — what should I choose? What’s the best review
process, the best CI/CD integration, the best deployment facility?
Which should I select for my startup, or consider migrating to? Which
supports good collaboration practices, which bad ones? This talk gives
the run-down.

## Talk Format

> What format is this talk best suited for?

Talk (~25-40 minutes)

## Audience Level

> Who is the best target audience for this talk?

Intermediate

## Description

> The description will be seen by reviewers during the CFP process and
> may eventually be seen by the attendees of the event. You should
> make the description of your talk as compelling and exciting as
> possible. Remember, you're selling both the organizers of the events
> to select your talk, as well as trying to convince attendees your
> talk is the one they should see.

In DevOps, the process of collaborative review, testing, staging, and
deployment to production constitutes a core element of the work we
do. And we generally strive to make this process as effective,
efficient, smooth, and transparent as possible. Achieving that partly
comes from the work culture we shape and inhabit, partly from our
selection of tools — and of course, work culture and work tools
permanently and closely influence each other. This goes for both the
tools that drive review, and the tools that drive CI/CD:

* the **GitHub Pull Request** process in combination with **GitHub
  Actions**;

* the **GitLab Merge Request** process in combination with **GitLab
  CI**;

* the **Gerrit Review** process in combination with **Zuul**.

None of these is perfect, all of them have their advantages and
disadvantages under particular circumstances. Some are meant to be
used principally as a service, some are fine to self-host. Some are
adamant about enforcing specific deployment practices, some follow a
more relaxed approach.

This talk is a summary of the current state of affairs with all these
tools, and contains recommendations on what to use under which
circumstances.

## Notes

> Notes will only be seen by reviewers during the CFP process. This is
> where you should explain things such as technical requirements, why
> you're the best person to speak on this subject, etc...

My team and I have worked with all tools mentioned in a professional
capacity, and I believe I've got a very good understanding of the
relative merits of the systems presented. This does not include a
hard-and-fast recommendation for one particular tool or platform.

This is a talk that's suitable for both in-person and on-line events.

## Tags

> Tag your talk to make it easier for event organizers to be able to
> find. Examples are "ruby, javascript, rails".

GitHub, GitLab, Gerrit, Zuul, CI/CD, Development, DevOps

