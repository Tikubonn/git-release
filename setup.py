
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as stream:
    long_description = stream.read()

setup(
    name="git-release",
    version="1.0.1",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="tikubonn",
    author_email="https://twitter.com/tikubonn",
    url="https://github.com/tikubonn/git-release",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "autopep8",
    ],
    dependency_links=[],
    entry_points={
        "console_scripts": [
            "git-release = script.git_release:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        'License :: OSI Approved :: MIT License',
    ]
)
