Title: No, We Won’t Have a Video Call for That!
Date: 2020-08-22
Tags: Conference, Communications, Work
Series: No, We Won’t Have a Video Call for That!
Series_index: 0
Summary: Communications in distributed teams: a write-up of my talk from FrOSCon 2020, Cloud Edition.

FrOSCon 2020 was an online event due to the COVID-19 pandemic, and
gave me the opportunity to present an extended and heavily updated
version of my [DevOpsDays 2019]({filename}devopsdaystlv-2019.md) talk.

* * *

I normally make my talks available as a video, and a slide deck with
full speaker notes. In this case though, I consider it fitting to
write the whole thing out, so that you *don’t* need to watch a full
length video in 45 minutes, but can read the whole thing in 15.

You’ll still find links to the recording and deck downpage, as usual.

* * *

No, we won’t have a video call for that!

Communications for distributed teams

FrOSCon 2020

<!-- Note --> 
This presentation is a talk presented at [FrOSCon 2020
Cloud Edition](https://www.froscon.de/). It is [CC-BY-SA
4.0](https://creativecommons.org/licenses/by-sa/4.0/) licensed, see
[the license](/LICENSE) for details.

Hello and welcome, dear FrOScon people — this is my talk on
communications in distributed teams. My name is Florian, this is the
second time I‘m speaking at FrOScon, and you probably want to know
what the hell qualifies me to talk about this specific issue. So:


### Why am I talking here?

So, why am I talking about **that**?

Or rather more precisely, why am **I** talking about that?

I turned 40 last year, have been in IT for about 20 years now (19
full-time), and out of that I have worked

* in 4 successive companies, all of which worked out of offices,
  for 11 years, 

* in a completely distributed company, that I founded, for 6 years,

* and now, for about three years, I have been running a distributed
  team that is a business unit of a company that has existed for 15
  years and throughout that time, has only ever worked from a single
  office.

So I think I might have seen and become aware of some of the rather
interesting challenges that come with this.


### What changed since last time?

I originally wrote and presented this talk for the first time in
December 2019. At the time, you probably had forgotten about SARS, had
no idea what SARS-CoV2 or COVID-19 were, and many of you were probably
working from offices.

And then something like three months later, everything changed and
suddenly, this talk became much more relevant to a much greater
audience.

And something else happened: a lot of people suddenly started talking
about working from home and distributed teams, and a lot of those
people who were talking very loudly, had themselves only been working
with or managing distributed teams since March. And a fair amount of
what you could about the subject then, and can still read now, is
complete and utter bullshit.

So there’s one point I actually *didn’t* make in the initial version
of this talk, because I thought it was self-evident. But I have come
to the conclusion that to a lot of people it is not, so to rectify
this omission from last December — and with apologies for that
omission to the wonderful DevOpsDays Tel Aviv crowd, who were my first
audience for this talk, let me make this one thing very clear from the
outset:

> Effective distributed collaboration is **not** pretending to be in
> an office while staring into a webcam all day.

You will never be able to capitalize on work as a distributed team
unless you kick some office habits. The key to distributed teams being
effective is **not** that they happen to not be in the same place, as
you’ll see from the remainder of this talk. So to expect success from
the approach that you take the habits of an office, simply remove the
element of locality, replace every face to face meeting with a video
call and carry on, is ludicrous.

The good news is that if you do it right, you’ll end up with a far
better team than a local one would ever be, *and* everyone has a
chance at far better work-life balance, *and* you don’t waste awful
amounts of time and energy and fossil fuels on your commute.


### What’s in this talk?

So you’ll find a few general themes throughout this talk:

* What modes we have *available* for communications in teams;

* Why distributed teams always collaborate *asynchronously,* and what
  communication modes lend themselves to that particularly well;
  
* Why *written communication* is so important in distributed teams;

* And why *meetings* (like video calls) are a mode of communication
  that effective distributed teams hardly ever need to use — except
  for very specific reasons.

But I do want to state one thing upfront:

> This is _not science._

Nothing of what I am talking about is steeped in any scientific
rigour. I present anecdotes, not evidence. I might be mistaking
correlation for causation, or the other way round. It’s solely based
on my personal experience, and the experience of others I have talked
to, watched, or read. Everything I say here is subject to debate and
rebuttal, or you can simply have a different opinion.

But it’s definitely **not** science.

Now with all of that said, let me attempt to give a definition of a
distributed team, according to my understanding:

A distributed team is a **professional** group whose members do not
rely on proximity in order to **routinely** collaborate
productively.

Now this is clearly not an ideal definition, not least because it
defines something by a negative, and an outside factor to boot: it
defines a distributed team by what it *does not need* to exist to
function. But it’s the best definition I’ve been able to come up with.

Now there’s a couple of key words in here:

* **Professional.** I’m talking about teams that work towards a
  professional goal. This doesn’t necessarily mean that they all work
  in the same company. They could, for example, all work in different
  companies collaborating on a joint project, which is what frequently
  happens in open source software projects. But they’re not pursuing
  their hobby, they’re doing their jobs.

* **Routinely.** I’m talking about teams that *habitually* work in a
  distributed fashion, not the work that goes on in an office-based
  team when one person is having a work-from-home day.

It is important to understand that that lack of proximity is not only
spatial, it is temporal as well, because:


> Working in a distributed team means **working asynchronously.**

If your team is distributed, this is equivalent to saying that it
works in an asynchronous fashion, that is to say, that people will
work on things in parallel, and a capable distributed team will have
just as few synchronization points as absolutely necessary.

The reason for this is not just working in different timezones, but
also the fact that everyone will have their own daily routine, and/or
have their individual times when they are most productive. Which you
*will not attempt to synchronize.* (Doing so would mean setting the
entire team up for failure.)

Now, this doesn’t come for free, nor does it fall in our lap:

> Being productive in a distributed team is a skill
> that most people must **learn;** it is not innate to us.

People are not born with the ability to work in a distributed
team. Humans function best in groups that collaborate in close
proximity to one another; it is only very recently that technology has
started to enable us to override that to an extent — giving us other
benefits like the ability to work from home, or the ability to hire
people residing anywhere, provided they have internet connectivity.

So we now *can* work in teams despite being continental distances away
from each other but we do have to acquire the skills to do that. And
if we fail to do so, that has a rather grave disadvantage, which is
that...

> **Nothing** has as dire an impact on productivity as **poor
> communications.**

This is a truism that applies to both distributed and non-distributed
teams. Having bad communications will wreck any project, blow any
budget, fail any objective. Now note that the reverse is *not true:*
having *good* communications does not guarantee success. But having
bad communications does guarantee failure.

And here is one thing to start with:

> A capable distributed team **habitually externalises** information.

Information is generally far less useful when it is only stored in one
person’s head, as opposed to being accessible in a shared system that
everyone trusts and can use. If you take important information out of
your own head and store it in a medium that allows others to easily
find and contextualise it, that’s a win for everyone.

And since we’re all technology people, we typically have multiple
facilities to externalise, share, and then access information at our
disposal. So let’s see how those compare.

## Modes of communication in distributed teams

A distributed team will habitually use multiple modes of
communication, relying mostly on those that make sharing, finding, and
contextualising information easy, and avoiding those that make it
difficult.

In many teams, distributed or not, using chat as a default mode of
communication is becoming the norm. Now with an important exception,
which I’ll get to near the end of the talk, this is **not** a symptom
of having a particularly dynamic or efficient team; it’s the opposite.


> Excessively using chat isn’t being efficient.
> It’s being lazy.

It’s a symptom of the worst kind of laziness _(not malice!)_: in an
attempt to communicate quickly and easily, for yourself, you are really
making things harder for everyone, including yourself.


|               | Share | Find | Contextualise |
| -----------   | :---: | :--: |               |
| Chat          | 🙂    | 😐   | 🙁            |

This is because, while *sharing* information in a chat is extremely
easy, it is also a “fire and forget” mode of communications. Chat
makes it difficult to find information after the fact. If you’ve ever
attempted to scour a busy Slack or IRC archive for a discussion on a
specific topic that you only remember to have happened a “few months
ago”, you’ll agree with me here.

It’s even *more* difficult to read a Slack discussion in context, that
is to say in relation to *other* discussions on the same topic, days
or weeks earlier or later.

Let’s compare that to other communication modes:

|               | Share | Find | Contextualise |
| -----------   | :---: | :--: |               |
| Chat          | 🙂    | 😐   | 🙁            |
| Email         | 😐    | 😐   | 😐            |


* Email makes it easy to share information with a person or a group
  from the get-go, but quite difficult to loop people into an ongoing
  discussion after the fact. Finding information later is just as hard
  as with chat, and it’s marginally better at contextualizing
  information than chat (because you get proper threading).


|               | Share | Find | Contextualise |
| -----------   | :---: | :--: |               |
| Chat          | 🙂    | 😐   | 🙁            |
| Email         | 😐    | 😐   | 😐            |
| Wiki          | 🙂    | 🙂   | 🙂            |
| Issue tracker | 🙂    | 🙂   | 🙂            |

* A wiki and an issue tracker (provided you don’t lock them down with
  silly view permissions), in contrast, both make it *very* easy to
  share, find, **and** contextualise information.  
  Note that “wiki”, in this context, is shorthand for any facility
  that allows you to collaboratively edit long-form documents
  online. That can be an actual wiki like a MediaWiki, but also
  something like Confluence, or even shared Google Docs.  
  Likewise, “issue tracker” can mean RT, OTRS, Jira, Taiga, Bugzilla,
  whatever works for you.


|               | Share | Find | Contextualise |
| -----------   | :---: | :--: |               |
| Chat          | 🙂    | 😐   | 🙁            |
| Email         | 😐    | 😐   | 😐            |
| Wiki          | 🙂    | 🙂   | 🙂            |
| Issue tracker | 🙂    | 🙂   | 🙂            |
| Video call    | 😐    | 🙁   | 🙁            |

* Video calls are even worse than chat or email, because sharing
  information works but doesn’t scale — you can’t reasonably have more
  than 5-or-so people in a video call, and sharing the recording of a
  full video call is just pointless.

So really, make your wiki and your issue tracker your default mode of
communications, and use the others sparingly. (This isn’t meant to be
a euphemism for “don’t use them”, as we’ll get to in a moment.)


## Text chat

So. Let’s talk about text chat. These days, that frequently means
[Slack](https://slack.com/), but what I am talking about also and
equally applies to
[IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat),
[Mattermost](https://mattermost.com/), [Riot](https://riot.im/), and 
anything similar.

Is text chat universally useful? No. Is it universally bad? Not that,
either. There is a very specific type of situation in which text chat
is a good thing:


> Use **chat** for collaboration that requires **immediate,
> interactive mutual feedback.**

Using interactive chat is a good idea for the kind of communication
that requires immediate, interactive mutual feedback from two or more
participants. If that is not the case, chat is not a good idea.

This means that the only thing that chat is good for is communication
that is required to be *synchronous,* and remember, in a distributed
team *asychronicity* is the norm. So using interactive chat for
communications needs to be an *exceptional* event for a distributed
team; if it is instead a regular occurrence you’ll make everyone on
the team miserable.

For any interaction that does *not* require feedback that is *both*
immediate and interactive, email, a wiki, or an issue tracker are *far
superior* modes of communication.


> The only reason to use **DMs** for collaboration  
> is a need for immediate, interactive mutual feedback  
> **and confidentiality.**

Using chat direct messages (DMs) as the *default* means of
communication is utterly braindead. In order for a chat DM to be
useful, there is precisely one clearly delineated confluence of events
that must occur:

* You need immediate feedback from the other person,
* you need mutual back-and-forth with the other person,
* you don’t want others to follow the conversation.

I can’t emphasize enough that this combination is perfectly valid —
but it is *exceedingly rare.* If you want just a private exchange of
ideas with someone, encrypted email will do. If you want to work on
something together with one person before you share it with others,
restricted view permissions on a wiki page or an issue tracker ticket
will work just fine.

If you don’t need confidentiality but you do need interactive and
immediate feedback, chances are that you’re working on something
urgent, and it is far more likely you’ll eventually need to poll other
opinions, than that you won’t. So just use a shared channel from the
get-go, that way it’s easier for others to follow the conversation if
needed — and they might be able to point out an incorrect assumption
that one of you has, before you end up chasing a red herring.

> A chat ping is a shoulder tap.

“Pinging” someone in a chat (that is, mentioning their username, which
usually triggers a visual or auditory notification), is exactly like
walking up to a person, interrupting what they are doing, tapping them
on the shoulder, and asking them a question.

**No matter whether it is your intention or not,** they will feel
compelled to answer, relatively promptly (the only exception is when
you’ve done this so often that you have conditioned your colleagues
to ignore you — congratulations).

This means that you’ve broken their train of thought, yanked them out
of a potentially complex task, forced them to redo what they did
pre-interruption, or actually have them commit a mistake.

So pinging someone in a chat is something you should only do if you
are aware of exactly this risk, *and* you are convinced that whatever
you’re pinging about is more important. Otherwise, to be very blunt,
you’ll be seen as the asshole.


> Want people to hate you? Send naked pings.

A “naked ping” is the action of sending someone a message consisting
only of their username and a marker like “ping”, “hi”, “hey” or
similar.

```
14:00:02Z johndoe: florian: ping
[...]
15:56:17Z florian: johndoe: I hate you
```
Don’t. Just don’t.

Any person who is versed in the use of chat communications will, when
subjected to this behavior, be inclined to flay you alive. Infinitely
more so if it’s a DM. **Do not do this.**

Instead, always provide context. Always always always. Don’t say “can
I ask you a question, instead, *ask the question.* If something isn’t
urgent, say something like “no urgency.”

```
14:00:02Z johndoe: florian: can I get your eyes on PR #1422?
[...]
15:56:17Z florian: johndoe: done! 
                   (was afk for a bit – sick kiddo)
15:56:58Z johndoe: florian: np, ty
```

It should be self-evident why this is better than naked pings, but if
to you it is not, then please read [Naked
Pings](https://blogs.gnome.org/markmc/2014/02/20/naked-pings/),
courtesy of Adam Jackson and Mark McLoughlin.

## Video calls

(Zoom, Hangouts, BlueJeans etc.)

Next, I’d like to talk about video calls. Doesn’t matter what
technology you’re using. Could be Zoom, Google Hangouts, BlueJeans,
Jitsi, whatever.

And I’d like to address this specifically, given the fact that in the
current pandemic the use of video calls appears to have skyrocketed.

There’s a very good reason to use video calls: they give you the
ability to pick up on nontextual and nonverbal cues from the call
participants. But that’s really the only good reason to use them.

Video calls have a significant drawback: until we get reliable
automatic speech recognition and transcription, they are only
half-on-the-record. Hardly anyone goes to the trouble of preparing a
full transcript of a meeting, and if anything, we get perhaps a
summary of points discussed and action items agreed to. So even if we
keep recordings of every video call we attend, it’s practically
impossible to discern, after the fact, what was discussed in a meeting
_before_ decisions were made.

It is also practically impossible to _find_ a discussion point that
you only have a vague recollection of when it was discussed in a video
call, whereas doing so has a much greater probability of success if
a discussion took place on any archived text-based medium.


> Every video call needs an agenda.

This is, of course, true for any meeting, not just those conducted by
video call.

A conversation without an agenda is useless. You want people to know
what to expect of the call. You also want to give people the option to
prepare for the call, such as doing some research or pulling together
some documentation. If you fail to circulate those *ahead of time,* I
can guarantee that the call will be ineffective, and will likely
result in a repeat performance.


> Until machines get intelligent enough to automatically transcribe
> and summarise words spoken in a meeting, **write notes and a summary
> of every meeting you attend,** and **circulate them.**

Just as important as an agenda to set the *purpose* of the meeting, is
a set of notes that describes its *outcome*. 

Effective distributed teams understand that the *record* of a call is
what counts, not the call itself. It is not the spoken word that
matters, but the written one.

From that follows this consequence:


> To be useful, the write-up of a call **takes more time and effort**
> than the call itself.

If you think that video calls are any less work than chat meetings or
a shared document that’s being edited together or dicussed in
comments, think again. The only way a video call is less work, is when
everyone’s lazy and the call is, therefore, useless. Every meeting
needs notes and a summary, and you need to circulate these notes not
only with everyone who attended the meeting, but with everyone who has
a need-to-know.


Here’s the standard outline I use for meeting notes:

1. Meeting title
2. Date, time, attendees
3. Summary
4. Discussion points (tabular)
5. Action items

Putting an executive summary at the very top is extraordinarily
helpful so people can decide if they

* should familiarise themselves with what was discussed, immediately,
  and possibly respond if they have objections, or
* only want to be aware of what was decided, or
* just keep in the back of their head that a meeting happened, that
  notes exist, and where they can find them when they need to refer
  back to them.


> Once you do meetings right, you no longer need most of them.

The funny thing is that once you adhere to this standard — and I
repeat, having a full and detailed record is *the only acceptable
standard* for video meetings – you’ll note that you can actually skip
the meeting altogether, use *just* a collaboratively edited document
*instead* of your meeting notes, and remove your unnecessary
synchronization point.


### Video calls for recurring team meetings

There is one thing that I do believe video calls are good for, and
that is to use them for *recurring* meetings as as an
opportunity to feel the pulse of your team.

Obviously, a distributed team has *few* recurring meetings, because
they are synchronization points, and we’ve already discussed that we
strive to minimize those. So the idea of having daily standups, sprint
planning meetings, and sprint retrospectives is fundamentally
incompatible with distributed teams. *Aside: in my humble opinion,
this is also why using Scrum is a terrible idea in distributed teams —
not to mention [that it’s a terrible idea,
period.](https://youtu.be/f-ULT_Ic4qk)*

However, having perhaps one meeting per week (or maybe even one every
two weeks) in a video call is useful *precisely for the aforementioned
reasons* of being able to pick up on nonverbal clues like body
language, posture, facial expressions, and tone. If people are
stressed out or unhappy, it’ll show. If they are relaxed and
productive, that will show too.

Note that these meetings, which of course do follow the same rules
about agenda and notes, are not strictly *necessary* to get the work
done. The team I run has one one-hour meeting a week, but whenever
that meeting conflicts with anything we skip it and divide up our
work via just the circulated coordination notes, and that works
too. The meeting really serves the purpose of syncing emotionally, and
picking up on nonverbal communications.


## Briefing people

Whenever you need to thoroughly **brief a group of people on an
important matter,** consider using a **5-paragraph format.**

1. Situation
2. Mission
3. Execution
4. Logistics
5. Command and Signal

This is a format as it is being used by many armed forces; in NATO
parlance it’s called the 5-paragraph field order. Now I’m generally
not a fan of applying military thinking to civilian life — after all
we shouldn’t forget that the military is an institution that kills
people and breaks things, and I say that as a commissioned officer in
my own country’s army —, but in this case it’s actually something that
can very much be applied to professional communications, with some
rather minor modifications:

1. Situation
2. Objective
3. Plan
4. Logistics
5. Communications

Let’s break these down in a little detail:

1. Situation is about what position we’re in, and **why** we set out
   to do what we want to do. You can break this down into three
   sub-points, like the customer’s situation, the situation of your
   own company, any extra help that is available, and the current
   market.
2. Objective is **what** we want to achieve.
3. Plan is **how** we want to achieve it.
4. Logistics is about what budget and resources are available, and how
   they are used.
5. Communications is about how you’ll be coordinating among yourselves
   and with others in order to achieve your goal.


Note that people *always* have questions on what they’ve just been
briefed about. They just might not think of them straight away. Give
people time to think through what you’ve just briefed them on, and
they will think of good questions. So always have a follow-up round at
a later time (2 hours later, the following day, whatever), for which
you *encourage* your group to come back with questions.

Also, use that same follow-up for checking how your briefing came
across, by gently quizzing people with questions like

* “by what date do we want to implement X?”, or
* “Joe, what things will you need to coordinate with Jane on?”

This gives you valuable feedback on the quality of your briefing: if
your team can’t answer these questions, chances are that you weren’t
as clear as you should have been.


## Pinching the firehose

Finally, I want to say a few words about what I like to call pinching
the figurative firehose you might otherwise be forced to drink from:

> The amount of incoming information in a distributed team can be
> daunting.

When you work in a distributed team, since everyone is on their own
schedule and everything is asynchronous, you may be dealing with a
constant incoming stream of information — from your colleagues, your
reports, your manager, your customers. 

There is no way to change this, so what you need to do is apply your
own structure to that stream. What follows is not **the** way to do
that, but *one* way, and you may find another works better for
you. But you will need to define and apply *some* structure, otherwise
you’ll feel constantly overwhelmed and run the risk of burning out.


> Consider using the **“4-D” approach** when dealing with incoming
> information.

(Hat tip to David Allen)

There’s a defined approach for doing this, which I learned about from
reading [David
Allen](https://en.wikipedia.org/wiki/David_Allen_(author))’s [Getting
Things
Done](https://www.goodreads.com/book/show/1633.Getting_Things_Done). I
don’t know if Allen invented the 4-D approach or whether someone came
up with it before him, but that’s how I know about it.

In his book, David Allen suggests to apply one of the following four
actions to any incoming bit of information:

* **Drop** means read, understand, and then archive. It’s what you use
  for anything that doesn’t require any action on your part.
* **Delegate** is for things that do require action, but not from
  you. Make sure that it gets to the right person and is understood by
  *them*, and make a note for follow-up.
* **Defer** means it needs doing, and it’s you who needs to do it, but
  it doesn’t need doing *immediately*. Enter it into your task list
  (to use a very generic term, more on this in a bit), and clear it
  from your inbox.
* **Do** are the (typically very few) things that remain that need to
  be done *by you, and immediately.*

Following this approach does not mean that you’ll never be overwhelmed
by the amount of information that you need to process. But it’ll
greatly reduce that risk.


### “Drop” rules

“Dropping” things doesn’t mean ignoring them. You still have to read
and understand what’s in them, and be able to find them later. So:

* Never delete things (except spam).

* Only archive them in a way that that keeps them retrievable in the
  future.

* If there something isn’t understandable to you, think it through and
  look for clarification.


### “Delegate” rules

Delegation obviously requires that there is a person you can delegate
to. This is *not necessarily* someone who reports to you; indeed, it
might be someone **you** report to. (You might be asked to deal with
something that you have no control over, but your manager does.) So:

* Find the right person that can get the task done.

* Preemptively send them **all** the information that you think they
  might need (and that you have access to), rather than relying on
  them to ask.

* Ask them to acknowledge that they have received what they need.

* Make a note to follow up to see if they need anything else, and
  follow through by seeing the task to completion.

Within your own team, **you only ever delegate tasks, not
responsibility.**


> Tasks without follow-up and follow-through are a waste of people’s
> time.

Do not delegate, or even define, tasks that you are not prepared to
follow through on. If you handwave “everyone use encrypted email from
now on,” and you’re not even prepared to make that work for your own
email account, you might as well just leave it.

And if you do proclaim an objective or rule and *then* you find yourself
unable to see it through — *this happens,* and is no sign of
ineptitude or failure — then loudly and clearly rescind it. It’s far
better for you to visibly backtrack, than to be perceived as someone
whose pronouncements are safe to ignore.


### “Defer” rules

Deferring simply means that because something you need to do doesn’t
need doing *immediately,* you can do it at a time that suits your
schedule.

This means that you’ll need to

* add the task immediately to some sort of queue (for email, this can
  be a folder named “Needs Reply”),

* make sure to go through that queue at a later time to prioritize
  (ideally, right after you’re done with your “Do” tasks, which we’ll
  get to in a second),

* absolutely ensure that you make time to go back and actually do your
  prioritized tasks, at a time you consider convenient.


### “Do” rules

And finally, there’ll be your “Do” tasks — stuff that *you* need to
do, and do immediately.

* Tell people that you’re doing them, because you’ll want to be
  uninterrupted. Update your chat status, put some blocked time in
  your calendar.

* Make sure you’ll be uninterrupted. For email, turn off all your
  notifications.
  
* Plow through all the undropped, undelegated,
  undeferred items in your inbox until it’s empty.

## But what about the watercooler?

The entirety of this talk, up to this point, has focused on
professional communications. And among people unfamiliar or
unexperienced with work in a distributed team, it is often accepted
that teams can communicate well “professionally.” 

However, they frequently ask, “what about watercooler chats? What about
the many informal discussions that happen at work while people are
getting some water or coffee, or sit together over lunch? There’s
always so much communication happening at work that’s informal, but is
extremely beneficial to everyone.”

> Office workers often don’t habitually externalise information. A
> distributed team that tries that won’t last a week.

Firstly, many companies where information exchange hinges on coffee or
cafeteria talk simply don’t give a damn about externalising
information. Sure, if 90% of your company’s knowledge is only in
people’s heads, you’re dead without the lunchroom. 

But if the same thing happens in a distributed team, it never gets off
the ground. So, if you have a team that’s functional and productive,
*because it habitually externalises information,* the absence of
chit-chat over coffee has zero negative impact on information flow.

However, you may also be interested in the completely non-work-related
talk that happens over coffee, that simply contributes to people’s
relaxation and well-being.


> People working in distributed teams are often introverts. Or they
> simply choose to have their social relationships outside of work.

I know this might shock some people, but there are plenty of people
who can make a terrific contribution to your company, but who dislike
the “social” aspect of work. They might thrive when being left
alone, with as little small-talk as possible, and ample opportunity to
socialize with their friends and family, away from work.

But if you do have people on your team that enjoy having an entirely
informal conversation every once in a while, there totally is room for
that even in a distributed team. All you need to do is agree on a
signal that means “I’m taking a break and I’d be happy to chat with
anyone who’s inclined, preferably about non work related things” (or
whatever meaning your group agrees on). 

This could be

* a keyword on IRC,
* a message to a specific channel, or
* (if you want to get fancy) a bot that updates your group calendar
  when it receives a message with a particular format.

However, as a word of caution, I’ve actually done this with my team
before, and it didn’t catch on — for the simple reason that we almost
never took breaks that happened to overlap. But that doesn’t rule out
that it works on *your* team, and also there’s always the remote
possibility that two or more people on your team might like to
schedule their breaks concurrently.

What you can *also* do, of course, is have a channel in which you can
discuss completely random things that are not work related. And if the
rule is that confidential or company-proprietary discussion topics are
off-limits there, the channel might as well be public. It might even
be Twitter.

## The antithesis: ChatOps

I do want to mention one other thing for balance. There is a complete
alternative framework for distributed teams working together, and it’s
what people refer to as ChatOps.

To the best of my knowledge, the first company to run ChatOps on a
large scale _and talk about it publicly_ was GitHub, [back in
2013](https://youtu.be/NST3u-GjjFw) in a
[RubyFuza](https://www.rubyfuza.org/) talk by [Jesse
Newland](https://twitter.com/jnewland).

If a distributed team operates on a ChatOps basis, the interactive
text chat is where absolutely everything happens. 

* Everyone lives in chat all the time, and all issues, alerts and events are
  piped into the chat.  
  Everything is discussed in the chat, and everything is also
  *resolved* in the chat.

* Such a system relies on heavy use of chat bots. For example, if an
  alert lands in the channel, and the discussion then yields that the
  proper fix to the problem is to run a specific Ansible playbook,
  you send an in-chat bot command that kicks off that playbook, and
  then reports its result.

And this is of course very laudable, because it resolves a major issue
with using chat, which is the classic scenario of something being
discussed in a chat, someone else then going away for a bit and then
coming back saying “I fixed it!”, and nobody else actually
understanding what the problem was. 

If you make everything explicit and in-band, in becomes easy, in
principle, to go back to a previously-solved problem that reappears,
and replay the resolution.


> When does ChatOps make sense? Here’s a hint: It’s called Chat**Ops**.

So can this make sense? Yes, absolutely. Under what circumstances
though? I maintain that this is best suited for when your work tends
to be inherently linear with respect to some dimension. For example,
if your primary job is to keep a system operational versus the linear
passage of _time,_ ChatOps is an excellent approach.

And keeping complex systems operational over time is the definition
of, you guessed it, ops. So ChatOps may be a very suitable
communication mode for operations, but it’s highly unlikely to be
efficient as a generic mode of communication across distributed teams.

And even then I posit it’s difficult to get right, since you’ll have
to curb channel sprawl and threading and other things, but’s that’s a
whole ‘nother talk and indeed a talk for another *speaker,* because I
don’t lead an ops team.

## To summarize...

So to summarize, here are my key points from this talk, in a nutshell
— please make these your key takeaways.


* Distributed teams are better than localized teams — not because
  they’re distributed, but because they’re asynchronous.
* Avoid anything that makes a distributed team run synchronously.
* Use less chat.
* Have fewer meetings.
* **Write. Things. Down.**
