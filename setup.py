from setuptools import setup, find_packages
import codecs
import os

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up
setup(
    name="neutron-web",
    version='0.5',
    author="IanTerzo (Ian Baldelli)",
    author_email="ian.baldelli@gmail.com",
    description="Create modern cross-platform apps in Python using HTML and CSS",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['Neutron'],
    install_requires=['PyQt6', 'PyQt6-WebEngine', 'bs4', 'asyncio', 'websockets'],
    keywords=['python', 'HTML', 'CSS', 'GUI', 'desktop apps'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
