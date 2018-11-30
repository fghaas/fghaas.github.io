Title: Interleaving in Pacemaker clones
Date: 2012-02-26 20:34:08 +0100
Slug: interleaving-pacemaker-clones
Tags: Pacemaker

Ever wonder what `meta interleave` really means in a Pacemaker clone
definition? We'll explain.

The `interleave` meta attribute is only valid on Pacemaker clone
definitions – and their extended version of sorts, master/slave
sets. It's not available on primitives and groups. Clones are often
used in configurations involving cluster filesystems, such as GFS2
([here's an example]({filename}gfs2-pacemaker-debianubuntu.md)).

Consider the following example (primitive definitions omitted to keep
this short):

```
clone cl_foo p_foo meta interleave=false
clone cl_bar p_bar meta interleave=false
order o_foo_before_bar inf: cl_foo cl_bar
```

What this means is for the `order` constraint to be fulfilled, *all*
instances of `cl_foo` must start before *any* instance of `cl_bar`
can. Often, that's not what you want.

In contrast, consider this:

```
clone cl_foo p_foo meta interleave=true
clone cl_bar p_bar meta interleave=true
order o_foo_before_bar inf: cl_foo cl_bar
```

Here, for each node, as soon as the *local* instance of `cl_foo` has
started, the corresponding local instance of `cl_bar` can, too. **This
is what's usually desired – when in doubt, allow interleaving.**

One thing that often throws people is that interleaving only works
when Pacemaker is configured to run the same number of instances of
two clones on the same node. Thus,

```
clone cl_foo p_foo\
  meta interleave=true \
    globally-unique=true clone-node-max=2
clone cl_bar p_bar meta interleave=false
order o_foo_before_bar inf: cl_foo cl_bar
```

... won't work, as Pacemaker is allowed to run 2 instances of `cl_foo`
on the same node, but only one of `cl_bar` (the default for
`clone-node-max` is 1).

Also, `globally-unique=true` is a requirement for any
`clone-node-max`>1 – which means that interleaving between a
globally-unique and a not globally-unique clone is also not supported.
* * *

This article originally appeared on the `hastexo.com` website (now defunct).
