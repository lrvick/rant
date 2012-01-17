# Rant #

<http://github.com/lrvick/rant>

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

  * Python 2.6 - 2.7
  * pip
  * libyaml
  * jinja2
  * pygments

## Usage / Installation ##

1. Install rant

    ```bash
    pip install -e git+https://github.com/lrvick/rant/#egg=rant
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

    This will open vim with a template like the following:

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

    To edit a post in the future simply do:

    ```bash
    rant edit posts/201109230245-My_neat_blog_post.md
    ```

    From here you can also modify any of the media found in /static, or edit
    any of the [Jinja2](http://jinja.pocoo.org/) layouts found in 'layouts'
    to your liking.

    Happy ranting :-)


## Notes ##

Many more features coming soon as this project is under active development.

This is by no means production-ready code. Do not actually use it in
production unless you wish to be eaten by a grue.

Questions/Comments? Please check us out on IRC via irc://udderweb.com/#uw
