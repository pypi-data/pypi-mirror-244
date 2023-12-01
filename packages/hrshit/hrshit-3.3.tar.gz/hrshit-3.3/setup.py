from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="hrshit",
    version="3.3",
    author="Masti Khor",
    author_email="arpitsengar99@gmail.com",
    description="package for playing pikmin from the cli.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arpy8/hrshit",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "hrshit=hrshit.player:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)