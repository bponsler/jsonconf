from os import listdir
from os.path import join, sep

from setuptools import setup


setup(name='jsonconf',
      version='0.0.1',
      description='Project configuration via JSON',
      author='Brett Ponsler',
      author_email='ponsler@gmail.com',
      url='',
      packages=['jsonconf'],
      test_suite="jsonconf.tests",
      )
