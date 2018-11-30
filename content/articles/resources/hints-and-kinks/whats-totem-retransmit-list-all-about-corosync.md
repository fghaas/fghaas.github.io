Title: What's a Totem "Retransmit List" all about in Corosync?
Slug: whats-totem-retransmit-list-all-about-corosync
Date: 2012-03-15 09:11:34 +0100
Tags: Corosync

Occasionally, you may see errors similar to this in your system logs:

```
corosync [TOTEM ] Retransmit List: e4 e5 e7 e8 ea eb ed ee
```

Here's what causes them, and what you can do to fix the issue.

Corosync, more specifically its Totem protocol implementation, defines
a maximum number of cluster messages that can be sent during one token
rotation. By default, that number is 50, but you may modify this value
by setting the `window_size` parameter in your `corosync.conf`
configuration file.

When among several fast cluster nodes ("processors" in Totem speak)
there are one or few slow ones, the kernel receive buffers can't cope,
messages get lost, and they then need to be retransmitted. This is
what causes the Retransmit List notifications in the syslogs. This
doesn't mean you're losing any messages or data. But it does mean that
your cluster performance degrades when this happens, and thus you
should really fix that problem.

There are a few considerations that apply to tuning Corosync's
`window_size`:

- If you have a small cluster (say, 8 nodes or less), and they all can
  be expected to perform equally well because they have identical or
  nearly-identical hardware, then setting a large `window_size` of up
  to 300 should be fine.

- If your cluster is rather heterogeneous, then you should probably
  stick with the default of 50. Definitely don't go higher than
  256000/MTU, where MTU is that of the network interface(s) Corosync
  communicates over. For a standard Ethernet interface the default MTU
  is 1500, which would make for a maximum `window_size` of 170.

- If you're running on the generally safe default of 50, and you're
  still getting Retransmit List notifications, then one of your nodes
  is most likely significantly slower than the others, and you had
  better find the cause of that and fix it. The node could be under
  constant excessive load, or have a problem with its network driver,
  or may be plugged into an incorrectly-configured switch port.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
