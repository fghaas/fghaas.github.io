Title: This site now lives on GitHub
Date: 2022-05-05
Slug: moving-to-github
Summary: I have moved my site to GitHub Pages. Here's what that means.

I have moved this site to GitHub. It's still available under the same
URL, of course, but it uses [GitHub Pages](https://pages.github.com/)
for hosting.

Why did I do this? A few reasons:

* I don't have a [comment facility]({filename}../../pages/comments.md)
  on this site, and I don't intend to add one, but I do want to give
  people the ability to submit corrections or sugggestions. You can do
  that now, by [creating a GitHub
  issue](https://github.com/fghaas/fghaas.github.io/issues), sending
  me a pull request, or doing a [GitHub
  edit](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)
  (which is really just a streamlined way of sending a PR from your
  browser).

* It gives me the option to use a GitHub Actions workflow to deploy
  the site fully automatically. As you may know I build this site with
  [Pelican](https://docs.getpelican.com/), and wiring up a workflow
  that first sets off a Pelican build and then invokes `ghp-import`
  (via `tox`) was a breeze. You're welcome to [take a look at the
  implementation](https://github.com/fghaas/fghaas.github.io/blob/main/.github/workflows/deploy.yml)
  if you like. (You can also look at [the relevant
  section](https://docs.getpelican.com/en/latest/tips.html#publishing-to-github)
  in the Pelican docs, of course.)

* Overall, this gives me the ability to do quick edits from almost
  anywhere, and also gives someone else (like you!) the ability to
  suggest fixes, which I can then apply almost instantaneously. But
  please don't *expect* any such things; I do maintain this site on a
  "when I get around to it" basis.

In short: if you've used this site as a regular or irregular
visitor/reader, not much will change. If however you wanted to chuck
in the occasional fix or correction, you can do that more easily now.

If at any point I find that GitHub Pages hosting isn't the right thing
to after all, I'll happily rehome the site elsewhere.

Please be advised that this is still my site, though, and I maintain
editorial control of all content. If you're sending me a PR, please do
so with the understanding that I might decline to merge or publish it,
for any reason at all. If that's not for you, please use your own
platform.
