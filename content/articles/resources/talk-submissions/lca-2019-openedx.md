Title: Learn Complex Skills, From Anywhere: Combining Django, Ansible and OpenStack to teach any tech skill
Date: 2019-08-12
Tags: Conference
Slug: lca-2019-openedx
Summary: A talk I submitted to PyCon AU 2018, linux.conf.au 2019, and PyCon DE 2019.

This is a talk I submitted[^1] to three separate conferences:

* [PyCon AU 2018](https://2018.pycon-au.org/), via an anonymized CfP
  process using [PaperCall](https://www.papercall.io/). This
  submission was rejected.

* [linux.conf.au 2019](https://2019.linux.conf.au/), which used a
  non-anonymized CfP process on a custom platform that, _I think,_ is
  built on [Symposion](https://symposion.readthedocs.io/). That
  submission was accepted, and the talk [ran in the main conference
  programme]({filename}../presentations/lca2019-openedx.md).

* [PyCon DE 2019](https://de.pycon.org/), via a non-anonymized CfP
  process using [pretalx](https://pretalx.com/). This
  submission was rejected.

It’s the linux.conf.au submission that is reflected in this page.

## Title

_Learn Complex Skills, From Anywhere: Combining Django, Ansible and
OpenStack to teach any tech skill_

## Target Audience

Community

## Abstract

> This will appear in the conference programme. Up to about 500
> words. This field is rendered with the monospace font Hack with
> whitespace preserved

Professional skill-building is challenging, particularly when the
skill to acquire is about distributed, scalable platform
technology. In this talk, I cover an open-source skill-building
platform that is 100% Python: built on Open edX and heavily involving
Django, Ansible, and OpenStack.

The information technology industry is currently dealing with an
interesting challenge in professional skill-building: almost every new
technology developed in recent years has been complex, distributed,
and built for scale: Kubernetes, Ceph, and OpenStack can serve as just
a few representative examples. Loose coupling, asynchronicity, and
elasticity are just some of the qualities frequently found in such
systems that were entirely absent in many of the systems we built only
a few years ago. As a result, people comfortable with building and
operating these complex systems are hardly found in abundance, and
organisations frequently struggle to adopt these technologies as a
direct result of this scarcity: we are dealing with a skills gap, not
a technology gap.

This means that we need novel ways to educate professionals on these
technologies. We must provide professional learners with complex,
distributed systems to use as realistic learning environments, and we
must enable them to learn from anywhere, at any time, and on their own
pace. One excellent way of doing this is to use the capabilities of
the Open edX platform to integrate a learning management system with
hands-on, on-demand lab environments that can be just as complex, and
just as distributed, as production systems. This allows anyone
interested to develop a professional skill set on novel technology at
minimal cost, and without the need for costly hardware platforms for
evaluation.

In this talk, I will give a rapid technical introduction to the core
components of this free and open source (AGPL 3/ASL 2) all-Python
platform:

* edx-platform, the core learning management system (LMS) and content
  management system (CMS), built on Django;

* edx-configuration, the automated deployment facility to roll out the
  Open edX platform, built on Ansible;

* and finally, the Open edX XBlock extension system and its
  integration with OpenStack, also itself an all-Python cloud
  platform, in order to provide on-demand lab environments from both
  private and public cloud environments.

## Private Abstract

> This will only be shown to organisers and reviewers. You should
> provide any details about your proposal that you don't want to be
> public here. This field is rendered with the monospace font Hack
> with whitespace preserved

I come from a background in technical consulting and instructor-driven
professional education, and together with my team have been building
and deploying Open edX based platforms as described in the talk
since 2015. I believe I have a good understanding on why
instructor-driven training, while desirable, is not accessible to
everyone in need of keeping abreast with technology development, and
that a self-paced, learn-from-anywhere alternative is needed. I am
extremely grateful for the fact that we have an very well-suited
platform for that purpose, and since it has a completely open-source,
Python codebase, it might be of interest to LCA attendees.

I have done a talk on a similar topic at the LCA 2018 Education
miniconf (video link included below). In the 2018 talk, I focused
primarily on the educational aspects of self-paced, on-line
training. This time, and I think more appropriately for the main
conference track, I would like to dive into the nuts and bolts of the
platform that drives this. As such, the talk should still be appealing
to people engaged in professional education (be it as learners,
tutors, or instructional designers), but will also be insightful to
Python and OpenStack developers, and heavy Ansible users.

## Video URL

<https://www.youtube.com/watch?v=E8BhTAjMwa4> 



[^1]: If you’re curious why this is here, please read
    [this]({filename}../../blog/talk-submissions.md).
