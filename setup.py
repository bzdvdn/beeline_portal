from io import open
from setuptools import setup, find_packages


def read(path):
    with open(path, mode="r") as f:
        return f.read()


setup(
    name="beeline-portal",
    version="0.0.3",
    packages=find_packages(exclude=("tests", "docs", "examples", "venv")),
    install_requires=["requests", "pytz"],
    description="Beeline cloudpbx portal api wrapper",
    author="bzdvdn",
    author_email="bzdv.dn@gmail.com",
    url="https://github.com/bzdvdn/beeline_portal",
    license="MIT",
    python_requires=">=3.7",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
)
