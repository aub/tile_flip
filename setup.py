#!/usr/bin/env python

import sys

try:
    from setuptools import setup, find_packages
except:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

readme = file('docs/README.txt','rb').read()

classifiers = [
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
]

setup(name='Seeder',
      version = '0.0.1',
      description = 'a web map seeding system',
      long_description = readme,
      author = 'Aubrey Holland',
      author_email = 'aubrey@gmail.com',
      url = 'http://riotprojects.com/',
			platforms = 'OS Independent',
			require = ['TileCache'],
			packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      scripts = [],
      zip_safe = False,
      test_suite = 'tests.seeder_test',
      license = 'MIT',
      classifiers = classifiers
     )

