#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='droll',

    version='0.1.dev1',

    description='Code-friendly blogging platform',
    long_description=long_description,

    url='https://github.com/node13h/droll',

    author='Sergej Alikov',
    author_email='sergej.alikov@gmail.com',

    license='AGPL-3.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django :: 1.8',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
    ],

    keywords='django blog',

    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    # See https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'Django>=1.8,<1.9',
        'gunicorn',
        'Markdown',
        'six',
        'pyotp',
        'django-storages',
        'dj-database-url',
    ],

    scripts=['droll-admin.py'],

)
