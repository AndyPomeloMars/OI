# PomeloABC - OI

## Project Introduction

This is an open-source `OI` tool developed by `PomeloABC` Studio, with code written in `Python` language.

This tool can help you more conveniently perform some OI operations.

Have you encountered the following situations:

- Hope to generate some strong data in a short period of time and easily use them to capture several programs.

- Hope to quickly crawl the question information (competition information) and submit the question code (competition code).

- Hope to compare two huge files and calculate their similarity.

- Hope to encrypt my private files and not crack them.

- Hope to quickly convert my Markdown document into a PDF document.

So, you can use `pomeloabc-OI` and `Python` to achieve these requirements, and the current features include:

- Program Pairer

- Data Comparator

- Data similarity comparator (using cosine similarity algorithm)

- Data encryptor (using RSA algorithm)

- Document Converter

- Data generators (data structures, files, mathematics, strings, etc.)

- Luogu Crawler (topics, competitions, users, posts, comments, private messages, including submission and other functions)

## Getting Started Guide

Before downloading, you need to prepare Python.

Python download url: [https://www.python.org](https://www.python.org)

- pip install:

    `pip3 install pomeloabc-oi`

- git clone:

    `git clone https://github.com/AndyPomeloMars/OI.git`

**At present, please understand and operate on your own. The official documents will be released in the future (estimated time from July to August 2024)**

**If you find any gaps in the code, please raise an issue and make temporary modifications based on examples and source code**

## Usage examples

```python
import pomeloabc_OI.OJHelper.Luogu as luogu
import pomeloabc_OI.Generator as gen
import pomeloabc_OI.Utils as utils

user = luogu.User("username", "password")
user.login()

problem = luogu.Problem(user, "P1001")
problem.generate()
problem.submit("P1001.cpp")

record = luogu.Record(user, "10000000")
result = record.get()
luogu.print_evaluation_res(result)

gra = gen.Graph()
graph = gra.graph(100, 70)
graph_str = gra.format(graph)

io = gen.IO("example")
io.input_write(graph_str)

rsa = utils.RSA(2048)
rsa.file_encode("example.in")
rsa.file_decode("example.in")
```

## Configuration Required

- `Python` $\geq$ 3.8
    - `playwright` $\geq$ $1.31.0$
    - `bs4` $\geq$ $0.0.1$
    - `rich` $\geq$ $13.6.0$
    - `pyperclip` $\geq$ $1.8.0$
    - `requests` $\geq$ $2.31.0$
    - `pillow` $\geq$ $9.4.0$
    - `html2text` $\geq$ $2020.1.16$
    - `Crypto` $\geq$ $1.4.0$
    - `sklearn` $\geq$ $1.3.0$

- `Tex` $2023$

## Contribution

All contributors please check the Honor List page and sincerely thank them for their contributions to the `pomeloabc-oi` project.

Welcome to contribute to `pomeloabc-oi`. If you have any features you would like to add, you can provide us with an Issue or implement them yourself and then initiate a Pull Request.

For more detailed information on how to make contributions, please review how to make contributions.