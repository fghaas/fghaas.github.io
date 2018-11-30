Title: Ceph Erasure Code Overhead Mathematics
Date: 2019-11-30
Slug: ceph-ec-math
Tags: Ceph
Summary: In a Ceph cluster, the frequent question, “how much space utilization overhead does my EC profile cause,” can be answered with very simple algebra.

So you’re running a Ceph cluster, and you want to create [pools using
erasure
codes](https://docs.ceph.com/docs/master/rados/operations/erasure-code/),
but you’re not quite sure of exactly how much extra space you’re going
to save, and whether or not that’s worth the performance penalty?
Here’s a simple recipe for calculating that space overhead.

Suppose a RADOS object has a size of $S$, and because it’s in an EC
pool using the
[`jerasure`](https://docs.ceph.com/docs/master/rados/operations/erasure-code-jerasure/)
or
[`isa`](https://docs.ceph.com/docs/master/rados/operations/erasure-code-isa/)
plugin,[^1] Ceph splits it into $k$ equally-sized chunks. Then the
size of any of its $k$ chunks will be: $$S \over k$$

In addition, we get $m$ more parity chunks, also of size $S \over k$.

Thus, the total amount of storage taken by an object of size $S$ is:
$$k \cdot {S \over k} + m \cdot {S \over k}$$

This of course we can rearrange and reduce to $$S + S \cdot {m \over
k}$$ or $$S \cdot (1 + {m \over k})$$ 

In other words, the overhead (that is, the **additional storage**
taken up by the EC parity data) is $$S \cdot {m \over k}$$ or when
expressed as a proportion to $S$, simply $$m \over k$$

As an example, an EC profile with $k = 8, m=3$ comes with a storage
overhead of $3 \over 8$ or 37.5%.

One with $k=5, m=2$ has an overhead of $2 \over 5$, or 40%. 

And finally, a *replicated* (conventional, non-EC) pool with 3
replicas can be thought of as having a degenerate EC profile with
$k=1, m=2$, resulting in an overhead of $2 \over 1$, or 200%.

On a parting note, you should realize that the space utilization
overhead is only one factor by which you should weigh erasure code
profiles against one another. The other is performance. Here, the
general (deliberately oversimplified) rule is that the more chunks you
define — in other words, the higher your $k$ — the higher the
performance penalty you suffer, particularly on reads.[^2] This is due to
the fact that in order to reconstruct the object and serve it to the
application, your client must collect data from $k$ different OSDs and
assemble it locally.[^3]


[^1]: Thanks to [Lars Marowsky-Bree](https://twitter.com/larsmb/) for
    [reminding me](https://twitter.com/larsmb/status/1201425069140000773) that
    slightly different arithmetics apply to the
    [`lrc`](https://docs.ceph.com/docs/master/rados/operations/erasure-code-lrc/),
    [`shec`](https://docs.ceph.com/docs/master/rados/operations/erasure-code-shec/),
    and
    [`clay`](https://docs.ceph.com/docs/master/rados/operations/erasure-code-clay/)
    plugins.

[^2]: Thanks to [Lenz Grimmer](https://twitter.com/LenzGrimmer) for
    [pointing
    out](https://twitter.com/LenzGrimmer/status/1201418525333700608)
    that the post should make this clear.

[^3]: If you want to know more about erasure codes and their history,
	not limited to their use in Ceph, [Danny
	Abukalam](https://twitter.com/dabukalam) did an [interesting
	talk](https://youtu.be/aHATgQL18is) on the subject at OpenStack
	Days Nordic 2019.
