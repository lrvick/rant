# Rant #

<http://github.com/lrvick/rant>

[![TravisCI][travis-badge]][travis-status]
[![Test Coverage][cc-coverage-badge]][cc-coverage]
[![Code Climate][cc-badge]][cc-repo]
[![PyPI version][pypy-badge]][pypy]
[![Wheel][wheel-badge]][wheel]
[![Dependencies][dependencies-badge]][dependencies]
[![License][license-badge]][license]

## About ##

"Rant" is a CLI driven blog-aware website generator written in python. It is
intended to make maintaining a blog or personal website easy as modifying text
files in your favorite editor.

Insipired by great projects such as: [Jekyll][1],
[Pelican][2], [Goldbarg][3], and [piles of others][4]

[1]: https://github.com/mojombo/jekyll
[2]: https://github.com/ametaireau/pelican
[3]: https://github.com/Schnouki/Golbarg
[4]: https://staticsitegenerators.net


## Current Features ##

  * Simple post/page authoring as markdown text files
  * sitemap.xml support
  * RSS / Atom support
  * Full jinja2 templating integration
  * Pagination
  * Pygments syntax hilighting
  * Disqus commenting integration in default templates
  * Other stuff

## Usage / Installation ##

1. Install rant

    Stable:
    ```bash
    pip install --user rant
    ```

    Development:
    ```bash
    pip install --user --upgrade -e git+https://github.com/lrvick/rant/#egg=rant
    ```

2. Start a new rant project

    Create a folder where you intend your site to live and initialize rant.

    ```bash
    rant install my_rant_blog
    ```

    This will populate the folder with the basic rant project ready to add posts to.

3.  Create a post or page

    To create a page or blog post do:

    ```bash
    rant create
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
    rant build
    ```

    From here you can also modify any of the media found in /static, or edit
    any of the [Jinja2](http://jinja.pocoo.org/) layouts found in 'layouts'
    to your liking.

    Happy ranting :-)

4. Preview your work 

    A development web server is included that will run `rant build` for you
    whenever you make changes to your source directory, then reload your
    browser.

    Start it with:

    ```bash
    rant serve
    ```

     The server will be reachable at http://localhost:8080 by default.

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

[cc-badge]: https://codeclimate.com/github/lrvick/rant/badges/gpa.svg
[cc-coverage-badge]: https://codeclimate.com/github/lrvick/rant/badges/coverage.svg
[cc-repo]: https://codeclimate.com/github/lrvick/rant
[cc-coverage]: https://codeclimate.com/github/lrvick/rant/coverage
[pypy-badge]: https://badge.fury.io/py/rant.svg
[pypy]: https://pypi.python.org/pypi/rant
[travis-badge]: https://travis-ci.org/lrvick/rant.svg?branch=master
[travis-status]: https://travis-ci.org/lrvick/rant
[license-badge]: https://img.shields.io/github/license/lrvick/rant.svg?maxAge=2592000
[license]: https://github.com/lrvick/rant/blob/master/LICENSE.md
[wheel-badge]: https://img.shields.io/pypi/format/rant.svg
[wheel]: https://pypi.python.org/pypi/rant
[dependencies-badge]: https://www.versioneye.com/user/projects/5780ca085bb139003969dcf8/badge.svg?style=flat-square
[dependencies]: https://www.versioneye.com/user/projects/5780ca085bb139003969dcf8
