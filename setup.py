import setuptools

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="LpCli",
    version="0.1",
    author="Matthieu Clemenceau",
    author_email="matthieu.clemenceau@canonical.com",
    description=("A Command Line helper to get data out of LaunchPad."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mclemenceau/lp-cli",
    project_urls={
        'Bug Reports': 'https://github.com/mclemenceau/lp-cli/issues',
        'Source': 'https://github.com/mclemenceau/lp-cli',
    },
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'lp-cli=LpCli.lp_cli:main'
        ],
    },
    install_requires=['launchpadlib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)
