# OpenNEM Energy Market Data Access

![PyPI](https://img.shields.io/pypi/v/opennem) ![Tests](https://github.com/opennem/opennempy/workflows/Tests/badge.svg) ![PyPI - License](https://img.shields.io/pypi/l/opennem)

The OpenNEM project aims to make the wealth of public National Electricity Market (NEM) data more accessible to a wider audience.

This client library for Python enables accessing the Opennem API and data sets.

Project homepage at https://opennem.org.au

Developer documentation at https://developers.opennem.org.au/

Currently supporting the following energy networks:

- Australia NEM: https://www.nemweb.com.au/
- Australia WEM (West Australia): http://data.wa.aemo.com.au/
- APVI rooftop solar data for Australia

## 1. Requirements

- Python 3.8+ (see `.python-version` with `pyenv`)
- Docker and `docker-compose` if you want to run the local dev stack

## 2. Quickstart

```sh
$ pip install opennem
```

```
>>> import opennem
```

## 3. Development

### 3.1 Auto setup and install

For contributions and development of this repository you need to install all the requirements. There
are some helper scripts in the `scripts/` folder.

```sh
$ ./scripts/init.sh
```

By default the venv is installed in the user local cache folder and not in the project path. To link the venv
so that it can be found automatically by the shell or editors run the helper script

```sh
$ ./scripts/link_venv.sh
Created .venv
```

### 3.2 Manual Setup

#### 3.2.1 Prerequisites

For MacOS and Linux require `pyenv` and `poetry`

 * [pyenv homepage](https://github.com/pyenv/pyenv#installation) - simple install with `brew install pyenv`
 * [poetry install](https://python-poetry.org/docs/) (don't install poetry with brew - see [this issue](https://github.com/python-poetry/poetry/issues/36))

#### 3.2.2 Initialize python

We use `pyenv` for python versioning as it allows a system to run multiple version of python. The version for this project is specified in the `.python-version` file in the root of the repository.

To install the locally required python version

```sh
$ pyenv install `cat .python-version`
```

To initialize and use the local python version

```sh
$ pyenv version local
3.9.6 (set by /Users/user/Projects/Opennem/opennempy/.python-version)
```

To test the install is correct

```sh
❯ python -V
Python 3.9.6
❯ which python
/Users/n/.pyenv/shims/python
```

#### 3.2.3 Install with poetry

To manually setup the local development environment, simply create the virtual environment, link it and setup
the PYTHONPATH

```sh
$ poetry install
$ ln -s `poetry env info -p` .venv
$ source .venv/bin/activate
$ pwd > .venv/lib/python3.9/site-packages/local.pth
```

Alternatively to actiavate the virtual environment `poetry` has a shell command:

```sh
$ poetry shell
Spawning shell within /Users/n/Library/Caches/pypoetry/virtualenvs/opennem-pFt2SfpM-py3.9
$ which python
/Users/n/Library/Caches/pypoetry/virtualenvs/opennem-pFt2SfpM-py3.9/bin/python
```

#### 3.2.4 Install with venv

Alternatively if you do not wish to use `poetry` you can setup a simple venv in the local folder and activate it.

```sh
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### 3.3 Test Install

You should be able to run a Python REPL (like `iPython`) and import the `opennem` module

```sh
$ ipython
Python 3.9.6 (default, Jun 28 2021, 19:24:41)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.23.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import opennem

In [2]:
```
