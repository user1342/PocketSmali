import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PocketSmali",
    version="0.0.1",
    author="James Stevenson",
    author_email="hi@jamesstevenson.me",
    description="A modular and extendable Python tool for emulating simple SMALI methods.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/user1342/PocketSmali",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPL-3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)
