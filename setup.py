# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

from kubecfg import __version__


CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
]

setup(
    name='kubecfg',
    version=__version__,
    description='Kubernetes Config Generator.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    author='Chive',
    author_email='kim@smuzey.ch',
    url='https://github.com/Chive/kubecfg',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=[],
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False
)
