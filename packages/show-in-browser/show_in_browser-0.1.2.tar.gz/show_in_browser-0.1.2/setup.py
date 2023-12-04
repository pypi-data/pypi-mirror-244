from setuptools import setup, find_packages

setup(
    name="show_in_browser",
    version="0.1.2",
    author="Peter Rush; Mircea-Andrei Radu",
    description="A simple python package for rendering a Pandas DataFrames and matplotlib/plotly plots in a browser.",
    long_description="Please see the README here: https://github.com/pxr687/show_in_browser",
    long_description_content_type='text/markdown',
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
    "pandas",
    "aspose-words"
    ],
)