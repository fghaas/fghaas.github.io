Title: Follow-up and follow-through
Date: 2023-10-07 20:00
Tags: Work, Communications
Slug: follow-up-follow-through
Summary: It comes with the territory.

It recently occurred to me that something I thought was a basic elementary aspect of management at all levels is apparently, in fact, unusual in many organisations.
It's the idea that you can't simply handwave and tell people to do something and if they don't do it then it's their fault, but that as a manager you retain ultimate responsibility and accountability[^raci] for whatever you assign or delegate.

[^raci]: I argue that the idea of responsibility and accountability being two separate things that can be split between two people is a gross distortion of reality and an insult to common sense, but that's a rant for another day.

This means that it's a core part of your job description that *you* ensure that the people you work with actually work on, and have a chance to accomplish, the objectives you entrust them with.
This basic concept in management is known as **follow-up and follow-through.**
And I maintain that being unwilling, incompetent or incapable of follow-up and follow-through should disqualify any person from a management position.

Effectively it means that your people should — having agreed with you on realistic, achievable objectives — be able to rely on you that you'll clear any obstacles that stand in their way.

* They might need to coordinate with someone outside your immediate team, perhaps someone they haven't worked with or even met before, and it's your job to facilitate that collaboration, proactively — that is, ideally you should be thinking of the right person to coordinate with, before they do.
* They might need approval from some higher-up or a green light from a customer, and it's your job to secure that.
* They might need something as simple as a sign-off on an expense, and it's your job to know the applicable policy, get any approval necessary, and then give your report a simple yes or no answer.
* They will rely on you for updates on the schedule.
  Perhaps we need to get something done faster, or maybe there's a holdup somewhere that extends our time window.
* And they will rely on you to follow up on things if they don't go as planned.

Sometimes, when people ask me how I do that and then I ask other the person what's keeping *them* from doing that, their answer gives me the impression that they feel unable to, simply because they don't know what their people are working on, at any given time.
And when I tell them that I always know *exactly* what each of my direct reports is working on, they assume I must be working in a single office with them.
At which point I politely inform them that in fact the average distance between any two of my team members is about 2,000 kilometres, and we see each other in person about twice a year (tops), and we have exactly one video conference per week, and I detest corporate surveillance tactics like "camera on" mandates, and we don't use chat — and then they think I'm either nuts or some sort of a wizard.

Okay. If you're not already convinced I am nuts, then let me share a bit of alleged wizardry with you.

## Use tools, tool-using species!

If you have some kind of a system[^system] that allows you to describe individual units of work — let's call them "tasks"[^generic], which contain

[^system]: It is of secondary importance *what* system it is that you choose to implement the concepts I describe here. They can be applied in a number of systems — Taiga, Trello, Jira, GitHub Projects all come readily to mind, as do others. At least theoretically, you might even use sticky notes on a big sheet of brown paper tacked to a wall near your desk.
[^generic]: I deliberately use the generic terms "task", "subtask", and "supertask" here. The system of your choice my use different terms. What matters is that you have a "thing" which can have zero or more children and zero or one parents.

