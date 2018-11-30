Title: Speaking at the 2012 Percona Live MySQL Conference
Date: 2012-02-27 13:39
Slug: speaking-2012-percona-live-mysql-conference
Author: florian
Tags: Conference, MySQL

This year, I have the pleasure of returning to the MySQL Conference &
Expo as a speaker. Percona have picked up the torch that O'Reilly had
held as the conference organizers, and they're putting together a 3-day
conference this year. I am co-presenting a tutorial with Yves Trudeau
from Percona.

Our tutorial is called [High Availability Deep Dive: Pacemaker, DRBD,
MySQL Replication, and
more!](http://www.percona.com/live/mysql-conference-2012/sessions/mysql-high-availability-deep-dive-pacemaker-drbd-mysql-replication-and-more) and
it's going to be the only full-day tutorial offered in this year's
conference. In it, Yves and I are going to cover

-   </p>
    An overview of the Pacemaker cluster stack (the classic "this is
    Pacemaker" introduction)

    </p>
    <p>
-   </p>
    DRBD-backed MySQL replication (another classic and widely deployed
    scenario)

    </p>
    <p>
-   </p>
    MySQL replication under Pacemaker management (a new option which
    Yves has vastly improved through a big patch set to the MySQL RA).

    </p>
    <p>

Do I expect this talk to be controversial? Definitely. The amount of
"Pacemaker is terrible" and "Pacemaker is unsuitable for managing highly
available databases" that has been around the blogosphere lately is
pretty mind-boggling.

But strangely enough, most of the things brought forward against
Pacemaker by its detractors seem like a time-warp back to about 2007.

-   </p>
    "We must use XML to manage Pacemaker!" Nonsense. In fact, that was
    *never* true – the release of Pacemaker as a separate project and
    the release of the crm shell coincided. Ever since, Pacemaker
    configuration has been as text-based as MySQL itself.

    </p>
    <p>
-   </p>
    "All Pacemaker can do is react to node failure!" Nothing could be
    further from the truth. Pacemaker has some of the most sophisticated
    resource monitoring and auto-recovery capabilities under the sun.

    </p>
    <p>
-   </p>
    "OK. But all it can do to react to *resource* failure is kill a
    daemon!" Bogus again. It will happily do whatever the resource agent
    specifies. Or the admin, through the configuration. 

    </p>
    <p>

In our tutorial, we're going to dispel a few of these myths. We
certainly make no claims as to Pacemaker being the one and only solution
for MySQL HA, but it's one that serves lots of use cases excellently.

Needless to say, I'll also hang around for the conference proper, and
I'm very much looking forward to seeing lots of familiar faces. I'll
also remain in the Bay Area for some time after the MySQL conference –
more on that in a day or two.

* * *

This article originally appeared on my blog on the `hastexo.com` website (now defunct).
