Title: Fragile Development: Scrum is terrible, and you should ditch it
Date: 2016-07-05
Modified: 2023-11-24
Slug: fragile-development
Author: florian
Summary: Scrum is irrational, impractical, and outright dangerous for software development. It is time to stop considering it a viable method for building software.
Tags: Philosophy, Development
Series: Scrum thoughts

This is a writeup of an
[Ignite](https://en.wikipedia.org/wiki/Ignite_(event)) talk I gave at
[OpenStack Israel 2016](http://www.openstack-israel.org).[^2023] The
paragraph headings below approximately correspond to the content of my
talk slides; the paragraphs themselves are an approximation of what I
said. If you're interested in the exact slide content, you can find
that [here](//fghaas.github.io/openstackisrael2016-ignite).

[^2023]: I subsequently reprised this talk, in 2023, at [PyCon Sweden](https://pycon.se). The updated slide deck is [here](https://fghaas.github.io/pyconse2023).

* * *

## Zero flexibility

> `_____`'s roles, artifacts, events, and rules are _immutable_ and
> although implementing only parts of `_____` is possible, _the result
> is not_ `_____`.

When you see a statement like this and wonder what should be filled in
for the blanks, it's rather quite likely that you would guess either a
radical political ideology, a very strict religious sect or cult, or
something to that effect. You couldn't be further from the truth.

> `Scrum`'s roles, artifacts, events, and rules are _immutable_ and
> although implementing only parts of `Scrum` is possible, _the result
> is not_ `Scrum`.

Yes, that's a
[direct quote from the Scrum guide.](https://web.archive.org/web/20160630123010/http://www.scrumguides.org/scrum-guide.html#endnote)[^2020]
Scrum, by its own definition, can either be implemented completely —
that is, with all its roles, artifacts, events, and rules _unchanged_
— or not at all. This sounds ludicrous enough as it is, and any sane,
thinking person should reject or at least resent _any_ such statement
outright. But let's give Scrum the benefit of doubt, and let's
actually start examining some of its postulates.

[^2020]: The end note in the post-2020 version of the Scrum guide reads [slightly differently](https://scrumguides.org/scrum-guide.html#end-note). It now simply says, "The Scrum framework, as outlined herein, is immutable. While implementing only parts of Scrum is possible, the result is not Scrum." In other words, it still makes the same immutability assertion, just in fewer words.

## Teams are self-organizing

Scrum hinges on the idea that teams are comprised of capable
individuals forming teams, which then self-organize. Now I'm sure
nobody would argue that self-organizing teams cannot exist, so this
postulate does not invalidate itself outright.

However, it is missing an important prerequisite: teams can
self-organize **if they are stable.** And team stability is a
precondition that almost never exists in the software industry: our
industry is _growth-oriented,_ and driven by quickly-growing startups,
so in a successful organization having a new colleague every other
month is not unheard of. It is also highly _competitive_ for talent,
so having a colleague leave every few months isn't unusual either. The
moment a new person joins or leaves, you have a new team. Team
stability goes out the window, and with it any reasonable expectation
of self-organization.


## Sprint after sprint after sprint

The Scrum Guide explicitly states that every _sprint_ (a time frame of
one month or less, in which the team completes objectives agreed to
for the sprint backlog) is _immediately followed by the next sprint._

This is mind-bogglingly ludicrous and outright dangerous to your
team's mental health. Software development is a marathon, and running
a marathon as an unbroken series of sprints leads to collapse or
death. In software development, it's likely to cause burnout.


## The Daily Scrum

One of Scrum's immutable events is the Daily Scrum. The Scrum Guide
defines this event as a specific, daily occurrence, time-boxed to 15
minutes and involving the entirety of the development team.

This is staggeringly out of place in the modern development team,
which may well be spread out over multiple offices and timezones, and
may not even physically be in one place more than a handful of times a
year. Even in the unlikely event that everyone _can_ get together in
one room for precisely fifteen minutes each day, have you ever been in
a meeting involving more than 3 people that got anything accomplished
in 15 minutes?

And remember, 15 minutes. Time-boxed, immutable. If you think _your_
Daily Scrum can be 30 or 45 minutes, or you can do it just every other
day or maybe thrice a week, recall: if you do that, you're no longer
doing Scrum.


## No planning beyond the current sprint

Scrum is quite emphatic that the only thing developers should be
really concerned about in terms of planning is the next 24 hours (the
plan for which is ostensibly being laid out in the Daily Scrum), and
beyond that, the current sprint at a maximum. Now, while the idea of
freeing people's minds and allowing them to focus on a single task at
hand is certainly laudable, the practical implications of having no
medium to long-term planning is insane.

I'd venture a guess that an approach where no planning is for more
than a month out is viable, under one condition: having exactly zero
users and/or customers for the product you are developing. I leave it
to you to decide how valuable it is, then, to develop the product in
the first place.


## Permanent emergency mode

Arguably, some of the methods proposed in Scrum are quite suitable for
emergency situations. In a situation where you need to come up with a
solution that requires creativity, hustle, and speed, you may well sit
down, put down a requirements list, elect a coordinator and
spokesperson for your team, and just start hacking. I'd fully agree
that such situations can be extremely challenging, and quite
satisfying to come out of with flying colors.

But if your organization is permanently operating in this mode,
**quit.** It doesn't matter which role you're in: as a developer,
you're headed for burnout. As a manager, you're herding your team into
burnout. Either way, you shouldn't be doing this job, either in your
own interest or in that of others.


## Novelty?

Scrum proponents frequently argue in its favor as the antithesis of
the obsolete waterfall model, where all deliverables are defined from
the outset and there is no room for deviation, leading to products
that are either broken, or outdated, or both the moment they are
completed. If you think we only found out recently that waterfall is
bad, you've been asleep at the switch for over 30 years. In his
seminal
[Mythical Man-Month](https://en.wikipedia.org/wiki/The_Mythical_Man-Month)
essay collection from 1975, Fred Brooks pointed out some weaknesses of
this model, and in his 1986 follow-up
[No Silver Bullet,](https://en.wikipedia.org/wiki/No_Silver_Bullet) he
proposes organic, incremental software development as an alternative.


## Your team can't work with Scrum?

Scrum advocates frequently argue that if Scrum doesn't work with your
team, chances are that your team is the problem. This means that you
should either replace them, or at least educate them in the ways and
means of Scrum, so they can become a better-performing team.

At this point, it should be fairly obvious that if Scrum doesn't work
for your team, the problem is not your team. The problem is Scrum.


## What if Scrum doesn't deliver?

And finally, Scrum proponents usually argue that if Scrum fails to
deliver adequate results in your organization, it's likely because you
aren't applying its central tenets correctly. In other words, you must
come to your senses, and implement Scrum as designed, and which point
results with magically appear, and your team will be in a constant
state of flow.

This is nonsense. **If** you were able to actually do Scrum (meaning
in its pure, immutable, One True Way), it would surely lead to
disaster. But, it's impossible to do so anyway, so go ahead and ditch
it — stop being a scrumbag.


* * *

This article originally appeared on my blog on the `hastexo.com` website (now defunct).
