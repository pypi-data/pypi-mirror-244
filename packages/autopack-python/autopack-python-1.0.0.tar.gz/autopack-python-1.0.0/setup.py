from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="autopack-python",
    version="1.0.0",
    author="Soikie",
    author_email="1060411267@qq.com",
    description="Provides tools for automated packaging and batch pyd conversion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Soikie/autopack",
    project_urls={
        "Bug Tracker": "https://github.com/Soikie/autopack/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)