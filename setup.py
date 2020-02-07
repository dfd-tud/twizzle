#!/usr/bin/env python
# coding=utf-8

"""
python distribute file
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

from setuptools import setup


def requirements_file_to_list(fn="requirements.txt"):
    """read a requirements file and create a list that can be used in setup.

    """
    with open(fn, 'r') as f:
        return [x.rstrip() for x in list(f) if x and not x.startswith('#')]


setup(
    name="twizzle",
    version="0.1.1",
    packages=["twizzle"],
    install_requires=requirements_file_to_list(),
    dependency_links=[
        # If your project has dependencies on some internal packages that is
        # not on PyPI, you may list package index url here. Then you can just
        # mention package name and version in requirements.txt file.
    ],
    entry_points={
        # 'console_scripts': [
        #     'main = mypkg.main:main',
        # ]
    },
    package_data={
        # 'mypkg': ['logger.conf']
    },
    platforms=['Linux'],
    author="Robin H., Stephan E.",
    author_email="stephan.escher@tu-dresden.de",
    description="A multi-purpose benchmarking framework",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="GNU GPLv3",
    url="https://github.com/dfd-tud/twizzle",
)
