# -*-coding:utf-8-*-

from setuptools import setup

setup(
    name="rte-tempo-api",
    version="1.0.0",
    packages=[
        "rte-tempo-api",
    ],
    url="https://github.com/WazoAkaRapace/rte-api",
    license="MIT",
    author="Mika Benoit",
    author_email="mika.benoit@gmail.com",
    description="Python API wrapper for RTE API",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    install_requires=("requests", "packaging"),
)
