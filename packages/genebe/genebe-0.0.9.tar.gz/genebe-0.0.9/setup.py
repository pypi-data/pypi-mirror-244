from setuptools import setup, find_packages
from genebe import version

setup(
    name="genebe",
    version=version.__version__,
    packages=find_packages(),
    install_requires=["pymmh3", "tinynetrc", "pandas", "requests"],
    extras_require={
        "fastmmh3": ["mmh3"],
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Piotr Stawinski",
    description="GeneBe Client: A user-friendly system for annotating genetic variants",
    url="https://genebe.net",
)