* a description (what the task is meant to accomplish; you can also call this the "objective" if you're being fancy),
* some kind of time span (say, from a projected start date to a projected end date),
* a person who is assigned the task,
* a status,
* any number of links to related tasks or documents,
* any number of free-form comments,

then you have everything at your disposal to never ever again be clueless about your team's work, and never ever be incapable of follow-up and follow-through.

In using such a system, it is our job to define a few ground rules.

The first thing we define is what status types apply to tasks.
These ultimately define our agreed-upon, practiced, and documented workflow — that is, something that actually deserves being called a *process.*
I have seen people build absolutely Byzantine workflows with a grotesque proliferation of statuses, but I've found these five to be perfectly sufficient:

* *Backlog:* we have defined the task, we want to get to it at some point, but it is currently not being worked on.
   It thus is not assigned to anyone, and has no due date.
* *To Do* (may also be named *Scheduled* or *Selected*): the task is assigned to someone, and it has a completion date, but work on the task has not started.
* *In Progress:* the assignee is working on the task.
* *Done* (or *Completed*): the assignee has completed the task.
* *Declined* (or *Rejected*): we have reconsidered a task that was previously on the backlog, and have decided against pursuing it after all.

The second thing we define is how tasks can relate to each other.
Again, it really doesn't take many of these categories; I think three are enough:

* *Blocker:* one task can be blocked by another, so task A cannot continue/proceed before task B is finished.
* *Cause:* one task can evolve as a direct result of another. 
   For example, a task to investigate a certain problem, assigned to person A, may lead to a task to fix that problem in a certain way, assigned to person B.
* *Relation:* pretty much "everything else", as in task A has something to do with task B, other than blocking or causing it. 
   Thus, anyone looking into *one* of the tasks may benefit from understanding it in the context of the other.

Now, we get to reasonably expect the following things from our reports:

1. They update the task status according to their actual progress on the task.
2. They add any relevant information related to the task either as comments, or as cross-references to other forms of documentation.
3. They create and maintain relevant cross-links to other current or previous tasks.
4. They peruse those cross-links and cross-references in the completion of current and future tasks.

That's it.
It's not reasonable to expect consolidated status reports from individuals on a weekly basis.
Neither is it to torture them with daily standups.[^daily]
We do, however, get to use the tools that our system provides *for us* to visualise, organise, contextualise, and comprehend the tasks that our team is working on.

[^daily]: My working hypothesis is that the existence of a mandatory daily meeting is an indicator for incompetence, poor communications, or functional illiteracy, or any combination of any of these.

A Kanban board is an excellent facility to do all that.
Whatever tool you prefer or your organization mandates, it will *most likely* let you build a Kanban board for all the currently pending tasks on your team, which fulfills just a handful of criteria:

* We need 4 columns, one of each of our statuses (excepting the _Declined_ one).
* We need the ability to filter by date, depending on whether we want a weekly, monthly, quarterly or annual overview.
* We probably want to be able to filter by person.
* We also want some sort of automated colour coding.
  For example, we can automatically colour tasks green if they have a defined start date in the future ("future tasks").
  We can show those with a defined completion date in the past ("overdue tasks") in yellow, and those with a "blocker" relationship with another open task ("blocked tasks") in red.

And that gives us practically everything we need for follow-up and follow-through, at a glance:

* Something is yellow?
  You can check on the comments in that thing and see if the person has run into a roadblock, or needs help, or has asked a question for which you can provide, or ask someone else to provide, an answer. 
  You can ask (again, in a comment) if there is something you can do to facilitate, or you can suggest a different approach, or you can simply conclude that the task will take a few extra days, and bump the due date. 
* Something is red?
  You'll want to investigate what the hold-up is, which you might be able to remove or mitigate.
  Or maybe you're not, in which case you can check on green tasks and maybe ask the person to take one of those on early instead, while they wait for the blocker to be removed.
* Work on something should have started by now, but is still in the "To Do" stage?
  Maybe you want to apply your person filter, see what else that person has on their plate, and check on that.
  Maybe that person is unexpectedly overloaded, or someone else is better suited for this task, or has fewer plates to juggle.
  Or maybe the assignee *is* actually hard at work on the task already, as is evident from their comments therein, but they have simply forgotten to update the status.
* Or perhaps it's Friday[^friday] noon and someone just closed out their last task for the week?
  Good opportunity to drop in the comments to say thanks and wish them a lovely weekend.

[^friday]: This assumes the weekend in your culture is Saturday/Sunday.

## But my org has more than one team!

Sure.
Up to this point, for reasons of simplicity, I have excluded cross-team collaboration.
But trust me, the first thing you'll want to get going is what I described above, at the team level.

To extend this notion to the entire organization, it is furthermore helpful if we don't have just one level of "task", but three:

* A regular "task" is something that can realistically be achieved by one person.
* That person may, for their own benefit, break this task down into something we can call "subtasks"[^generic] to make them more manageable.
  It may also be prudent for another person to take care of an individual subtask, however: 
  responsibility for completing the task remains with the task assignee, and subtasks can only ever be taken on by someone on the same team as the assignee of its parent task.
* When it is necessary to collaborate across teams, we collect multiple tasks into "supertasks"[^generic], so that everyone has a consolidated view of the common objective.
  Obviously, the ultimate responsibility for the completion of the supertask then moves one level up, to whoever has decision authority over everyone involved.
  For example, if an organisation has "departments" made up of "teams" and a supertask includes work done by multiple teams in the department, then supertask responsibility rolls up to the department head (who, of course, can fulfill *their* follow-up and follow-through responsibility by applying the same concept described here, one level up).

And then, we only add one more colour to our Kanban board palette: blue is for tasks that have at least one relationship (of any type) with a task owned by another organisational unit.
These are the ones that you, as the unit lead, monitor for anything you need to coordinate with the *other* unit lead.
Again, facilitating coordination with other organisational units is *our* job, not something where our reports must fend for themselves. 

## In summary

As a manager at any level, follow-up and follow-through is a core element of our responsibility.
In a contemporary technology company using standard tools of the trade, this is easier to do than ever before.
So let's just do it.
