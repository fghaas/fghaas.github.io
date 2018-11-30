Title: Replacing the built-in Open edX forum with a suitable alternative
Date: 2017-02-02
Slug: replace-edx-forum
Tags: Open edX

Open edX comes with a built-in
[discussion forum](http://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/latest/manage_live_course/discussions.html)
service. Many Open edX users find this service less than optimal: it
is the only edX service to require Ruby, it depends on a Ruby version
that is outdated and
[no longer receives security updates (although a fix for that is on the way),](https://github.com/edx/configuration/issues/3589)
it and generally feels like overkill to many users.

Thankfully, since the Open edX Eucalyptus release it's been quite easy
to replace the course forum with an alternative. Here at hastexo,
we're fans of [Disqus](//www.disqus.com) (you may have noticed we also
use it around out web site), so let's see what we can do to drop the
Open edX Forum and replace it with Disqus.

## Step 1: Locate your course's `policy.json` file

If you keep your course materials in Git or some other
version-controlled repository, you'll already be familiar with the
[directory structure of an OLX course tree.](http://edx.readthedocs.io/projects/edx-open-learning-xml/en/latest/directory-structure.html#olx-and-directory-file-structures)
If you're not,
[just use edX Studio](http://help.appsembler.com/article/157-how-to-export-and-import-a-course)
to export your course into a compressed archive, download it, and
extract it on your local machine.

Locate the `policies/_base` directory. Find the `policy.json` file
located therein. It might look like this:

```javascript
{
  "course/201702": {
    "language": "en",
    "invitation_only": true,
    "start": "2017-02-01T00:00:00Z",
    "advertised_start": "2017-02-01T00:00:00Z",
    "end": "2017-02-28T23:59:59Z",
    "is_new": true,
    "catalog_visibility": "both",
    "max_student_enrollments_allowed": null,
    "due": null,
    "giturl": null,
    "course_image": "images_course_image.jpg",
    "advanced_modules": ["hastexo"],
    "hide_from_toc": false,
    "ispublic": false,
    "rerandomize": "never",
    "show_calculator": false,
    "showanswer": "attempted",
    "days_early_for_beta": null,
    "discussion_topics": {
      "General": {
        "id": "i4x-hastexo-hx212-course-201702"
      }
    },
    "tabs": [
      {
        "name": "Courseware",
        "type": "courseware"
      },
      {
        "name": "Course Info",
        "type": "course_info"
      },
      {
        "name": "Textbooks",
        "type": "textbooks"
      },
      {
        "name": "Discussion",
        "type": "discussion"
      },
      {
        "name": "Wiki",
        "type": "wiki"
      },
      {
        "name": "Progress",
        "type": "progress"
      }
    ]
  }
}
```

Note the `tabs` list. It contains the list of course tabs
([which edX Studio, confusingly, calls "pages"](http://edx.readthedocs.io/projects/edx-partner-course-staff/en/latest/course_assets/pages.html)).


## Step 2: Remove the default Discussion tab

You can now edit `policy.json`, and drop the `Discussion` entry from
the `tabs` list, to make it look like so:

```javascript
    "tabs": [
      {
        "name": "Courseware",
        "type": "courseware"
      },
      {
        "name": "Course Info",
        "type": "course_info"
      },
      {
        "name": "Textbooks",
        "type": "textbooks"
      },
      {
        "name": "Wiki",
        "type": "wiki"
      },
      {
        "name": "Progress",
        "type": "progress"
      }
    ]
```

Maybe you also want to remove the course wiki. Just keep whichever
tabs you'd like to keep.


## Step 3: Add a "static" tab

In place of the old `Discussion` tab (which, you may have noticed, was
of a special type conspicuously named `discussion`), you can now put a
tab of different, simpler type: `static_tab`. Like so:

```javascript
    "tabs": [
      {
        "name": "Courseware",
        "type": "courseware"
      },
      {
        "name": "Course Info",
        "type": "course_info"
      },
      {
        "name": "Textbooks",
        "type": "textbooks"
      },
      {
        "name": "Discussion",
        "type": "static_tab",
		"url_slug": "discussion"
      },
      {
        "name": "Wiki",
        "type": "wiki"
      },
      {
        "name": "Progress",
        "type": "progress"
      }
    ]
```

Note that a `static_tab` type tab also requires a value
`url_slug`. What's that one about, you ask?


## Step 4: add static content

Whatever you put into `url_slug` tells Open edX to go look into the
`tabs` subdirectory of your course root, and find a properly named
file there. In our case, that file needs to be named
`discussion.html`, because we defined `"url_slug": "discussion"`.

So, head over to Disqus and grab the generated code from there, and
then stick it into `tabs/discussion.html`. Something like this:

```html
<div id="disqus_thread"></div>
<script>// <![CDATA[
(function() { // DON'T EDIT BELOW THIS LINE
var d = document, s = d.createElement('script');
s.src = '//<your Disqus site domain name>/embed.js';
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
// ]]></script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
<p></p>
```

## Step 5: deploy

Re-compress your tarball,
[upload to Studio](http://edx.readthedocs.io/projects/edx-partner-course-staff/en/latest/course_assets/pages.html)
or run
[`manage.py import`,](https://openedx.atlassian.net/wiki/display/OpenOPS/Managing+OpenEdX+Tips+and+Tricks#ManagingOpenEdXTipsandTricks-manage.pycommands)
and you're done!


* * *

This article originally appeared on the `hastexo.com` website (now defunct).
