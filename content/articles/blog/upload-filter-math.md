Title: Why upload filters don’t work (really simple math!)
Date: 2019-03-25T20:00:00-00:00
Slug: upload-filter-math
Tags: Politics

“I can’t figure out how upload filters should work, but I’m not a
technical person — surely someone who is can sort it out!”

That is a misconception. I’ll be happy to explain, requiring — I
promise! — no technical understanding of what an upload filter is, or
how it works.

<!--break-->

The current draft of the EU Directive “on copyright and related
rights in the Digital Single Market”, available
[here](http://www.europarl.europa.eu/doceo/document/A-8-2018-0245-AM-271-271_EN.pdf),
(PDF in English), also known as [the **EU Copyright
Directive**](https://en.wikipedia.org/wiki/Directive_on_Copyright_in_the_Digital_Single_Market),
requires in its Article 17 (formerly Article 13), clause 4, that the
service provider undergoes,

> in accordance with high industry standards of professional
> diligence, best efforts to ensure the unavailability of specific
> works and other subject matter for which the rightholders have
> provided the service providers with the relevant and necessary
> information.

It is obvious that the only way any platform hosting
user-generated content would thus have to intercept any such content
_on upload,_ failing which it would immediately become potentially liable for a
copyright violation. This would require a technical facility commonly
called an _upload filter._

## We don't need to talk about how upload filters _work_

Now, an upload filter is immensely complex and there are tons of
technical difficulties — the only time this has been attempted on a
large scale is YouTube’s [Content
ID](https://en.wikipedia.org/wiki/Content_ID_(algorithm)), and it is
exceedingly unreliable and prone to overblocking. But for the purposes
of this discussion, it doesn’t matter whether implementing an upload
filter is difficult to do.[^1]

Assume for a moment someone has built a magnificent upload
filter. Something that operates on magic pixie dust that catches *all*
copyright violations.

## Interactions

Now, let’s call every instance of someone uploading content to the
internet an “interaction”. Every tweet, every Facebook post and
comment, every comment on your favorite news site, every blog post you
write, every picture that you take and post to a WhatsApp group of 50
people or more, every YouTube video and comment — let’s call all of
those “interactions.”

And let’s make an outrageously overblown assumption: suppose that on
the internet today, 1% of such interactions infringe someone’s
copyright. Again, let me reiterate that this is ludicrously high. The vast
majority of internet interactions today are either completely trivial
and thus irrelevant to copyright, or works of your own, or a perfectly
legal fair-use way of using someone else’s work, such as when you
quote a passage of a book. But purely for the sake of this discussion,
let’s say it’s 1%.

So then let’s look at 10,000 interactions that completely random
people make on the internet.

Those would then break down like so:

|                      | Total
| -------------------- | ------
| Perfectly legal      | 9,900
| Infringing copyright | 100


## Catching copyright violations. Or non-violations.

OK. Now, suppose we built a *perfect* upload filter, i.e. one that
catches *all* copyright infringements. Remember, the Directive calls
for “best effort to ensure the **unavailability**” (emphasis mine) of
potentially infringing content. It does not allow providers to balance
for freedom of expression or the like, so to err on the side of
caution, they must strive to over- rather than underblock. So a
perfect filter is one that has **no false negatives** — meaning if
content infringes, it is always caught.

Now, suppose further that the filter mis-identifies content (meaning,
flags content as infringing when it is not) with a rate of only
2%. That means it has **2% false positives.** That, now, is
ridiculously low for any automated screening procedure.[^2]

So that means that out of our 10,000 interactions tracked by our
“perfect” content filter, the numbers break down like this:

|                    | Total  | Flagged as legal | Flagged as infringing
-------------------- | ------ | ---------------- | ---------------------
Perfectly legal      | 9,900  | 9,802            | 198 
Infringing copyright | 100    | 0                | 100
**Overall**          | 10,000 | 9,802            | 298


## Congratulations, a coin toss beats your upload filter.

That leads us to the question: if you upload something and it gets
flagged, how likely is it that it is *actually* infringing any
copyright? Answer: 100 in 298. Roughly one in three. **Yes, that is
worse than a coin toss.** And remember, this is assuming an
implausibly high rate of infringements overall, and a ludicrously low
false-positive and false-negative rate on your filter.

Go ahead and play with the numbers, tweak the false-negatives and
false-positives, whatever. **As long as what you’re looking for is
exceedingly rare, automated filters detect it with poor accuracy.**

And if you leave all parameters the same, but consider a probably much
more realistic infringement rate of 1 in 1000, that is, 0.1%, then
things look like this: 

|                    | Total  | Flagged as legal | Flagged as infringing
-------------------- | ------ | ---------------- | ---------------------
Perfectly legal      | 9,990  | 9,800            | 200 
Infringing copyright | 10     | 0                | 10
**Overall**          | 10,000 | 9,800            | 300

Now there’s a one-in-thirty chance that an upload block is
legitimate. Assuming there is an appeals process, and all false
positives get appealed, then that means the **human** going through
the appeals will have to undo a block **29 times out of 30.** 

## A cheap optimization

I’d like to propose an optimization here: any website seeking to
implement a content filter should consider to just use a **random
number generator to reject your upload, comment, tweet, or post with a
certain probability that is demonstrably larger than that of an upload
filter.** I’d posit that that would be by far the safest, cheapest way
to comply with the directive — if it becomes law.

Of course, everyone who is now in favor of this directive (including
its Article 17) will hate that.

* * *

## Footnotes

[^1]: It’s also easy to dismiss with a “try harder”
	retort, which is completely disingenuous, because it’s akin to
	saying, doc, this patient has terminal pancreatic cancer, but you
	*must* cure her. Inoperable? Terminal? No there’s *got* to be a
	way. Sometimes there is no way, and it’s OK when an expert tells
	you that.

[^2]: I don’t believe YouTube releases numbers on its ContentID error
	rate, but it’s apparently [pretty
	bad](https://www.techdirt.com/articles/20181214/17272041233/youtubes-100-million-upload-filter-failures-demonstrate-what-disaster-article-13-will-be-internet.shtml)
	for a system that cost $100M to build.
