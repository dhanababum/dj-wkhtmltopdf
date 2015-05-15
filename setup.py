#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from setuptools import setup, find_packages

readme = open('README.md').read()

setup(
    name='djwkhtmltopdf',
    version='v.0.1.alpha',
    description="Converting Html to Pdf using wkhtmltopdf.",
    long_description=readme,
    classifiers=[
        'Development Status :: 0.1 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
    ],
    keywords='wkhtmlpdf,html,pdf,python,django',
    author='Dhana Babu',
    url='http://github.com/directeur/django-sorting/tree/master',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
