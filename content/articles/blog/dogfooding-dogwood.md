Title: Dogfooding Dogwood
Date: 2016-02-12
Slug: dogfooding-dogwood
Author: florian
Tags: Open edX, OpenStack
Summary: The Open edX "Dogwood" release is out. We've been running its code base in production for several weeks, and can share some first-hand experience.


This week, the [Open edX](https://open.edx.org) community
[announced](https://open.edx.org/blog/newest-open-edx-release-dogwood-now-available)
its latest release,
[Open edX Dogwood](http://edx.readthedocs.org/projects/open-edx-release-notes/en/latest/dogwood.html). (In
case you don't follow the Open edX community closely, its releases are
alphabetically named after trees, so on the heels of the Birch and
Cypress releases, we now have
[Dogwood](https://en.wikipedia.org/wiki/Cornus_(genus)), and
Eucalyptus will be next.)

Our team got involved in Open edX around the Cypress release
timeframe, and we shifted our OpenStack integration work to track the
master branch in December, to ensure we would be ready in time for
Dogwood. [hastexo Academy](//academy.hastexo.com) also tracks master,
so if you take one of our self-paced online courses, you'll be running
the latest and greatest from Open edX.

-----

## Checking out the new features

There are several new features in Open edX Dogwood, some of which we
tested and ran, with somewhat mixed (but generally positive) results.


### Platform upgrades

Open edX now builds upon Django 1.8 and Python 2.7.10. It's great to
see some technical debt pay-down by moving beyond the now-unsupported
Django 1.4. We hope to see this continue by Eucalyptus
[hopefully moving to the next Ubuntu LTS, 16.04 "Xenial Xerus".](https://openedx.slack.com/archives/general/p1455215550000885)

It would also be great to see a move to Python 3, but we're not
holding our breath on that, for various reasons &mdash; including the fact
that Ansible, which Open edX uses for deployment, [also still requires
Python 2.](https://lwn.net/Articles/661590/)


### Comprehensive theming

Comprehensive theming is a new and improved way to apply theming and
branding to Open edX platforms, which will eventually replace the
current "Stanford" theming engine (named after an Open edX theme
developed at Stanford University, which became a popular basis for
rebranding the Open edX LMS). In mid-January, we shifted
[our own Stanford-style Open edX theme](https://github.com/hastexo/edx-theme)
to Comprehensive Theming and test-deployed on hastexo Academy, then
still in pre-launch. We ran into a critical bug
[that has been fixed for the release,](https://github.com/edx/edx-platform/pull/11319)
and will come back to redeploying our new Comprehensive theme at a
later date.

We're also waiting for a
[patch to the `edx-configuration` Ansible repository](https://github.com/edx/configuration/pull/2676)
to land, so we can properly deploy our Comprehensive theme to our Open
edX instance.


### Otto

We also looked extensively at the new Open edX ecommerce framework,
"Otto", for buying and sellling course seats. Sadly, we found multiple
issues that prevented us from using it in our infrastructure for the
time being, and we pushed Otto off for our Eucalyptus respin.

Otto has no support for tax assessment on course seats; this is a show
stopper for anyone who wants to sell courses to people in Europe, as
course seats are Digital Goods under EU VAT regulations and require
VAT assessment. We were admittedly a little dismayed to find that Otto
had made some design decisions that made this impossible to fix in the
way you would normally do this in the
[Oscar](http://django-oscar.readthedocs.org/en/latest/) framework that
Otto builds on. Fixing Otto in-place would likely have delayed our
Academy launch by several months, so that was a delay we were
unwilling to accept. There are other issues with Otto, notably the
fact that it comes with its own PayPal integration (as if
[django-oscar-paypal](http://django-oscar-paypal.readthedocs.org/en/latest/)
didn't exist), which made us rather uncomfortable.

So we instead integrated hastexo Academy with our own, pure-Oscar web
store that makes use of upstream community supported features much
more extensively than Otto, and that also enables us to sell other
products and services besides hastexo Academy course seats.


### LTI XBlock

With the Dogwood release, the LTI XModule has been refactored into the
[LTI Consumer XBlock](https://github.com/edx/xblock-lti-consumer). While
we do not currently use this XBlock in production, it comes in very
handy as a good reference for
[XBlock unit tests](https://github.com/edx/xblock-lti-consumer/tree/master/lti_consumer/tests/unit),
which we'll be using to improve the test coverage in our own XBlock.

-----

## Open edX integration with OpenStack

Our OpenStack integration work for Open edX is continuing at its
regular, steady pace.

### Running Open edX Dogwood on OpenStack

You're of course still able to deploy Open edX on OpenStack, using the
Heat templates we've maintained since Cypress.

### Running the hastexo XBlock on Open edX Dogwood

The hastexo XBlock, enabling course authors to define arbitrarily
complex lab environments for courses with OpenStack Heat, is of course
fully supported for Open edX Dogwood. That's exactly what you're using
when speeding through interactive labs on hastexo Academy.

-----

## Congrats, and thanks!

Congratulations are in order for the entire development community! Our
team at hastexo would like to extend a big thank-you to everyone who
made a contribution to this release.

* * *

This article originally appeared on my blog on the `hastexo.com` website (now defunct).
