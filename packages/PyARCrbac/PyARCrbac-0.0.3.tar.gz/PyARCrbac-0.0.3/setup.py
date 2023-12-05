from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.3'
DESCRIPTION = 'a Python library that provides functions for retrieving tokens from local azure metadata service.'

# Setting up
setup(
    name="PyARCrbac",
    version=VERSION,
    author="ikbendion (dblonk)",
    author_email="<contact@ikbendion.nl>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    Homepage = "https://github.com/ikbendion/PyARCrbac",
    Issues = "https://github.com/ikbendion/PyARCrbac/issues", 
    readme = "README.MD",
    keywords=['python', 'azure', 'rbac', 'azurearc', 'authentication', 'azmanagement'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)