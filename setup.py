#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This script provides setup requirements to install hrvanalysis via pip"""

import setuptools

# Get long description in READ.md file
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="ecg_qc",
    version="v1.0-b6",
    author="Alexandre CHIROUZE, Alexis COMTE, Laura DUMONT",
    license="GPLv3",
    author_email="alexandre@chirouze.tech, alexis.g.comte@gmail.com, laura.dt.dumont@gmail.com",
    description="a package to compute if ECG signal quality is optimal or noisy",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/Aura-healthcare/ecg_qc",
    packages=setuptools.find_packages("ecg_qc/*", exclude=["tests"]),
    python_requires='>=3.6',
    install_requires=[
        "biosppy>=0.6.1",
        "dill>=0.3.4",
        "numpy>=1.19.5",
        "pathtools>=0.1.2",
        "py-ecg-detectors>=1.0.2",
        "scikit-learn>=0.24.2",
        "wfdb>=3.1.1",
        "xgboost>=1.3.1"
    ],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
