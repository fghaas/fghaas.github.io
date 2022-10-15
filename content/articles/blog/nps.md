Title: Nebulous Percentage Shenanigans
Date: 2022-10-15 15:00
Tags: Work, Communications
Slug: nps
Summary: I recently learned that I am a "detractor" of things I actually quite like. Here are a few related things I also learned about in the process.

Surely you've seen a question similar to the following in a survey or
request for feedback.

> How likely is it that you'll recommend X to a colleague or friend?

In this question, X is either a product or service, or a brand, or
*all* of a company's products or services. Answers are given on a
scale of 0 to 10, with 0 being "not at all likely" and 10 being
"extremely likely". It is frequently the last question in a survey,
or even the only one.

The reason this question is so frequent is that it drives a metric
that is popular with marketingfolk and management: the [net promoter
score](https://en.wikipedia.org/wiki/Net_promoter_score), or NPS.

To work out the NPS, what you do is deduct the percentage of
"detractors" of your product from that of the "promoters". If the net
result is above zero, per the lore, you are generally doing well. If
you hit above 30, your product or service or brand or company is
allegedly performing excellently.

## What's a promoter? What's a detractor?

Now, what defines your promoters and detractors, according to the NPS
metric? Clearly we'll have to slot the possible responses into
categories.

And here's where you'll notice something peculiar about the scale. It
consists of discrete values going from 0 to 10 inclusive, not from 0
to 9 or 1 to 10. That means it's an 11-point scale. What do we notice
about the number 11?  Exactly, it's prime. It's thus impossible to
sort the scale items into evenly sized categories, no matter how many
or few.

But okay, let's say it's not a law that the categories need to be
evenly sized. So you might think that answering anything from 0 to 3
makes someone a "detractor", and anything between 7 and 10 a
"promoter", with the middle ground (4 to 6) being somewhat neutral.

But that's not what NPS uses. The actual NPS scale looks like this:

* 0 to 6: detractor
* 7 to 8: "passive"
* 9 to 10: promoter

Now, recall that NPS ignores the "passive" respondents altogether, and
only looks at the percentage of "promoters" minus that of
"detractors". If a majority of respondents answer 7 or 8 (intuitively
a solidly positive score, if you ask me), those do not factor into the
result at all. Only being inclined to *rather enthusiasically*
recommend a product or service makes you a promoter. And answering 6,
clearly north of the scale's middle mark, makes you a detractor.

Obviously, this oddly warped scale in combination with ignoring part
of the sample altogether makes the deduction of one percentage from
another rather agony-inducing for any secondary school maths
teacher. That's eminently not how these things work; on its face it's
one of those results that Wolfgang Pauli [would have
called](https://en.wikiquote.org/wiki/Wolfgang_Pauli) "not only not
right, but not even wrong."

## Would you recommend a rental car company to someone who doesn't need a rental car?

But in addition to a warped scale and off-label use of percentages,
NPS also uses an inherently biased premise.

Suppose I rent a car from a fictitious company we'll call My Local
Public Transit Sucks, or MyLoPTS. And after I return my vehicle, I am
asked how likely I am to recommend renting a car from MyLoPTS to "a
friend," which I would presume to mean any randomly selected one of my
friends.

Now I would not recommend *any* rental car company to someone I know
to not be in need of a rental car. And I would assume that a *maximum*
of 10% of my friends, acquaintances, and colleagues are in need of a
rental car at any one time (considering that *my* locally available
public transport very much does *not* suck, so the demand for rental
cars is quite low). So even if I was *certain* to recommend MyLoPTS to
anyone *needing* a rental car, the correct answer for the question as
asked --- the likelihood of recommending MyLoPTS to *a friend,*
regardless of circumstances --- on a scale of 1 to 10 would be 1. My
answer to the question as stated thus has little to no relation to how
happy I am with MyLoPTS' service.

So, it's a misguided question with a warped scale that makes implicit
assumptions and then does creative maths with the result. Why do so
many people believe that this makes any sense?

## Greetings from Harvard

The answer, apparently, is in [a single article in the Harvard
Business
Review](https://hbr.org/2003/12/the-one-number-you-need-to-grow). That
article will be old enough to drink in two years' time in its USian
habitat, so whether its 2003 findings are still valid in 2022 is
debatable. But let's assume for the time being that they are.

On the subject of the scale in question, here's a quote from that
article:

> [We] settled on a scale where ten means “extremely likely” to
> recommend, five means neutral, and zero means “not at all likely.”
> When we examined customer referral and repurchase behaviors along
> this scale, we found three logical clusters. “Promoters,” the
> customers with the highest rates of repurchase and referral, gave
> ratings of nine or ten to the question. The “passively satisfied”
> logged a seven or an eight, and “detractors” scored from zero to
> six.
>
> --- Frederick F. Reichheld, [The One Number You Need to
> Grow](https://hbr.org/2003/12/the-one-number-you-need-to-grow),
> Harvard Business Review (2003)

So, this confirms that the scale itself isn't meant to be warped by
default. Anything under 5 means unlikely to recommend, 5 is neutral,
and anything above 5 is likely to recommend. (Since the respondents
would presumably be required to select discrete values, that fact
still warps the scale and places the "neutral" value off-centre ---
but let's assume the creators of the scale did think of it as a
continuum, which does not have this problem.)

Rather than being baked into the scale from the get-go, the
categorization into "promoters" comes from an actual correlation of
responses to repurchase and referral behavior.  Or at least the
article claims so --- the research data it's based on does not appear
to be publicly available. We can only assume that similar correlations
with actual customer behavior were drawn for the "passively satisfied"
and "detractor" categories, though I am not quite sure how they would
have identified the former, separating them from promoters. I suppose
a "passively satisfied" person could perhaps have been one that did
come back to make another purchase, but never made a referral? It
would be interesting to see how they tracked that in 2003.

At any rate, the HBR article then asserts that NPS was a predictor of
company growth when comparing to its competition: in other words, that
companies with a higher NPS than their competitors also experienced
higher revenue growth than them --- across multiple industries (the
article specifically mentions airlines, ISPs, and rental car
companies).

The article also says this:

> The “would recommend” question wasn’t the best predictor of growth
> in every case. In a few situations, it was simply irrelevant. In
> database software or computer systems, for instance, senior
> executives select vendors, and top managers typically didn’t appear
> on the public e-mail lists we used to sample customers. Asking users
> of the system whether they would recommend the system to a friend or
> colleague seemed a little abstract, as they had no choice in the
> matter. [...]
>
> Not surprisingly, “would recommend” also didn’t
> predict relative growth in industries dominated by monopolies and
> near monopolies, where consumers have little choice. For example, in
> the local telephone and cable TV businesses, population growth and
> economic expansion in the region determine growth rates, not how
> well customers are treated by their suppliers.
>
> --- Frederick F. Reichheld, [The One Number You Need to
> Grow](https://hbr.org/2003/12/the-one-number-you-need-to-grow),
> Harvard Business Review (2003)

That sounds quite reasonable. Obviously, recommending a product to a
friend or colleague doesn't help the company selling it, if the friend
or colleague has no say in the purchase decision.

## Cultural bias, and Goodhart et al.

But there's another thing that the article *doesn't* say, apparently
because it's obviously implied: all companies covered in the research,
and presumably the vast majority of the customers surveyed, were from
the United States.

[It's rather well
understood](https://measuringu.com/scales-cultural-effects/) that
scales are read differently by people from different cultures. So
while the correlation of a certain response score with a certain
behaviour is likely to work fine when you're surveying U.S. customers
of U.S. companies, it's likely to fall apart when you're trying to
make similar predictions from answers from non-U.S. respondents, or
to compare responses internationally.

Note further that the article describes NPS as a *predictor* of
growth, meaning *the underlying conditions* that cause a company to
have a high NPS *also* give it a competitive advantage and thus
facilitate growth. Trying to tweak the measure itself --- for example,
by [coaching
people](https://twitter.com/larsmb/status/1579137943750385665) to
respond 9 or 10 when they would intuitively select 7 or 8 --- is a
great example of collapsing a statistical regularity by placing
pressure on it for control purposes, i.e. [Goodhart's
Law]({filename}meaningless-metrics-treacherous-targets.md).

And, of course, NPS is subject to [Campbell's
Law]({filename}meaningless-metrics-treacherous-targets.md) as much as
any other metric. When a score becomes the goal of a process, it both
loses its value as an indicator, and distorts the process itself in
undesirable ways. You could argue that this effect of NPS is a
regrettable, but natural aftereffect of its enduring popularity over
nearly 20 years --- but no, *it's right there in the same HBR
article:*

> Branch scores were not improving quickly enough, and a big gap
> continued to separate the worst- and best-performing regions. [...]
> So the management team decided that field managers would not be
> eligible for promotion unless their branch or group of branches
> matched or exceeded the company’s average scores. That’s a pretty
> radical idea when you think about it: giving customers, in effect,
> veto power over managerial pay raises and promotions.
>
> --- Frederick F. Reichheld, [The One Number You Need to
> Grow](https://hbr.org/2003/12/the-one-number-you-need-to-grow),
> Harvard Business Review (2003)

"Radical" strikes me as a rather charitable assessment for what
Goodhart and Campbell (and [Marilyn
Strathern](https://en.wikipedia.org/wiki/Marilyn_Strathern)) would
call completely messing up the measure, by making it a career-defining
target.

## In summary

NPS strikes me as Not Particularly Sensible.

* * *

### Further reading

These are provided for additional reference only; I do not necessarily
agree with all their findings and suggestions.

* Kim Witten, [10 reasons why NPS is BS (and what you can do about
  it)](https://uxdesign.cc/this-popular-business-metric-is-hurting-you-55ed535e9a59)
  (2022)
* Khadeeja Safdar and Inti Pacheco, [The Dubious Management Fad
  Sweeping Corporate
  America](https://www.wsj.com/articles/the-dubious-management-fad-sweeping-corporate-america-11557932084)
  (Wall Street Journal, 2019) (paywalled)
* Ron Shevlin, [It's Time To Retire The Net Promoter Score (And Here's
  What To Replace It
  With)](https://www.forbes.com/sites/ronshevlin/2019/05/21/its-time-to-retire-the-net-promoter-score/)
  (Forbes, 2019)
* Jared Spool, [Net Promoter Score Considered Harmful (and What UX
  Professionals Can Do About
  It)](https://articles.uie.com/net-promoter-score-considered-harmful-and-what-ux-professionals-can-do-about-it/)
  (2017)

I should mention that I particularly disagree with the notion of
"replacing" the NPS with something else. See [my thoughts on
metrics]({filename}meaningless-metrics-treacherous-targets.md) for
background.