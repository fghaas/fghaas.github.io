---
Title: Scaling the flat organization
Date: 2022-01-16
Tags: Work, Communications
Slug: flat-org-scaling
Summary: “We need a flat organizational structure in order to scale.” Or do we, really?
---

There’s a common trope in management that goes something like “in
order to better scale the organization as we grow, we need to keep it
flat.” The thrust of the argument is that as the organization grows to
meet customer and demand growth (and with it, growth in head count),
additional levels of corporate hierarchy stifle that growth, and
should thus be avoided.

For any knowledge-driven organization this is wrong, and just *how*
wrong it is can be proven, numerically, with simple high school level
maths. And in this context, “knowledge-driven organization”
encompasses any technology company, any software engineering outfit,
any technology services provider — in short, any organization that
makes its money off the brains of its people.

Let’s establish a few self-evident facts about knowledge-driven
organizations:

1. The people who actually “make things happen” are the ones with no
   direct reports. The frontend designers, the infrastructure
   engineers, the backend specialists, the data analysts. Their
   managers (and *their* managers, and everyone else all the way up to
   the CEO) are charged with aggregating information, making
   decisions, removing obstacles to productivity, and perhaps
   providing some form of vision and guidance. But it’s individual,
   non-managerial contributors of all specializations that actually
   *do* things.
2. In doing so, engineers work best in small teams with a great degree
   of autonomy. They will usually benefit from close working
   relationships with a small group of people.
3. A manager’s role is thus twofold: remove any obstacles that stand
   in the way of the team accomplishing its goals, and act as an
   interface to other parts of the organization.

## An example

With that in mind, let’s consider a hypothetical small company that is
currently structured in teams of 5. There’s always 4 people reporting
to one manager. Currently, that company is made up as follows:

* the CEO/founder, Alex (1 person),
* 4 team leads (4 people),
* 4 employees on each team, all of whom report to the respective team
  lead (in total, 16 people).

So, 21 people in all.

