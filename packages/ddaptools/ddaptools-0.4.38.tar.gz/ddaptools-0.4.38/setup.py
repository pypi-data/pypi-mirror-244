from setuptools import setup, find_packages
import codecs
import os



# Update Notes:
"""_summary_

0.4.37: Fixed span guid not extracted from Windows Events
0.4.38: Collapse on events with same span guid that are found on the same staging_event being processed.


"""

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.4.38'
DESCRIPTION = 'DDAPP Modules'
LONG_DESCRIPTION = 'Common Constants, classes and msethods for ETL and other python projects'

# Setting up
#nenewang08
setup(
    name="ddaptools",
    version=VERSION,
    author="Anon Dev",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'utilities'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)


