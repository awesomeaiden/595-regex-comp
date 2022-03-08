import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="regex_server",
    version="1.0.0",
    author="Regex Comprehension Team",
    description="Regex Comprehension Backend Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/awesomeaiden/595-regex-comp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
