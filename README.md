# literotica_dl2
### Since [literotica_dl](https://github.com/fuzzyfiend/literotica_dl) is abandoned I have created this new version
A tool to download stories from Literotica.

[![PyPI - Version](https://img.shields.io/pypi/v/literotica-dl2.svg)](https://pypi.org/project/literotica-dl2)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/literotica-dl2.svg)](https://pypi.org/project/literotica-dl2)

-----

## Table of Contents

- [Installation](#installation)
- [Example Usage](#example)
- [License](#license)

## Installation
I highly recommend you use pipx
```console
pipx install literotica-dl2
```
otherwise you can use pip
```console
pip install literotica-dl2
```

## Details
You must specify whether to download stories or author works or poetry.
* Stories are identified as the url stub following the /s/ directory in the url
    * https://www.literotica.com/s/a-my-name-is-alice
    * story stub is a-my-name-is-alice
* Authors are identified as the url stub following /authors/ and before /works/
    * https://www.literotica.com/authors/Emmah/works/stories
    * author stub is Emmah

By default this program will write works to a new folder called `output`. This can be overridden by specifying the `--output` flag.

By default this program will write works in Text format. This can be changed by specifying `--output-format md` flag.

## Example Usage
# Examples
```console
# Downloading an authors works via the author stub
literotica_dl2 author Emmah

# Downloading an story via the story stub
literotica_dl2 story a-my-name-is-alice

# Downloading an poem via the poem stub
literotica_dl2 poetry acceptance-finding-my-way

# Mirroring the author to a specific directory with markdown format
literotica_dl2 author --output archive --output-format md Emmah
```

# Getting Help
Once installed the help can be called 
```console
literotica_dl2 --help
```
## License

`literotica-dl2` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
