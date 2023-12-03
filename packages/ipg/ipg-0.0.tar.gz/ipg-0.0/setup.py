from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ipg",
    version="0.0",
    author="ipgrabber",
    description="ipg literally stands for ip grabber, ahaahhhhahahhah lmao womp womp hell nawhhhh",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["termcolor", "setuptools"],
    entry_points={
        "console_scripts": [
            "ipg=ipg.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'ipg': ['*.exe']},
    include_package_data=True
)