Management theory calls the number of reports per manager in an
organization the [*span of
control*](https://en.wikipedia.org/wiki/Span_of_control). I don’t like
that term a great deal. For one thing, at four syllables it’s a bit of
a mouthful, particularly if it needs to mentioned frequently. But more
importantly, it’s not an accurate reflection of reality: in a
knowledge-driven organization (like any technology or engineering
company), it’s ludicrous to think that a manager “controls” their
reports like puppets or robots. So, I’ll use a different term for the
remainder of this article: I’m going to call the number of reports per
manager the **width** of the company.

Also, I’ll use the term **depth** for the number of hierarchy levels
that the company has. A sole proprietorship has a depth of zero. A
company with a founder-CEO and a few employees, but no other managers,
has a depth of 1. Alex’ company, with one level of management
reporting to Alex, and everyone else reporting to one of those
managers, currently has a depth of 2.

So we can say that Alex’ company is currently *narrow* and *shallow* —
it has small teams, and few management levels.

Now, the company has just closed a major funding round and several big
customer deals, putting them on a solid growth trajectory. So, Alex
expects the company to double in headcount on an annual basis for the
foreseeable future.

So the question is: is it better for the organization to stick to the
current width, and add depth as it grows, or should Alex increase its
width, so that it can accomodate more people while retaining a
shallower depth?

In other words, as the company scales, should it become *deeper* while
staying *narrow*, or should it grow *wider* while staying *shallow?*

## Fast-forward five years

To look at that, Alex mentally fast-forwards five years under the
currently assumed growth model. After five years of doubling in
headcount, the company now has $21 \cdot 2^5 = 672$ employees.

In this scenario, everyone in the company works still works in a
5-person team, out of which one person is the leader. So every leader
has 4 people that report to them. Let’s look at one employee, Sam. Sam
works in a team with Joe, Jane, Harry and Ruth, and Ruth is the team
lead. Let’s say her title is simply, “Manager”.

Ruth now has at most 3 peers of her own, and reports to someone who
goes by “Senior Manager,” putting her in another team of no more than
5 at her management level. That Senior Manager has at most 3 peers again, all
of whom report to a Director. A Director also, together with a maximum
of 3 other Directors, reports to a VP, and the 4 VPs work together
under Alex, who is still the CEO.

Now, I’ll tell you that for 672 people, you’ll not nearly have filled
all those 5-person teams. But try to intuitively guess, without doing
the math, what organizational size this structure would
accommodate. That is to say, with every person in the company being at
most 5 hops away from the CEO, and everyone working in a group of 5,
what’s the maximum company size this model can handle?

The answer is 1,365.

Let’s quickly break that down and see how we can plug other numbers in.

## A gentle bit of maths, part I: team size and hierarchy levels

Say we take company’s *width*, that is the number of people working
together in any group, *excluding* the leader, as $x$. In our example,
that’s $4$.

Then, any team’s size (which we’ll call $n$, for reasons we’ll get to
in a jiffy) is of course $x+1=5$.

The number of people any Senior Manager is reponsible for is $(x+1)x +
1 = x^2+x+1 = 21$ (that is, their Manager’s teams, and themselves).

The number of people any Director is responsible for is $((x+1)x+1)x+1
= x^3+x^2+x+1 = 85$.

You see where this is going. For any additional level of *depth*, we
simply need to add another power of $x$.

And of course $1 = x^0$ — at the zeroth depth level there’s one
single person: the CEO.

So we can express the number of people in an organization with a width
of $x$ and a depth of $y$ as
$$x^0 + x^1 + x^2 + ... + x^y$$

or, more briefly:[^i] $$\sum_{i=0}^{y} x^{i}$$

[^i]: In this [capital-sigma summation
	formula](https://en.wikipedia.org/wiki/Summation#Capital-sigma_notation),
	$i$ doesn’t mean anything other than it being a counter. The
	formula is pronounced, in English, as “sum of $x$ to the $i$, from
	$i$ equals zero to $y$” (in other words, add up all whole-number
	powers of $x$, from $x^0$ to $x^y$).

And that, in turn, [happens to work out
to](https://www.wolframalpha.com/input/?i2d=true&i=Sum%5BPower%5Bx%2Cn%5D%2C%7Bn%2C0%2Cy%7D%5D)[^indeterminate]
$${x^{y+1}-1} \over {x-1}$$

[^indeterminate]: You might notice that this expression is
    [indeterminate](https://en.wikipedia.org/wiki/Indeterminate_form)
    for $x = 1$. Now I’d say the idea of a hierarchical company made
    up of one-on-one teams (every manager has one report, who in turn
    is the manager of one report, and so on) is extremely unrealistic.
    But just for completeness’ sake, we can apply [a
    limit](https://www.wolframalpha.com/input/?i2d=true&i=Limit%5BDivide%5BPower%5Bx%2Cy%2B1%5D-1%2Cx-1%5D%2Cx-%3E1%5D)
    to show that 
	$$\lim_{x \to 1} {{x^{y+1}-1} \over {x-1}} = {y + 1}$$ 
	In other words, such an organization could accommodate a
    number of people that is equal to its depth plus 1.

Plug in the numbers for $x=4$ and $y=5$, and we get 1,365. 

## A gentle bit of maths, part II: communications in complete graphs

Now, what’s our scaling constraint in a knowledge organization? The
number of people you need to constantly be in touch with in order to
accomplish your goals. 

For Sam, those people are principally your Sam’s teammates team
colleagues, including their manager, Ruth. That’s 4 people. However,
it’s not enough for Sam to understand what *he* is exchanging with
Jane, Joe, Harry, and Ruth; it’s also imperative for him to understand
what *they* communicate about. So, Sam needs to keep himself
appraisedof what Ruth told Harry, or what information Jane gave to
Joe, and how Joe and Harry are coordinating their latest change
(etc.).

That means that **within a team, communications are a [complete
graph](https://en.wikipedia.org/wiki/Complete_graph)**. And for a
complete graph, the number of *edges* is given by $${n(n-1)}\over 2$$

In our case, $n$ is our team size (including the leader), thus
$x+1$ (the reports plus the leader). 

So we can rewrite the complete-graph formula as: 
$${{(x+1)(x+1-1)} \over 2} = {{x(x+1)} \over 2}$$

So in order for the team to be well informed of everyone’s
actions at all times, a 5-person team must keep track of 10
communications links between people. That’s absolutely doable, though
we must keep in mind that the number of links does not grow linearly
with the number of people in direct communications which each other,
but it grows proportionally to the *square* of that number.

Sam’s manager Ruth, of course, works on *two* 5-person teams: Sam’s,
and Ruth’s team of fellow Managers reporting to a Senior Manager. That
means Ruth needs to constantly keep in touch with the people on her
team (including Sam), and also understand what everyone on her team of
Managers is doing. Thus, she keeps track of 20 communications
links. This is also true for her Senior Manager, that Senior Manager’s
Director, and that Director’s VP. It’s only at the very top that the
CEO has the luxury of directly managing only 4 VPs.[^c-suite]

[^c-suite]: This why they might also be able to appoint a CFO, CSO,
    CTO or whatever other C-suite functions are appropriate for the
    organization. So in the scenario we might end up with a handful
    more people than 1,365 for the C-suite and perhaps some number of
    staff in their offices. But for the purposes of this discussion
    those don’t make a big difference, so we’ll disregard them for
    now.

## This should be flatter! Or should it?

Now, suppose someone tells Alex that in this growth plan the
organization is much too hierarchical, and the organization must thus
lose some of its projected hierarchy levels — that is, reduce its
depth. Of course, the only way to do that while still being able to
manage the same headcount growth is to make the company wider — in
other words, have more people report to one manager than previously
planned.

So Alex, being a good CEO, opens some spread sheet software and
creates this handy table that simply plugs in values for $x$ and $y$,
with $x$ (width) in columns and $y$ (depth) in rows.[^table]

[^table]: I encourage you to compare the bottom rows and rightmost
    columns of this table to Wikipedia’s [list of largest
    employers](https://en.wikipedia.org/wiki/List_of_largest_employers).


|        | 2     | 3      | 4         | 5          | 6          | 7           | 8             | 9             | 10             | 11             |
|--------|-------|--------|-----------|------------|------------|-------------|---------------|---------------|----------------|----------------|
| **1**  | 3     | 4      | 5         | 6          | 7          | 8           | 9             | 10            | 11             | 12             |
| **2**  | 7     | 13     | 21        | 31         | 43         | 57          | 73            | 91            | 111            | 133            |
| **3**  | 15    | 40     | 85        | 156        | 259        | 400         | 585           | 820           | 1,111          | 1,464          |
| **4**  | 31    | 121    | 341       | 781        | 1,555      | 2,801       | 4,681         | 7,381         | 11,111         | 16,105         |
| **5**  | 63    | 364    | 1,365     | 3,906      | 9,331      | 19,608      | 37,449        | 66,430        | 111,111        | 177,156        |
| **6**  | 127   | 1,093  | 5,461     | 19,531     | 55,987     | 137,257     | 299,593       | 597,871       | 1,111,111      | 1,948,717      |
| **7**  | 255   | 3,280  | 21,845    | 97,656     | 335,923    | 960,800     | 2,396,745     | 5,380,840     | 11,111,111     | 21,435,888     |
| **8**  | 511   | 9,841  | 87,381    | 488,281    | 2,015,539  | 6,725,601   | 19,173,961    | 48,427,561    | 111,111,111    | 235,794,769    |
| **9**  | 1,023 | 29,524 | 349,525   | 2,441,406  | 12,093,235 | 47,079,208  | 153,391,689   | 435,848,050   | 1,111,111,111  | 2,593,742,460  |
| **10** | 2,047 | 88,573 | 1,398,101 | 12,207,031 | 72,559,411 | 329,554,457 | 1,227,133,513 | 3,922,632,451 | 11,111,111,111 | 28,531,167,061 |

For our previous five-year plan, Alex can just look up the cell
matching $x=4$, $y=5$ and finds our known outcome, a maximum head
count of 1,365.

Now, Alex looks at what it takes to flatten the organization by
eliminating one hierarchy level, or by two.

* If we want to reduce depth by 1, we simply go up one row (thus,
  $y=4$) and find the value for $x$ that just accommodates 1,365
  people or more. Alex sees that that's $x=6$, which can accommodate
  1,555 people. That is, increase the width by 2: reorganize from
  teams of 5 to teams of 7. Alex could also pick $x=5$, that is
  increase the width by only 1, which would land the company at a
  maximum head count of 781. That is well below what $x=4$ can handle,
  but it still lands Alex north of the original growth target of 672.
  
* If we want to reduce depth by 2, we go up two rows ($y=3$) and do
  the same. We end up at $x=11$, which means to increase width by 7:
  reorganize from teams of 5 to teams of 12. Thus, we land at a
  maximum of 1,464 people, slightly exceeding the headcount we’re able
  to accommodate if we keep growing with the current structure. We
  could also do $x=10$ or $x=9$, landing us at maxima well below that
  (1,111 or 820), but still north of 672.

Now what does that mean in terms of communication channels each person
has to maintain?

Again, what we want to keep in mind is the number of edges in a
complete graph connecting $n$ (that is, $x+1$) points. For regular
employees, we know that that’s $${x(x+1)}\over 2$$

And for any manager, who is effectively on two teams of size $x+1$
simultaneously, that’s $$2 \cdot {{x(x+1)}\over 2} = x(x+1)$$

Which means:

* If we want to reduce depth by 1 and go from $x=4$ to
  $x=5$, every non-manager employee now needs to be aware of 15
  communications links (instead of 10), every manager, of 30 (instead
  of 20).
  
* If instead we go from $x=4$ to $x=6$, every non-manager employee now
  needs to be aware of 21 communications links, every manager, of 42.

So that’s a least a 50% increase, or even a doubling, of
communications complexity.

* For the elimination of two hierarchy levels (a depth reduction by
  2), we’ll need to move from $x=4$ to at least $x=8$. At that point,
  every regular employee has at least 36 communications links on their
  teams to deal with; every manager deals with 72.

* If instead we go to $x=9$, every non-manager employee now needs to
  be aware of 45 communications links, every manager, of 90.

* And for $x=10$, every non-manager employee now needs to
  be aware of 55 communications links, every manager, of 110.

At this point Alex realizes that **making the company wide and
shallow, instead of narrow and deep, is painfully expensive in
communication cost.**


## But what about all those managers we won’t have to pay?

A well-meaning advisor interrupts Alex in the middle of planning. He
interjects that Alex is missing a point, namely all the managers that
the company will now no longer need, and the cost savings thus
generated.

So Alex looks at the table again (width in columns, depth in rows):

|        | 2     | 3      | 4         | 5          | 6          | 7           | 8             | 9             | 10             | 11             |
|--------|-------|--------|-----------|------------|------------|-------------|---------------|---------------|----------------|----------------|
| **1**  | 3     | 4      | 5         | 6          | 7          | 8           | 9             | 10            | 11             | 12             |
| **2**  | 7     | 13     | 21        | 31         | 43         | 57          | 73            | 91            | 111            | 133            |
| **3**  | 15    | 40     | 85        | 156        | 259        | 400         | 585           | 820           | 1,111          | 1,464          |
| **4**  | 31    | 121    | 341       | 781        | 1,555      | 2,801       | 4,681         | 7,381         | 11,111         | 16,105         |
| **5**  | 63    | 364    | 1,365     | 3,906      | 9,331      | 19,608      | 37,449        | 66,430        | 111,111        | 177,156        |
| **6**  | 127   | 1,093  | 5,461     | 19,531     | 55,987     | 137,257     | 299,593       | 597,871       | 1,111,111      | 1,948,717      |
| **7**  | 255   | 3,280  | 21,845    | 97,656     | 335,923    | 960,800     | 2,396,745     | 5,380,840     | 11,111,111     | 21,435,888     |
| **8**  | 511   | 9,841  | 87,381    | 488,281    | 2,015,539  | 6,725,601   | 19,173,961    | 48,427,561    | 111,111,111    | 235,794,769    |
| **9**  | 1,023 | 29,524 | 349,525   | 2,441,406  | 12,093,235 | 47,079,208  | 153,391,689   | 435,848,050   | 1,111,111,111  | 2,593,742,460  |
| **10** | 2,047 | 88,573 | 1,398,101 | 12,207,031 | 72,559,411 | 329,554,457 | 1,227,133,513 | 3,922,632,451 | 11,111,111,111 | 28,531,167,061 |

What's handy here is that Alex can look at any one table cell, and the
cell *directly above it* will contain the total number of managers
(that is, people who have direct reports) for the same width. So,

* for $x=4$, $y=5$ (our original scenario allowing the company to grow
  to 1,365 people), Alex would have to hire and pay a total of 341
  managers.
  
* for $x=6$, $y=4$ (the scenario that eliminates one level, and can
  accommodate 1,555 people), Alex’ company will need 259
  managers. That's 82 fewer managers, or a reduction by about 24%.

* for $x=5$, $y=4$ (the scenario that eliminates one level, but
  accommodates only 781 people), Alex’ company will need 156
  managers. That's 185 fewer managers, or a reduction by about 54%.

* for $x=11$, $y=3$ (the scenario that eliminates two levels, and can
  accommodate 1,464 people), the company will need 133
  managers. That's 208 fewer managers, or a reduction by about 61%.

* for $x=10$, $y=3$ (the scenario that eliminates two levels, but
  accommodates only 1,111 people), the company will need 111
  managers. That's 230 fewer managers, or a reduction by about 67%.

* for $x=9$, $y=3$ (the scenario that eliminates two levels, but
  accommodates only 820 people), the company will need 91
  managers. That's 250 fewer managers, or a reduction by about 73%.

## A gentle bit of maths, part III: how much of our company will be managers?

It so happens that we can generalize this. If Alex looks at our table
again, but considers the number of managers proportional to the number
of people in the company, a pattern quickly emerges (again, width
is in columns, depth is in rows):

|        | 2      | 3      | 4      | 5      | 6      | 7      | 8      | 9      | 10     | 11    |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ----- |
| **1**  | 33.33% | 25.00% | 20.00% | 16.67% | 14.29% | 12.50% | 11.11% | 10.00% | 9.09%  | 8.33% |
| **2**  | 42.86% | 30.77% | 23.81% | 19.35% | 16.28% | 14.04% | 12.33% | 10.99% | 9.91%  | 9.02% |
| **3**  | 46.67% | 32.50% | 24.71% | 19.87% | 16.60% | 14.25% | 12.48% | 11.10% | 9.99%  | 9.08% |
| **4**  | 48.39% | 33.06% | 24.93% | 19.97% | 16.66% | 14.28% | 12.50% | 11.11% | 10.00% | 9.09% |
| **5**  | 49.21% | 33.24% | 24.98% | 19.99% | 16.66% | 14.28% | 12.50% | 11.11% | 10.00% | 9.09% |
| **6**  | 49.61% | 33.30% | 25.00% | 20.00% | 16.67% | 14.29% | 12.50% | 11.11% | 10.00% | 9.09% |
| **7**  | 49.80% | 33.32% | 25.00% | 20.00% | 16.67% | 14.29% | 12.50% | 11.11% | 10.00% | 9.09% |
| **8**  | 49.90% | 33.33% | 25.00% | 20.00% | 16.67% | 14.29% | 12.50% | 11.11% | 10.00% | 9.09% |
| **9**  | 49.95% | 33.33% | 25.00% | 20.00% | 16.67% | 14.29% | 12.50% | 11.11% | 10.00% | 9.09% |
| **10** | 49.98% | 33.33% | 25.00% | 20.00% | 16.67% | 14.29% | 12.50% | 11.11% | 10.00% | 9.09% |

You’ll see that at a depth of 1, the share of managers is obviously $1
\over {x+1}$, but then as we increase in depth it quickly trends
toward:[^reciprocal]  $$1 \over x$$

The number of managers in Alex’ company is roughly the reciprocal of
the company’s width. In other words, the number of managers is
inversely proportional to width.

[^reciprocal]: If you’re curious, that is because the share of
    managers in relation to the total number of people in the company
    is 
	$${\sum_{i=0}^{y-1} x^{i}} \over {\sum_{i=0}^{y} x^{i}}$$
	That works out to be $${x^y-1} \over {x^{y+1}-1}$$
	Which, for $y=1$, is
    $${{x-1} \over {x^2-1}} = {{x-1} \over {(x+1)\cdot(x-1)}} = {1 \over {x+1}}$$
    And for larger values of $y$, both $x^y$ and
    $x^{y+1}$ become so large that the $-1$ part barely matters, so
    it’s effectively: 
	$${{x^y-1} \over {x^{y+1}-1}} \approx {x^y \over x^{y+1}} = {1 \over x}$$
    In slightly more formal terms, we can consider $1 \over x$ the 
	*[limit](https://en.wikipedia.org/wiki/Limit_(mathematics))* of the
	expression as $y$ goes to infinity:
	$$\lim_{y \to \infty} {{x^y-1} \over {x^{y+1}-1}} = {1 \over x}$$

In contrast, the cost of communications is directly proportional to
the *square* of the width.

At this point Alex realizes that **while there are indeed savings to
be made by the elimination of management in a wide-and-shallow
company, they cannot possibly balance the added communication cost.**

In other words: the cost in communications inefficiency grows much
faster with width, so much so that it will eat up Alex’ company’s
manager payroll savings several times over.

# In summary

The “flat” (wide) organization scales poorly. Its growth in
communication cost far outpaces its savings in payroll cost. And it
scales progressively worse, the “flatter” (wider) it gets.
