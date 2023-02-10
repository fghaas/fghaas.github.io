Title: Brown M&Ms, UTC, and ISO 8601
Date: 2023-02-10 19:00
Slug: brown-mms
Tags: Work
Summary: What have brown M&Ms got to do with date/time formats and mutual respect? More than you might think.

The Van Halen "brown M&Ms" story is a classic tale of rock'n'roll lore.
In 1982, Van Halen had a famous [concert rider](https://www.thesmokinggun.com/documents/crime/van-halens-legendary-mms-rider) that included a requirement that was patently ludicrous at face value:
backstage, the catering at a Van Halen show had to provide bowls of M&Ms chocolate candies --- *with all the brown ones removed.*
That's right, there had to be M&Ms, but if there was a single brown one to be found, this would constitute a breach of contract on the promoter's part.

This example is frequently trotted out as an example of crazy rock stardom.
Clearly, this was an episode of fame getting to the heads of a group of kids that had suddenly hit the big time.
Or was it?

David Lee Roth, the then-singer of Van Halen, explained the reason behind the "no brown M&Ms" rule [in an interview](https://youtu.be/_IxqdAgNJck) nearly 30 years later.

In 1982, the Van Halen show was one of the biggest acts on the North American tour circuit.
Their stage lighting rigs would look positively tame by modern standards, but at the time very few acts were touring with equipment that was as power-hungry as Van Halen's.
(Consider that at the time it wasn't uncommon for bands to just play under the venue's house lights, rather than travelling with several truckloads of stage equipment as big acts commonly do today.)

So the band put together very stringent electrical wiring and power distribution requirements in their promotion contract.
Their rider would specify the density and spacing between outlets, amperage requirements, and fuse ratings.
(Clearly, Van Halen had a vested interest in *not* blowing a fuse or tripping a circuit breaker mid-show, and in keeping their crew safe from electrocution by improper grounding.)
This amounted to quite a compendium of documentation, and right in the middle of that binder they slipped a page specifying the catering requirements --- including the now-famous "no brown M&Ms" rule.
Its purpose was simply to check on whether the promoter had thoroughly read the contract.

Thus, if a band member or roadie walked into the backstage area shortly before sound check, and they found brown M&Ms, it stood to reason that the promoter hadn't been paying close attention to that part of the contract.
And *that* meant that they couldn't rule out that the promoter had been sloppy with the power specs, too.
So they would do a full line check to make sure that the equipment held up.

Allow me to change the subject.

I wrote the communication guidelines for my team.
Eventually, since the company I work for hadn't any such thing, they basically adopted large parts of what I wrote and made it company policy.

Two of the things that made it into the company policy, and are still standing rules on my team --- and will remain so, as long as I run it --- are these:

* Always use the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) `YYYY-MM-DD` format for any dates you specify.
* Always use [UTC](https://en.wikipedia.org/wiki/Coordinated_Universal_Time) for any time information you communicate. (Adding conversions to local timezones is OK, but not required --- and UTC must always come first.)

People have called me silly and nitpicky for insisting on these things. But they serve a purpose.

You see, I work in an international team.
I am from Austria and I would *not* specify today's date as 2023-02-10 in regular written communications.
I would put 10.2.2023.
Someone who lives in Spain would use 10/2/2023.
Someone from India would put 10-02-2023.
And someone from the U.S. would write 2/10/2023 (as you can see this creates some difficulty establishing, unambiguously, whether we are talking about the 10th day of February, or the 2nd day of October).

The fact that we agree on an internationally unambiguous format that *none* of us would use natively simply means that we all *slightly* go out of our way, in order to make things easier for everyone.
That is a hallmark of respectful behavior: if everyone accepts a *slight* inconvenience for themselves, we all act more fairly to each other.

The same goes for giving times in UTC: very few people (on a global scale) live "on UTC": there is just a handful of countries[^utc-0-countries] that are in the UTC±0 timezone and never observe daylight saving time.
Their combined population is about 140 million people, less than 2% of the world's total.
Everyone else lives in a timezone other than UTC at least for half of the year.

[^utc-0-countries]: Burkina Faso, Côte d'Ivoire, Gambia, Ghana, Guinea, Guinea-Bissau, Liberia, Mali, Mauritania, São Tomé and Príncipe, Senegal, Sierra Leone, and Togo.

This means if you're one of *most* people, coordinating times in UTC means having to do a little bit of mental calculation for yourself: you know which side of Greenwich you're on, and how far removed, and whether or not it's summer and whether or not your area observes daylight saving time.
Everyone else is in the same boat.
You go a little out of your way, I go a little out of mine, we respect each other, we get along.

It's been a little while since I wrote those guidelines.
"Use ISO 8601" and "use UTC" are my "no brown M&Ms" rules.
And like the removal of brown M&Ms were a proxy variable for diligent contract reading, my date/time rules have turned out to be proxy variables for respect.

There are some people who just assume that these simple rules are not for them, and that surely everyone else can adapt so they don't have to.
I grow progressively more skeptical of those people.

