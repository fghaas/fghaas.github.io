Title: Configuring radosgw to behave like Amazon S3
Date: 2012-07-09 08:15:57 +0100
Slug: configuring-radosgw-behave-amazon-s3
Tags: Ceph

If you've heard of Ceph, you've surely heard of radosgw, a RESTful
gateway interface to the RADOS object store. You've probably also
heard that it provides a front-end interface that is compatible with
Amazon's S3 API.

The question remains, if you have an S3 client that always assumes it
can find objects at http://bucket.s3.amazonaws.com, how can you use
such a client to interact, unmodified, with your radosgw host (or
hosts)?

Pulling this off is actually remarkably simple, if you can control
what nameserver your clients use to resolve DNS names. Which should be
a given in the private cloud space.

First, of course, you'll need an installed and configured Ceph cluster
with one or several radosgw nodes. The Ceph documentation is an
excellent reference for setting up radosgw.

## Configuring radosgw to support virtual hosts

Then, you make sure you have the following entry in your Ceph configuration (normally in /etc/ceph/ceph.conf):

```ini
[client.radosgw.charlie]
  rgw dns name = s3.amazonaws.com
```

Substitute charlie with whatever name you want to use for your radosgw
client when you interact with Ceph. What the rgw dns name option
specifies is that radosgw will answer queries also for URLs like
http://bucket.hostname/object, as opposed to just
http://hostname/bucket/object.

## Configuring Apache to respond to S3 host names

Also, add a wildcard record to the ServerAlias directive in the web server configuration for your radosgw host. For example:

```apache
<VirtualHost *:80>
    ServerName radosgw.example.com
    ServerAlias s3.amazonaws.com
    ServerAlias *.amazonaws.com
```
	
## Configuring your DNS server

Then, set up your DNS server with a wildcard record in the
s3.amazonaws.com zone, and have nameserver respond to requests in that
zone. The zone file (for BIND9, in this case) could look like this:

```
$TTL	604800
@	IN	SOA	alice.example.com. root.alice.example.com. (
			      2		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	alice.example.com.
@	IN	A	192.168.122.113
*	IN	CNAME	@
```

In this zone, the A record s3.amazonaws.com resolves
to 192.168.122.113, and any sub-domain (like
mybucket.s3.amazonaws.com) also resolves to that same address via a
CNAME record.

## Using your RADOS store with S3 clients

And then you just configure your client hosts to resolve DNS names via
that nameserver, and use your preferred client application to interact
with it.

For example, for a user that you've created with radosgw-admin, which
uses the access key 12345 with a secret of 67890, and Mark Atwood's
popular `Net::Amazon::S3::Tools` toolkit, here's how you can interact
with your RADOS objects:

```
# export AWS_ACCESS_KEY_ID=12345
# export AWS_ACCESS_KEY_SECRET=67890
# s3mkbucket mymostawesomebucket
# s3ls
mymostawesomebucket
# s3put mymostawesomebucket/foobar <<< "hello world"
# s3ls mymostawesomebucket
foobar
# s3get mymostawesomebucket/foobar
hello world
```

Simple enough. You can add one more nifty feature.

## Adding load balancing

radosgw can scale horizontally, and all you need to do to make this
work is to duplicate your radosgw and Apache configuration onto a
different host, and then add a second record to your DNS zone:

```
$TTL	604800
@	IN	SOA	alice.example.com. root.alice.example.com. (
			      3		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	alice.example.com.
@	IN	A	192.168.122.112
@	IN	A	192.168.122.113
*	IN	CNAME	@
```

Then, as you access more buckets, you'll hit the A records in a
round-robin fashion, meaning your requests will be balanced across the
servers. Add as many as you like.

## HTTPS support

Obviously, the above steps will not work for HTTPS connections to the
REST API. And really, making that work would amount to some pretty
terrible SSL certificate authority and client trust hackery, so just
don't do it.

* * *

This article originally appeared on the `hastexo.com` website (now defunct).
