# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import  setup, find_packages


setup(
    name='decorated',
    version='1.4.3',
    author='Mengchen LEE',
    author_email='CooledCoffee@gmail.com',
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    tests_require=[
        "nose>=1.3.1",
        "coverage>=3.7.1",
        "unittest2>=0.5.1",
        "fixtures>=0.3.14",
    ],
    description='Decorator framework and common decorators for python.',
    install_requires=[
        "six>=1.6.1",
        "importlib>=1.0.3",
        "unittest2>=0.5.1"
    ],
    url='https://github.com/CooledCoffee/decorated/',
    zip_safe=True,
    test_suite="nose.collector",
)
