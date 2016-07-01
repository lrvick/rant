from setuptools import setup
import os

setup(
    name='rant',
    version='0.2.2',
    author='Lance R. Vick',
    author_email='lance@lrvick.net',
    packages=['rant'],
    scripts=['bin/rant'],
    url='http://github.com/lrvick/rant',
    license='LICENSE.md',
    description='A CLI driven blog-aware website generator. It is intended to make maintianing a blog or personal website easy using only your favorite console editor such as Vim, and a few simple commands',
    long_description=open('README.md').read(),
        #('', ['README.md','LICENSE.md','CHANGES.md','AUTHORS.md']),
    data_files=[('', ['README.md','LICENSE.md','CHANGES.md','AUTHORS.md'])] +
        [(d, [os.path.join(d,f) for f in files])
        for d, folders, files in os.walk('defaults')],
    install_requires=[
        'setuptools == 20.10.1',
        'Jinja2 == 2.8',
        'Markdown == 2.6.6',
        'PyYAML == 3.11'
    ]
)
