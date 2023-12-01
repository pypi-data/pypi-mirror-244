from setuptools import setup, find_packages

setup(
    name="genebe",
    version="0.0.7",
    packages=find_packages(),
    install_requires=["mmh3", "tinynetrc", "pandas", "requests"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Piotr Stawinski',
    description='GeneBe Client: A user-friendly system for annotating genetic variants',
    url='https://genebe.net',
)
