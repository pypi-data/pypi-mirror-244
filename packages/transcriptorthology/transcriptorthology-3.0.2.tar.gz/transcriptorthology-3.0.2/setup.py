from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '3.0.2'
DESCRIPTION = 'Algorithm to address Orthology and Paralogy at the Transcript Level'

setup(
    name="transcriptorthology",
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="Wend Yam Donald Davy Ouedraogo",
    author_email="wend.yam.donald.davy.ouedraogo@usherbrooke.ca",
    url='https://github.com/UdeS-CoBIUS/TranscriptOrthology',
    license='CoBIUS Lab',
    packages=find_packages(),
    install_requires=["pandas","ete3","networkx","matplotlib","argparse", "numpy"],
    keywords=['clustering','alternative splicing','orthology-paralogy inference','isoorthology','algorithm','evolution','transcripts', 'phylogeny','computational-biology'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
