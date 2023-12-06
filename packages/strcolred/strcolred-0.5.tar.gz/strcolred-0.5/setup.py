import setuptools
from setuptools import setup
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="strcolred",
    version='0.5',
    license='Eclipse Public License 2.0',
    authors=["johnlesure"],
    author_email="john.lesure@gmail.com",
    description="Python terminal colour library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['strcolred']
)

