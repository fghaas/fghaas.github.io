Title: Meaningless Metrics, Treacherous Targets
Date: 2021-11-14
Tags: Work, Communications
Slug: meaningless-metrics-treacherous-targets
Summary: A quick introduction to Goodhart, Strathern, Campbell, Yankelovich, and McNamara.

A common feature of organizations in the software technology industry
(but certainly not *only* in that industry) is their fixation on
metrics, measurements, and quantifiers. I understand that this is
frequently done and advocated for in the spirit of making management
more objective, less arbitrary, more scientific, and perhaps
fairer. But since they say that the road to hell is often paved with
good intentions, here's a quick summary of what we know about about
the undesirable side effects of such an approach.


## Goodhart’s Law

British economist [Charles
Goodhart](https://en.wikipedia.org/wiki/Charles_Goodhart) wrote in
1975, in an article about British monetary policy:

> Any observed statistical regularity will tend to collapse once
> pressure is placed upon it for control purposes.
>
> — Charles Goodhart, “Problems of Monetary Management: the
> U.K. Experience” (1975)

That's a mouthful of somewhat niche technical jargon, but let me try
to paraphrase it like this:

* You collect some data.
* You crunch the numbers using statistics.
* You observe a pattern.
* You distill a value (a “statistical regularity”) from it.
* Someone decides that that value should change: it is too high or too
  low.
* Someone — an individual or a group — is tasked with bringing that
  value up or down, and then keeping it high or low, or rising or
  falling, or above or below a particular threshold.
* That value now is no longer a useful statistical indicator.

What you *probably* knew as *Goodhart's Law* if you'd heard about it
prior to reading this article is a generalization by anthropologist
[Marilyn Strathern](https://en.wikipedia.org/wiki/Marilyn_Strathern),
also from the UK:[^why-goodhart]

> When a measure becomes a target, it ceases to be a good measure.
>
> — Marilyn Strathern, “['Improving ratings': audit in the British
> University
> system](https://archive.org/details/ImprovingRatingsAuditInTheBritishUniversitySystem)”
> (1997)

[^why-goodhart]: The reason the condensed version is called
	“Goodhart’s Law” and not “Strathern’s Law” is apparently due to a
	coinage by British researcher Keith Hoskin, who wrote a year prior
	to Strathern, in a paper she cited:
    > “Goodhart’s Law” — that every measure which becomes a target becomes
    > a bad measure — is inexorably, if ruefully, becoming recognized as
    > one of the overriding laws of our time.
    > 
    > — Keith Hoskin, “The ‘awful idea of accountability’: inscribing
    > people into the measurement of objects” (1996)

Why is that so? It’s because once you make the measure a target that
has an influence on people (for example, meeting it gets them a bonus,
failing at it gets them a demotion), you have wired them to improve
*the measure,* and not necessarily to improve the underlying
conditions that the measure originally arose from. Therefore, they
might opt for gaming the measure, because that gets them to their goal
(a promotion, for example) more quickly and at less effort to them.

Furthermore, even keeping the option of fudging the numbers aside:
when faced with a choice between doing something that might have a
negative effect on the measure and something else that might have a
negative effect on something *other than* the measure, people will
tend to choose the latter. This may lead to situations where people
*avoid* an activity with *significant* inherent value, just to avoid
depressing a measurement — a concept known as *creaming.*[^creaming]

[^creaming]: If you think that term sounds a bit odd, I’d agree. I
    guess it comes from the idea of milking a cow and then skimming
	only the cream, discarding the rest.

For example, a hospital may be interested in measuring individual
surgeons’ intraoperative death rates: the percentage of a surgeon’s
patients that die in the middle of surgery. On its face, this metric
could help weed out bad surgeons. If a particular surgeon is an
outlier and has *way more* patients dying on their operating table
than their peers, it’s possible that that surgeon might be doing
something wrong: they could be incompetent, or frequently intoxicated,
or even be a [Dr. Death](https://en.wikipedia.org/wiki/Dr._Death) type
serial killer.

It gets tricky, though, when in the interest of transparency the
hospital doesn’t just fire or retrain incompetent surgeons which it
identifies based on such statistics, but when it “publishes” the
patient mortality data. (I use quotes here because this does not
necessarily mean sharing it with the general public, but perhaps
sharing it with all of the surgical staff.) At that stage, an
individual surgeon's *rank* in the statistics will become at least a
matter of pride, status, and prestige, even if it’s not otherwise
rewarded in any way, nor seen as a precondition for continued
employment.

This, then, will incentivize surgeons to *avoid* taking on risky
surgeries where there is a significant chance of the patient dying
mid-surgery — surgeries typically *attempted* in the first place to
save the patient’s life, in the course of an immediate major
emergency. Thus, Dr. Alpher who only ever treats torn knee ligaments
might look better in the ranking than Dr. Bethe the polytrauma
specialist, or Dr. Gamow the neurosurgeon who specializes in
particularly challenging malignant brain tumor removal. If there is a
non-negligeable risk of intraoperative death for a particular brain
cancer patient and such an event would be bad for Dr. Gamow’s ranking,
then Dr. Gamow might have an incentive to declare that patient
inoperable — and as a result the patient would *certainly* die, just
not in surgery.[^tyranny]

[^tyranny]: The surgery statistics example of creaming is paraphrased
    from Jerry Z. Muller, “[The Tyranny of
    Metrics](https://press.princeton.edu/books/hardcover/9780691174952/the-tyranny-of-metrics)”
    (2018).

## Campbell's Law

Although less well known than Goodhart’s law, Campbell’s law is
closely related and, in my humble opinion, just as important.

[Donald
T. Campbell](https://en.wikipedia.org/wiki/Donald_T._Campbell), a
U.S.-based social scientist, wrote in 1976, on the subject of
standardized testing in education:

> The more any quantitative social indicator is used for social
> decision-making, the more subject it will be to corruption pressures
> and the more apt it will be to distort and corrupt the social
> processes it is intended to monitor.
>
> [...]
>
> Achievement tests may well be valuable indicators of general school
> achievement under conditions of normal teaching aimed at general
> competence. But when test scores become the goal of the teaching
> process, they both lose their value as indicators of educational
> status and distort the educational process in undesirable ways.
>
> — Donald T. Campbell, “Assessing the impact of planned social
> change” (1976)

In other words, if you conduct a one-time evaluation of student
achievement across many students in multiple schools, then the fact
that the test is standardized might help in achieving comparable
results. However, as soon as you make the tests a repeat occurrence,
and tie students’ test results to school funding allocations, teacher
salaries, or even just school prestige, you’re undermining their
original purpose: teachers will now spend a significant portion of
their time and effort to ensure that students *score well on the
test*, rather than build the competence that the test was originally
designed to measure.

This is an example of allocating resources (teacher and student time
and effort) to an activity with no inherent value (taking a
standardized test) just to improve a measurement (the test score). And
since the resources are finite, spending them on the activity with no
inherent value (test-taking) makes less of them available to the
inherently valuable activity the indicator is intended to assess
(teaching and learning). This is the “corruption and distortion”
Campbell talks about.


## The McNamara Fallacy, and the Yankelovich Ladder

Closely related to Goodhart’s, Strathern’s and Campbell’s observations
is something called the McNamara Fallacy.

[Robert McNamara](https://en.wikipedia.org/wiki/Robert_McNamara),
U.S. Secretary of Defense during much of the Vietnam war, infamously
believed that he could scientifically measure the progress of the war
by quantitative indicators alone. One of his favourites was *body
count,* the number of enemy personnel killed, in comparison to
friendly casualties. The rationale appears to have been, whatever
other factors (qualitative or quantitative) are in play, whichever
side kills more of the other wins the war. Indeed he seems to have
been inclined towards ignoring all non-quantitative indicators of how
the war was going.

An anecdote
[told](https://en.wikipedia.org/wiki/McNamara_fallacy#The_Vietnam_War)
by U.S. Air Force general [Edward
Lansdale](https://en.wikipedia.org/wiki/Edward_Lansdale) alleges that
he (Lansdale) pointed out to McNamara in a briefing that McNamara,
when assessing the progress of the war, failed to take into account
the feelings of the common rural Vietnamese people. McNamara then
allegedly wrote an item saying “feelings of the Vietnamese people” on
his list of things to keep track of in pencil, pondered it for a
moment, and then erased it — reasoning to Lansdale that feelings
cannot be measured, thus must not be important.[^lansdale]

[^lansdale]: The Lansdale/McNamara anecdote is paraphrased from [the
    Wikipedia article on the McNamara
    Fallacy](https://en.wikipedia.org/wiki/McNamara_fallacy), which in
    turn cites Rufus Phillips and Richard Holbrooke, “Why Vietnam
    Matters: An Eyewitness Account of Lessons Not Learned” (2008) as
    its source.

This is step 3 on a progressive scale social scientist [Daniel
Yankelovich](https://en.wikipedia.org/wiki/Daniel_Yankelovich)
described a few years later:

> * The first step is to measure whatever can be easily measured. This
>   is OK as far as it goes.
>
> * The second step is to disregard that which can’t be easily
>   measured or to give it an arbitrary quantitative value. This is
>   artificial and misleading.
> 
> * The third step is to presume that what can’t be measured easily
>   really isn’t important. This is blindness.
> 
> * The fourth step is to say that what can’t be easily measured
>   really doesn’t exist. This is suicide.
>
> — Daniel Yankelovich, “Corporate Priorities: A continuing study of
> the new demands on business” (1972).

And it’s somewhat remarkable just how often businesses and
organizations fall into this trap, fifty years later. They might not
end up at step 4, but falling for step 2 or 3 is bad enough.


## An applied example

Let’s now turn to an example from our industry. Something that’s so
important, evidently, that it has given rise to a whole discipline in
our field: *site reliability.*

Now it’s perhaps a bit amusing that although you can find myriads of
articles describing what *site reliability engineering* (SRE) is, a
definition of “site reliability” lives only in a small footnote of the
[Google SRE Book](https://sre.google/sre-book/preface/#id-gA2u2Iyh4):

> For our purposes, reliability is “The probability that [a system]
> will perform a required function without failure under stated
> conditions for a stated period of time”.
>
> — Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Murphy, “Site
> Reliability Engineering: How Google Runs Production Systems”
> (2017)[^oconnor]

[^oconnor]: It should be noted that the SRE book is itself quoting a
	definition of reliability found in Patrick P. O’Connor & Andre
	Kleyner, “Practical Reliability Engineering” (2012).

But, at least there *is* a definition, which is good. Now I think it’s
reasonable to say that the following two statements *about* site
reliability are probably true:

1. In keeping with SRE reflecting a holistic approach to engineering,
   trying to unify a multitude of considerations, site reliability is
   not something we can judge by a single, numerical, universal, and
   useful metric. You can’t measure a single “site reliability score”,
   and then compare hundreds of platforms based on that.[^score]

2. Whatever site reliability *is* as a whole, it certainly *includes*
   a site’s ability to process your data and not mangle it. So, if you
   upload your data into a platform, you want to be able to do
   something useful with it.

[^score]: The irony is not lost on me that by the definition quoted in
    the SRE book, such a score absolutely *should* exist if its
    definition of reliability were adequate: it claims to be a
    probability. Probabilities go from 0 to 1. That would make site
    reliability a dimensionless quantity between 0 and 1, end of
    story. But it goes without saying that such a score would be “an
    arbitrary quantitative value”, which would put it on step 2 of the
    Yankelovich ladder.

SRE tends to rely on *[service level
indicators](https://sre.google/sre-book/service-level-objectives/#indicators-o8seIAcZ)*
(SLIs) to measure compliance with service level agreements (SLAs),
manage error budgets, and generally keep track of what shape the
site/platform is in.

So, let’s compare two indicators that differ greatly in their
measurability.

1. *Availability* is exceptionally easy to measure for, say, a REST
   API. You send a request with a defined payload, you measure the
   time it takes to serve your request, you check the status code, you
   check whether the response contains what you expect, and you record
   a data point.

2. *Durability* is *much* more difficult to measure at any given point
   in time. Effectively, to properly take a data point for durability
   at the same time as getting one for availability, you’d have to
   read back some data you wrote, say, a year ago, and check its
   content against something like a known hash.[^hash] *And also* write some
   data now, travel a year into the future, read it back at that
   point, travel back into the present,[^timetravel] and record your
   data point.

[^hash]: That hash would have to be separately stored *outside* the
    system. If the hash is stored *alongside* the data whose
    integrity it’s meant to protect, then it only guards against
    unintentional data corruption, but not against deliberate
    manipulation.

[^timetravel]: I wish to point out that the only bit that’s impossible
    here is the backwards time travel. The forwards time travel is
    fine, we all travel forwards in time all the time, just at a
    constant rate of one second per second.

Now before I continue I’d like to inject another thought to the issue
of data durability: not every platform is a storage solution. In other
words, you don’t always have the option of reading your data back
verbatim. Say for example you’re feeding an inordinate number of data
points into a platform that ingests and aggregates them. You may not
even be interested in the original data some months or years down the
road, so it might be acceptable (and even necessary, as dictated by
cost concerns) to discard the original data immediately after it has
been processed. And that rules out the possibility (or necessity) to
ever read it back exactly as it went in. But you *will* be interested
in the statistics that you generate based on the aggregated data.

And now suppose there is a subtle bug in the *implementation* of the
aggregation algorithm. As in, the algorithm itself is perfectly fine,
but there’s a flaw in the implementation. That, too, may render part
of your data unusable or outright invalid, violating data integrity
and durability.

But the tricky part here is that availability is easy to
measure. [Data durability
isn’t](https://www.theregister.com/2018/07/19/data_durability_statements/). Therefore,
availability lends itself to becoming a target (hello, Professor
Strathern), and durability tends to be seen as difficult to measure
and hence less important (hello, Secretary McNamara).

So now, if you find yourself in charge of a system that you *suspect*
has started to corrupt a significant fraction of customer data, data
which customers are pouring into it at an alarming rate, what do you
do?  You’re not sure whether there’s actual corruption yet. The proper
thing to do, if it’s impossible to rule out or fix the data corruption
problem immediately,[^immediately] is probably to stop intake, and
also ensure that no requests are served that may touch potentially
corrupted data — that is, shut the service down even before you’ve
ascertained corruption. But if you suspect that your next bonus payout
or promotion may rely on you meeting your availability goals, and you
know you’re already shaving it close with your availability error
budget, would you really be inclined to do that?

[^immediately]: I’ve run into a few issues of suspected silent data
    corruption in my career and I’ve *never* been in the situation
    where a reliable fix was available immediately.

## “You can’t manage what you don’t measure”

There’s a popular saying in management circles that takes one of the
following forms:

* “If you can’t measure it, you can’t manage it.”
* “You can’t manage what you don’t measure.”
* “You can’t manage what you *can’t* measure.”

Whichever variant you discuss, it is commonly attributed to either
Austrian-American management thinker [Peter
Drucker](https://en.wikipedia.org/wiki/Peter_Drucker), or to American
engineer and statistician [William Edwards
Deming](https://en.wikipedia.org/wiki/W._Edwards_Deming). Drucker is
seen by many as highly influential in management theory, Deming
developed groundbreaking sampling techniques used on the massive scale
of the United States census. So either of them would be an authority
on management and measurement, lending high credibility to the
statement. 

There’s just a small problem: neither of them appears to ever have
said or written anything to that effect.

The closest that [one of them, Deming, ever
wrote](https://deming.org/myth-if-you-cant-measure-it-you-cant-manage-it/)
was:

> It is wrong to suppose that if you can’t measure it, you can’t
> manage it — a costly myth.
>
> —  W. Edwards Deming, “The New Economics for Industry, Government,
> Education” (1993)

In case you didn’t notice, the point this makes is *the exact
opposite* of the popular version of the quote. It’s so wrong that it
comes close to the corruption of the
[Seneca](https://en.wikipedia.org/wiki/Seneca_the_Younger) lament, “non
vitæ sed scholæ discimus”, “we learn not for life but for school,” of
which you surely learned the inverse... in school.

Metrics-obsessed managers often take the misquote for gospel. So much
so that they frequently see issues where a qualitative approach is
obviously necessary, and they still try to apply quantification. 

My standard example for this are employee satisfaction surveys.

Ultimately, what leadership should be interested in learning from
those surveys is how good people feel about working in the
company. There are a number of factors that contribute to this: are
they overloaded, well utilized, or bored? Are people treating each
other with respect and kindness, or malice and contempt? Does everyone
feel that they are doing something meaningful, or do they all hate
their work and are solely in for the money? All these things are
inherently qualitative. And the company could do a great job by hiring
a person trained in sociology or psychology, who sits down with people
for confidential qualitative interviews, and then prepares a
research report with findings and recommendations that management can
act on.

But no, we have to measure. Make everyone take an online survey where
they rate everything on a scale of 1 to 5. Do you know what that is?
Exactly, step 2 on the Yankelovich ladder. Give that what can’t easily
be measured an arbitrary quantitative value — because that’s what it
is, arbitrary. People from different cultures won’t agree even on what
[a simple 5-step scale really
means](https://measuringu.com/scales-cultural-effects/).

And depending on *what* version of the faux quote they adhere to, a
manager may even be farther up the ladder:

* If they say “you can’t manage what you *don’t* measure” (with the
  translation being “I won’t concern myself with anything for which I
  don’t have quantitative data”): that’s step 3, blindness, that which
  isn’t measured isn’t important.
  
* If they insist that “you can’t manage what you *can’t* measure”
  (with the translation being “I won’t concern myself with anything
  that isn’t quantifiable”): that’s step 4 (suicide), that which isn’t
  measured doesn’t exist.

## So, what now?

Every article and book on bad metrics ends on a positive note, giving
you suggestions for “good” metrics: for example, make them hard to
game, make sure they are defined by competent experts, ensure that
they are in line with inherent ideas of respectability and
professionalism. Honestly, I’ve yet to come across a metric that ticks
all these boxes.[^game]

[^game]: In particular, pretty much any real-world metric fails the
    “hard to game” test. Said [Lukas Grossar on
    Twitter](https://twitter.com/lukasgrossar/status/1267830321057107969):
    “It always amazes me that people don’t believe that slapping a KPI
    onto something won’t lead to people gaming that KPI. We’re
    engineers for God sake, making broken stuff work in our favor is
    basically our job description.”

So, I am aware that if you are running a platform under an existing
SLA, you *will* be running under some metrics of questionable utility
that you cannot get rid of — just because they happen to be industry
standards.

However, instead of expanding metrics obsession to your entire
organization by introducing ever more counterproductive metrics, I
want to propose a different approach:

1. Whatever you measure, make the *marginal* cost of a measurement
   negligeable.[^marginal] The cost of adding a new metric should be
   practically zero. The moment someone has to repeatedly spend time
   on collecting and compiling the data, they can’t spend that time on
   doing productive work (and Campbell says hi), so you want to avoid
   that.

2. This effectively means that all the systems you care about
   (machines, services, applications) should generate collectable data
   points, everywhere, all the time.[^privacy] And you probably won’t be
   collecting metrics from anything else. In other words, you are
   *just* measuring that which is easily measurable, and you keep
   aware that there a lot of things you don’t measure that are just as
   important. You stay on step one of the Yankelovich ladder.

3. Now, I’d propose you make the data thus ingested available throughout
   your organization, in machine-readable form and using standardized
   APIs. You want people to actually *discover* things from your data.
   
4. Encourage people to use real, scientific, statistical methods to
   figure out statistical regularities (“indicators”). Offer
   statistics training to people who are interested.

5. Once someone identifies a statistical regularity, encourage them to
   form an opinion of whether it would be beneficial for it to go up
   or down, formulate a hypothesis on what change to your system would
   have the desired effect, and conduct an experiment. If the
   experiment has no effect, roll back the change and proceed with the
   next hypothesis. If it has an adverse effect, roll back and try the
   opposite. If it has the desired effect, keep the change. Move on to
   discovering the next regularity. Resist the urge to make the
   discovery a target. (Otherwise, Strathern will drop
   by.)

6. Constantly observe and identify things that are important, but not
   measurable. Apply qualitative analysis, emotion, and
   empathy. (Otherwise, McNamara will introduce himself.)

[^privacy]: I’d argue that this requires strong privacy guarantees for
    your users/customers. Effectively, just don’t collect data that’s
    none of your business.

[^marginal]: Emphasis on marginal. It’s obvious that the *fixed*
    cost of building and maintaining an instrumentation platform and
    metric system is nonzero. But once you’ve got it set up, the cost
    of *adding a new metric* should be substantially zero.

So, is there anything inherently wrong with measuring or measurements?
Nope. But making them targets, introducing arbitrary quantifiers, and
ignoring everything else is.
