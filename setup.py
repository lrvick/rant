from setuptools import setup

setup(
    name='rant',
    version='0.2',
    author='Lance R. Vick',
    author_email='lance@lrvick.net',
    packages=['rant'],
    scripts=['bin/rant'],
    url='http://github.com/lrvick/rant',
    license='LICENSE.md',
    description='A CLI driven blog-aware website generator. It is intended to make maintianing a blog or personal website easy using only your favorite console editor such as Vim, and a few simple commands',
    long_description=open('README.md').read(),
    install_requires=[
        'feedgenerator',
        'jinja2',
        'markdown',
        'pyyaml',
        'pygments',
    ]

)
