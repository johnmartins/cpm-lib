from setuptools import setup, find_packages

# python setup.py bdist_wheel sdist
VERSION = '1.1.1'
DESCRIPTION = 'Tool for calculating risk of change propagation in a system.'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cpm-lib',
    version=VERSION,
    description=DESCRIPTION,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
    extras_require={
        "dev": [
            "pytest==8.*",
            "twine>=4.0.2"
        ]
    },
    url="https://github.com/johnmartins/cpm-lib",
    author="Julian Martinsson Bonde",
    author_email="johnmartins1992@gmail.com",
    license="MIT"
)