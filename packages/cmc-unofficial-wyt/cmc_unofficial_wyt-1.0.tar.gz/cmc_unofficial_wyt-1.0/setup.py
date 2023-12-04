# setup.py

import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="cmc_unofficial_wyt",
    version="1.0",
    author="wytxty",
    author_email="yvettewkkaa@gmail.com",
    description="cmc wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wytxty/cmc_unofficial_wyt",
    packages=setuptools.find_packages(),
    license="MIT")
