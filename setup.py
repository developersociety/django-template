#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='blanc-django',
    version='0.1.1',
    description='Blanc setup for Django',
    long_description=open('README.rst').read(),
    url='http://www.blanctools.com/',
    maintainer='Alex Tomkins',
    maintainer_email='alex@blanc.ltd.uk',
    platforms=['any'],
    install_requires=[
        'Fabric==1.7.0',
    ],
    packages=find_packages(),
    package_data={'blanc_django': [
        'conf/*.py',
        'conf/project_name/*.py',
        'conf/project_name/templates/*.html',
        'conf/static/css/*.css',
        'conf/static/css/*.less',
        'conf/static/js/*.js',
    ]},
    entry_points={
        'console_scripts': [
            'blanc-start-project = blanc_django.startproject:main',
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='Proprietary',
)
