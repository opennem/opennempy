# OpenNEM Developer Documentation

![PyPI](https://img.shields.io/pypi/v/opennem) ![PyPI - License](https://img.shields.io/pypi/l/opennem)


```{warning}
OpenNEM v3 is still in _release candidate_ stage and all data has not been vetted and is still under active development.
```


The OpenNEM project aims to make global energy network data more accessible to a wider audience through a website portal and data access API's and tools.

This client library for Python enables accessing the Opennem API and data sets.

## Project Links

 * Project homepage at [https://opennem.org.au](https://opennem.org.au)
 * Developer Documentation (what you're reading now) at [https://developers.opennem.org.au](https://developers.opennem.org.au)
 * OpenAPI documentation at [https://api.opennem.org.au/docs](https://api.opennem.org.au/docs)
 * Our GitHub organization is `opennem` and at [https://github.com/opennem](https://github.com/opennem)
 * The client library package is on PyPI at [https://pypi.org/project/opennem/](https://pypi.org/project/opennem/)
 * Twitter username is `@opennem` and we are at [https://twitter.com/opennem](https://twitter.com/opennem)


## Supported Data Sets

Currently supported electricity networks:

* `NEM` - [Australia NEM](https://www.nemweb.com.au/)
* `WEM` - [Australia WEM (West Australia)](http://data.wa.aemo.com.au/)
* `APVI` - [APVI](https://apvi.org.au) - Rooftop solar data for Australia

## Project Overview

The OpenNEM project ([GitHub organization `opennem`](https://github.com/opennem/)) consists of three primary projects in separate source code repositories:

 * `opennem-backend` - [GitHub](https://github.com/opennem/opennem) - GitHub project name `opennem`. The primary backend stack that crawls all the data sources, parses them, generates outputs, the database schema and the API interface for integrations. The primary development language is Python.
 * `opennem-fe` - [GitHub](https://github.com/opennem/opennem-fe) - This is the web frontend for OpenNEM written in Javascript and powering the [OpenNEM website](https://opennem.org.au)
 * `opennem` - [GitHub](https://github.com/opennem/opennempy) - GitHUB project name `opennempy`. This is the Python client library for accessing OpenNEM data via the API. It also contains a large set of tools for dealing with energy data.

 ```{warning}
OpenNEM project names and GitHub project names often do not match. For ex. the backend is `opennem-backend` on PyPI and when installed but is on `opennem` as a project name on the GitHub organization
```

## Which project is for me?

We are open to contributions for any of the projects. The backend is developed in Python with FastAPI, SQLAlchemy, Alembic et al. while the frontend is developed in Javascript with vue.js.

 * `opennem-backend` (`opennem/opennem` on GitHub) is the main project and involves collecting and parsing data from numerous sources and storing it in the backend database that is made available via an api at `api.opennem.org.au`. If you are a developer or an academic that is looking to contribute additional features or data source for OpenNEM then this is likely the project you are looking for.
 * If you are a front-end developer and wish to contribute to the features currently on the website then you are likely looking for the `opennem-fe` project.
 * `opennem` (`opennem/opennempy` on GitHub) is the Python client library. If you are an academic, data scientist or wish to query the OpenNEM API to parse and report on the data, then this project is for you. The documentation for the client library begins in the next section of this website.

## Documentation

The backend, frontend and client libaries are all documented here on this site at https://developers.opennem.org.au/. The source for this documentation is available within the `opennempy` GitHub repository. For ex. the source code [for this page is available here](https://github.com/opennem/opennempy/blob/master/source/index.md)

Documentation is build from within the `opennemy` project using a Sphinx template with the source in markdown.

You can run `make watch` which will open a browser with a preview build of the documentation.

Final builds of the documentation are made with `make`. There is currently a GitHub action that automatically publishes these pages on checkin.

## Contents

```{toctree}
:maxdepth: 2

quickstart
introduction
development
settings
schemas/schemas
server/server
```

## Module Documentation

```{toctree}
:maxdepth: 2

opennem/opennem
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
 
