"""
Setup file for shared utilities across Projects workspace.
"""

from setuptools import setup, find_packages

setup(
    name="projects-utils",
    version="0.1.0",
    description="Shared utilities for data science projects",
    author="q",
    packages=find_packages(include=['utils', 'utils.*']),
    python_requires=">=3.11",
    install_requires=[
        "matplotlib",
    ],
)
