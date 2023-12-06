import codecs
import os

import setuptools
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '0.0.2'
DESCRIPTION = "a crawler program used to get movie's comment on douban"
LONG_DESCRIPTION = 'dumb_menu is a ligh weight menu ,support hot key, support both win and mac'
setup(
    name="my_crawler_qwqcoder",
    version=VERSION,
    author="qwqcoder",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[],
    package_data={
        'src': ['src/*']
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6'
)





