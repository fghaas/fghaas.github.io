Title: I Don’t Think This Means What You Think It Means: Red Herrings in OpenStack
Date: 2019-05-08
Tags: Conference, OpenStack
Slug: oidn-2019-red-herrings
Summary: A talk I submitted to OpenInfra Days Nordics 2019.

This is a talk I proposed[^1] for [OpenInfra Days
Nordics](https://openinfranordics.com/), via a non-anonymized CfP
process using [PaperCall](https://www.papercall.io/).

## Title

_I Don’t Think This Means What You Think It Means: Red Herrings in
OpenStack_

## Elevator Pitch

> You have 300 characters to sell your talk. This is known as the
> "elevator pitch". Make it as exciting and enticing as possible.

OpenStack’s complexity comes with operational challenges. And in
situations where OpenStack misbehaves, it is frequently non-trivial to
find the actual cause of an issue. This talk includes several examples
of red herrings in OpenStack, and suggestions for spotting
and avoiding them.

## Talk Format

Talk (>30-45 minutes)

## Audience Level

All

## Description

> This field supports Markdown. The description will be seen by
> reviewers during the CFP process and may eventually be seen by the
> attendees of the event.
>
> You should make the description of your talk as compelling and
> exciting as possible. Remember, you're selling both the organizers
> of the events to select your talk, as well as trying to convince
> attendees your talk is the one they should see.

When working with OpenStack, you deal with an environment that is
inherently complex. As with all complex environments, things sometimes
go wrong or behave unexpectedly. And when *that* happens, your
immediate goal is to locate, pinpoint, and then troubleshoot the
issue.

And then, sometimes, you go down the dead-wrong path, and end up
chasing a red herring for some time, before you find the real
problem. This talk contains examples of such red herrings, enabling
you to recognize and avoid them.

This talk is both for those who _run_ an OpenStack cloud, and those
who _consume_ its functionality as a service. It talks about both red
herrings in OpenStack operations, and red herrings in operating
applications _on_  OpenStack. 

## Notes

> This field supports Markdown. Notes will only be seen by reviewers
> during the CFP process. This is where you should explain things such
> as technical requirements, why you're the best person to speak on
> this subject, etc...

I’ve been working on OpenStack since 2012, have consulted on lots of
private and public cloud deployments using OpenStack, and I work for
the operator of a multi-region global OpenStack Cloud. “I've seen
things you people wouldn't believe. Attack ships on fire off the
shoulder of Orion...”

In addition to what **I** have seen, others have seen other things,
which is why I am crowdsourcing the content of this talk. That being
so, the talk proposal [is
public](https://xahteiwi.eu/talk-submissions/oidn-2019-red-herrings/),
and I am asking people [on
Twitter](https://twitter.com/xahteiwi/status/1126030330937380864) to
send me their stories, which I will add to and mix with my own, with
due attribution.

Just to give one example of what I would like to cover, see [this
article](https://xahteiwi.eu/resources/hints-and-kinks/1000-routers-per-tenant-think-again/)
on my web site, which talks about how you can run into what looks like
a quota issue in Neutron, but whose cause is in fact buried deep in
[RFC 5798](https://tools.ietf.org/html/rfc5798).

## Tags

> Tag your talk to make it easier for event organizers to be able to
> find. Examples are "ruby, javascript, rails".

OpenStack, Operations

[^1]: If you’re curious why this is here, please read
    [this]({filename}../../blog/talk-submissions.md).
