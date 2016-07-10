from setuptools import setup

setup(
    name='rant',
    version='0.2.3',
    author='Lance R. Vick',
    author_email='lance@lrvick.net',
    packages=['rant'],
    scripts=['bin/rant'],
    url='http://github.com/lrvick/rant',
    license='LICENSE.md',
    description='''
    A CLI driven blog-aware website generator. It is intended to make
    maintaining a blog or personal website easy using only your favorite
    console editor such as Vim, and a few simple commands'
    ''',
    long_description=open('README.md').read(),
    package_data={
        '': [
            '../README.md',
            '../LICENSE.md',
            '../CHANGES.md',
            '../AUTHORS.md',
            '../defaults/config.yml',
            '../defaults/*/*'
        ]
    },
    test_suite='tests',
    tests_require=[
        'flake8',
        'wheel',
        'tox',
        'mock',
    ],
    install_requires=[
        'setuptools',
        'Jinja2',
        'Markdown',
        'PyYAML',
        'future'
    ]
)
