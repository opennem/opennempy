# OpenNEM Energy Market Data Access

![PyPI](https://img.shields.io/pypi/v/opennem) ![Tests](https://github.com/opennem/opennempy/workflows/Tests/badge.svg) ![PyPI - License](https://img.shields.io/pypi/l/opennem)

The OpenNEM project aims to make the wealth of public National Electricity Market (NEM) data more accessible to a wider audience.

This client library for Python enables accessing the Opennem API and data sets.

Project homepage at https://opennem.org.au

Currently supports:

- Australia NEM: https://www.nemweb.com.au/
- Australia WEM (West Australia): http://data.wa.aemo.com.au/
- APVI rooftop solar data for Australia

## Requirements

- Python 3.8+ (see `.python-version` with `pyenv`)
- Docker and `docker-compose` if you want to run the local dev stack

## Quickstart

```sh
$ pip install opennem
```

```
>>> import opennem
```
