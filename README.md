# Rant #

<http://github.com/lrvick/rant>

[![TravisCI][travis-badge]][travis-status]
[![Code Climate][cc-badge]][cc-repo]
[![Test Coverage][cc-coverage-badge]][cc-coverage]
[![PyPI version][pypy-badge]][pypy]

[cc-badge]: https://codeclimate.com/github/lrvick/rant/badges/gpa.svg
[cc-coverage-badge]: https://codeclimate.com/github/lrvick/rant/badges/coverage.svg
[cc-repo]: https://codeclimate.com/github/lrvick/rant
[cc-coverage]: https://codeclimate.com/github/lrvick/rant/coverage
[pypy-badge]: https://badge.fury.io/py/rant.svg
[pypy]: https://pypi.python.org/pypi/rant
[travis-badge]: https://travis-ci.org/lrvick/rant.svg?branch=master
[travis-status]: https://travis-ci.org/lrvick/rant

## About ##

"Rant" is a CLI driven blog-aware website generator written in python. It is
intended to make maintaining a blog or personal website easy using only your
favorite CLI editor such as vim, and a few simple commands.

Insipired by great projects such as: [Jekyll](https://github.com/mojombo/jekyll),
[Pelican](https://github.com/ametaireau/pelican)
and [Goldbarg](https://github.com/Schnouki/Golbarg)

## Current Features ##

  * Simple post/page authoring as markdown text files
  * sitemap.xml support
  * RSS / Atom support
  * Full jinja2 templating integration
  * Pagination
  * Pygments syntax hilighting
  * Disqus commenting integration in default templates
  * Other stuff

## Requirements ##

  * Python 2.7+
  * pip
  * libyaml
  * jinja2
  * pygments

## Usage / Installation ##

1. Install rant

    ```bash
    pip install rant
    ```

2. Start a new rant project

    Create a folder where you intend your site to live and initialize rant.

    ```bash
    mkdir my_rant_blog
    cd my_rant_blog
    rant install
    ```

    This will populate the folder with the basic rant project ready to add posts to.

3.  Create a post or page

    To make a first blog post do:

    ```bash
    rant publish
    ```

    This will open your default $EDITOR with a template like the following:

    ```bash
    ---
    layout: post
    title:
    date: 2011-09-23 02:45
    image:
    tags:
    comments: true
    draft: false
    ---
    ```

    Fill out the top [YAML](http://yaml.org/) block as you desire, then add
    your post below the '---' in
    [Markdown](http://daringfireball.net/projects/markdown/) format.

    On saving it will automatically generate any needed html for the page
    according to the 'post' templates found in 'layouts/post.html' .

    To edit a post in the future simply edit it and regenerate.

    ```bash
    vim posts/201109230245-My_neat_blog_post.md
    rant generate
    ```

    From here you can also modify any of the media found in /static, or edit
    any of the [Jinja2](http://jinja.pocoo.org/) layouts found in 'layouts'
    to your liking.

    Happy ranting :-)

## Notes ##

  Use at your own risk. You may be eaten by a grue.

  Questions/Comments?

  You can find me on the web via:

  [Email](mailto://lance@lrvick.net) |
  [Blog](http://lrvick.net) |
  [Twitter](http://twitter.com/lrvick) |
  [Facebook](http://facebook.com/lrvick) |
  [Google+](http://plus.google.com/109278148620470841006) |
  [YouTube](http://youtube.com/lrvick) |
  [Last.fm](http://last.fm/user/lrvick) |
  [LinkedIn](http://linkedin.com/in/lrvick) |
  [Github](http://github.com/lrvick/)
