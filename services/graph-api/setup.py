import io
import re
import os
from pathlib import Path
from setuptools import find_packages, setup

"""Setup script for packaging.

See http://flask.pocoo.org/docs/1.0/patterns/distribute/ and 
https://pypi.org/project/setuptools/ for details
"""

README = """An graphene server for serving the pinochet dataset"""
INIT_PY = Path(__file__).parent.joinpath("project", "__init__.py")

# versioning occurs at __init__.py
# this pattern is taken from Flask's own setup.py
# https://github.com/pallets/flask/blob/901661c1a4ff23e88884186c9d283ad413970951/setup.py#L10


with io.open(INIT_PY, "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="pinochet-graphene",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    description=README,
    long_description=README,
    url="https://github.com/diegoquintanav/pinochet-analyze",
    author="Diego Quintana Valenzuela",
    author_email="daquintanav@gmail.com",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8.0",
)
