Title: Handy Git aliases
Date: 2023-01-06 18:00
Slug: git-aliases
Tags: Git
Summary: I keep a few aliases in my ~/.gitconfig that you might find useful, too.

I use Git on a practically daily basis, and although it comes with
just about everything including the proverbial kitchen sink, there are
a few bits of functionality that I only *wish* it had. Luckily, Git's
functionality is almost indefinitely extensible via the use of
aliases.

So, here are some that I define in my `~/.gitconfig` file, with a
brief explanation of what they're good for:

## List branches by their date of last modification

```ini
[alias]
  recent = branch --sort=-committerdate --format=\"%(committerdate:relative)%09%(refname:short)\"
```

I frequently have a pretty large number of topic branches that I work
on, plus ones that I pull in from other people's remotes for local
review. So it's helpful to know which branches in my checkout were
most recently updated, and I can run `git recent` to do that.


## Delete old topic branches that have been merged

```ini
[alias]
  delete-merged-branches = !git branch --merged | grep -Ev '(main|master)' | xargs -prn1 git branch -d
```

I create a topic branch for everything that needs to be reviewed and
merged to `main` at some point. That means it's not unheard of that I
create dozens of them each month, and they quickly accumulate. If I
did not regularly prune old topic branches, my Git checkouts would
become unmanageable pretty quickly.

So, I use my `git delete-merged-branches` command to remove those
local branches that are fully merged to `main`.


## Find the origin of a branch point

```
[alias]
	oldest-ancestor = !bash -c 'diff -u <(git rev-list --first-parent \"${1:-main}\") <(git rev-list --first-parent \"${2:-HEAD}\") | sed -ne \"s/^ //p\" | head -1' -
```

Sometimes I create a topic branch off `main`, then add oodles of
commits on it. At the same time, more commits land on `main`, and
eventually I forget which commit I based my branch on.

Then, I can use `git oldest-ancestor` to retrace my branch point,
like so:

* `git oldest-ancestor foo bar`: find out at which commit `bar`
  branched off `foo`.
* `git oldest-ancestor foo`: find out at which commit the currently
  checked-out branch branched off `foo`.
* `git oldest-ancestor`: find out at which commit the currently
  checked-out branch branched off `main`.

> I seem to recall I learned this trick from a Stack Overflow
> discussion, which I can't find anymore. What I *have* found is a
> similar implementation from [Lee Dohm](https://www.lee-dohm.com/)
> that is MIT licensed:
> [`git-oldest-ancestor`](https://github.com/lee-dohm/dotfiles/blob/main/bin/git-oldest-ancestor).


## Fix trailing whitespace

```ini
[alias]
  fixws = !git diff-index --check --cached HEAD -- | sed /^[+-]/d | sed -r s/:[0-9]+:.*// | uniq | xargs sed -e s/[[:space:]]*$// -i
```
I usually want to avoid committing changes with extraneous
whitespace, and if I enable the default `pre-commit` script that
lives in a `.git/hooks` directory by dropping `.sample` off its
filename, Git will even enforce this as a pre-commit rule.

So what I do is this:

* I try `git commit`.
* Git complains about trailing whitespace.
* I run `git fixws`, and repeat my `git commit` command.
