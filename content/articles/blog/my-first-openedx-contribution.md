Title: My first Open edX contribution
Tags: Open edX
Date: 2016-01-05
Author: florian
Summary: In which I talk about landing my first patch in Open edX.

I've finally submitted my first code contribution to [Open
edX](https://open.edx.org/), a trivial patch for an annoying issue in
the LMS start page. The PR is
[here](https://github.com/edx/edx-platform/pull/11138).

The LMS component in Open edX is the stuff that actually provides a
learning platform to students, including the courseware itself, a
discussion forum, a wiki, and everything else you need for an
immersive learning experience. In our own [hastexo
Academy](//academy.hastexo.com) environment, it of course also loads
the [hastexo XBlock](//github.com/hastexo/hastexo-xblock) to interface
with arbitrarily complex, on-demand lab environments.

If you want to know how the LMS fits into Open edX overall, there's
[an overview
graphic](//open.edx.org/sites/default/files/wysiwyg/open-edx-pages/edX_architecture_CMS_LMS_0.png
"Open edX architecture diagram") over at
[open.edx.org](//open.edx.org) for your perusal.

Being a new contributor to Open edX, this obviously involves jumping
through [yet another Contributor Agreement
process](https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst). Here's
to hoping this gets resolved quickly.

### Update, 2016-02-03

The contributor agreement was [squared away really
fast](//github.com/edx/edx-platform/pull/11138#issuecomment-168964638);
the patch review did, however, take some time. [But it's in
now](//github.com/edx/edx-platform/commit/71a6779dfa44baa27d9c2b509587385edb4380af).

* * *

This article originally appeared on my blog on the `hastexo.com` website (now defunct).
