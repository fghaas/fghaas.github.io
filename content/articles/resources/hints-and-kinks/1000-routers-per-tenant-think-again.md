Title: 1,000 routers per tenant? Think again!
Date: 2018-12-08
Slug: 1000-routers-per-tenant-think-again
Tags: OpenStack
Summary: When you allow one of your OpenStack tenants a large number of routers, they may not be getting as many as you think they will.

## Neutron quotas

As with all other OpenStack services, Neutron uses a fairly extensive
quota system. An OpenStack admin can give a tenant[^1] a quota limit
on networks, routers, port, subnets, IPv6 subnetpools, and many other
object types.

Most OpenStack deployments set the default per-tenant quota at 10
routers. **However, nothing stops an admin from setting a much higher
router quota, including one above 255. When such a quota change has
been applied to your tenant, you’re in for a surprise.**

## HA routers

Way back in the OpenStack Juno release, we got high-availability
support for Neutron routers. This means that, assuming you have more
than one network gateway node that can host them, your virtual routers
will work in an automated active/backup configuration. 

In effect, what Neutron does for you is that for every subnet that is
plugged into the router — and for which it therefore acts as the
default gateway — the gateway address binds to a keepalived-backed
VRRP interface. On one of the network nodes that interface is active,
and on the others it’s in standby. **If your network node goes down,
keepalived makes sure that the subnets’ default gateway IPs come up on
the other node.** The keepalived configuration is completely
abstracted away from the user; the Neutron L3 agent happily takes care
of all of it.

In addition, in case a network node is up but has lost upstream
network connectivity itself, whereas another is still available that
retains it, HA routers also fail over in order to ensure connectivity
for your VMs.

## The catch: one HA router network per tenant

In order to enable HA routers, Neutron creates _one_ administrative
network per tenant, over which it runs VRRP traffic. In order to tell
apart all the keepalived instances that it manages on that network, it
assigns each an individual Virtual Router ID or VRID.

And here’s the problem: **[RFC
5798](https://tools.ietf.org/html/rfc5798) defines the VRID to be an
8-bit integer.** That means that if you use HA routers, then setting a
router quota over 255 is useless — Neutron will run out of VRIDs in
the administrative network, before your tenant can ever hit the quota.

And this is a hard limit; there’s really not much that Neutron can do
about this — apart from starting to spin up additional administrative
networks once it runs out of VRIDs in the first one, but that likely
would be a pretty involved change. **Thus, at least for the time
being, if you want more than 255 _highly-available_ virtual routers,
you’ll have to spread them across multiple tenants.**

What’s more is that Neutron is not very forthcoming about this
limitation itself: an attempt to create an HA router beyond the limit
simply leads to an `Unknown` error from the Neutron API endpoint.

## Wait, what if I really don’t *need* HA routers?

Well, firstly you probably do want them, really. But that aside,
let’s assume for a moment that you actually don’t. Or rather, that
it’s more important for you to have more than 255 routers in a single
tenant, than for any of them to be highly available. So you create
routers with the `ha` flag set to `False`, simple, right?

It turns out that you probably won’t be able to do that. And that’s
not because you can’t change a router’s `ha` flag without first
temporarily disabling it — that’s not going to hurt you much if you’ve
already decided you don’t need HA; in such a case a brief router blip
will be acceptable. Instead, it’s because (at the time of writing)
**the default Neutron policy restricts setting the `ha` flag on a
router to admins only.**

So *if* you want to be able to disable a router’s HA capability,
you’ll first need to convince your cloud service provider to override
the following default entries in Neutron’s `policy.json`:

```json
{
    "create_router:ha": "rule:admin_only",
    "get_router:ha": "rule:admin_only",
    "update_router:ha": "rule:admin_only",
}
```

... and instead set them as follows:

```json
{
    "create_router:ha": "rule:admin_or_owner",
    "get_router:ha": "rule:admin_or_owner",
    "update_router:ha": "rule:admin_or_owner",
}
```

If your cloud service provider deploys Neutron with
[OpenStack-Ansible](https://docs.openstack.org/openstack-ansible/latest/),
they can define this in the [following
variable](https://docs.openstack.org/openstack-ansible-os_neutron/latest/):

```yaml
neutron_policy_overrides:
    "create_router:ha": "rule:admin_or_owner"
    "get_router:ha": "rule:admin_or_owner"
    "update_router:ha": "rule:admin_or_owner"
```

Once the policy has been overridden in this manner, you should be able
to create a new router with:

```shell
openstack router create --no-ha <name>
```

And modify an existing router’s high-availability flag with:

```shell
openstack router set --disable <name>
openstack router set --no-ha <name>
openstack router set --enable <name>
```

## *Is* my router HA, really?

In relation to what I described above, you may want to *find out*
whether one of your routers is configured to be highly available in
the first place. You’d expect to easily be able to do this with an
`openstack router show` command:


Alas, what you see in the example above *is* indeed a highly-available
router, **so why does it clearly report its `ha` flag as being
`False`?**

Well, that’s another consequence of that default Neutron policy, in
combination with rather unintuitive behavior by the `openstack`
command line client. You see, this part of the aforementioned policy

```json
{
    "get_router:ha": "rule:admin_only",
}
```

... means you’re not even allowed to *query* the `ha` flag if you’re
not an admin, and when the `openstack` client is asked to display a
boolean value that the user is not allowed to even read, then it
always displays `False`.

* * *

[^1]: I’m very sorry, I still can’t force myself to call a tenant it a
	“project”, as I find that term profoundly illogical: the proper
	term for the concept being discussed here is multitenancy, not
	multiprojectcy.
