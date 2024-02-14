import setuptools
 
with open("README.md", "r", encoding = "utf-8") as file:
    long_description = file.read()
 
setuptools.setup(
    name = "pomeloabc_OI",
    version = "1.0.1",
    author = "AndyPomeloMars",
    author_email = "andypomelomars@163.com",
    description = "This tool can help you more conveniently perform some operations.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/AndyPomeloMars/pomeloabc_OI",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.8"
)