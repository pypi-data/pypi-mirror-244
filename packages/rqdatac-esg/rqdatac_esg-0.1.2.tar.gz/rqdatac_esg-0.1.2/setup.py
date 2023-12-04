# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import versioneer

requirements = [
    # to specify what a project minimally needs to run correctly
    'pandas',
    'python-dateutil',
    'rqdatac>=2.9.48.3',
]

setup(
    name="rqdatac_esg",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="rqdatac esg extension",
    author="Ricequant",
    author_email="public@ricequant.com",
    keywords="rqdatac_esg",
    url="https://www.ricequant.com/",
    include_package_data=True,
    packages=find_packages(include=["rqdatac_esg", "rqdatac_esg.*"]),
    install_requires=requirements,
    python_requires=">=2.7, <4",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            # "rqdatad = rqdatad.__main__:main"
        ]
    },
)
