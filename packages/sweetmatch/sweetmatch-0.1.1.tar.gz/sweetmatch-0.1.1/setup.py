from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

requirements = [
    "scipy",
    "numpy",
]

setup(
    name="sweetmatch",
    version="0.1.1",
    author="Jean-Luc Déziel",
    author_email="jluc1011@hotmail.com",
    url="https://gitlab.com/jldez/sweetmatch",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    install_requires=requirements,
)
