#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from setuptools import setup, find_packages

readme = open('README.md').read()

setup(
    name='dj-wkhtmltopdf',
    version='1.0.3',
    description="Converting Html to Pdf using wkhtmltopdf.",
    long_description=readme,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='wkhtmlpdf,html,pdf,python,django',
    author='Dhana Babu',
    author_email='dhana36.m@gmail.com',
    url='https://github.com/dhanababum/dj-wkhtmltopdf',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
