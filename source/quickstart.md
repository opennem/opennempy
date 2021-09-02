# Getting Started

## Requirements

- Python 3.8+ (see `.python-version` with `pyenv`)
- Docker and `docker-compose` if you want to run the local development stack with a database

Check if you have the correct `python` version in your shell:

```sh
$ python -V
Python 3.9.6
```

If you require assistance setting up a local `python` environment, see the `pyenv` homepage and documentation.


## Quickstart

Install the `PyPI` module

```sh
$ pip install opennem
```

You can now import the module from a Python script or REPL.

```
$ ipython
>>> import opennem
```

## Usage

The following method calls makes a live API request to the OpenNEM servers and returns a list of networks.

```python
>>> import opennem
>>> opennem.api.networks()
[NetworkSchema(code='WEM', country='au', label='WEM', regions=[NetworkRegionSchema(code='WEM', timezone=None)], timezone='Australia/Perth', interval_size=30),
 NetworkSchema(code='NEM', country='au', label='NEM', regions=[NetworkRegionSchema(code='NSW1', timezone=None), NetworkRegionSchema(code='QLD1', timezone=None), NetworkRegionSchema(code='VIC1', timezone=None), NetworkRegionSchema(code='TAS1', timezone=None), NetworkRegionSchema(code='SA1', timezone=None)], timezone='Australia/Sydney', interval_size=5)]
 ```

 The call to `opennem.api.fueltechs` makes a live HTTP request to the OpenNEM API and returns a list of supported fueltechs in well-defined schemas.

```python
>>> opennem.api.fueltechs()
[FueltechSchema(code='battery_charging', label='Battery (Charging)', renewable=True),
 FueltechSchema(code='battery_discharging', label='Battery (Discharging)', renewable=True),
 FueltechSchema(code='coal_black', label='Coal (Black)', renewable=False),
 FueltechSchema(code='coal_brown', label='Coal (Brown)', renewable=False),
 FueltechSchema(code='distillate', label='Distillate', renewable=False),
 FueltechSchema(code='gas_ccgt', label='Gas (CCGT)', renewable=False),
 FueltechSchema(code='gas_ocgt', label='Gas (OCGT)', renewable=False),
 FueltechSchema(code='gas_recip', label='Gas (Reciprocating)', renewable=False),
 FueltechSchema(code='gas_steam', label='Gas (Steam)', renewable=False),
 FueltechSchema(code='hydro', label='Hyrdo', renewable=True),
 FueltechSchema(code='pumps', label='Pumps', renewable=True),
 FueltechSchema(code='solar_utility', label='Solar (Utility)', renewable=True),
 FueltechSchema(code='solar_thermal', label='Solar (Thermal)', renewable=True),
 FueltechSchema(code='solar_rooftop', label='Solar (Rooftop)', renewable=True),
 FueltechSchema(code='wind', label='Wind', renewable=True),
 FueltechSchema(code='aggregator_vpp', label='Aggregator (VPP)', renewable=True),
 FueltechSchema(code='aggregator_dr', label='Aggregator (Demand / Response)', renewable=True),
 FueltechSchema(code='nuclear', label='Nuclear', renewable=True),
 FueltechSchema(code='imports', label='Network Import', renewable=False),
 FueltechSchema(code='exports', label='Network Export', renewable=False),
 FueltechSchema(code='bioenergy_biogas', label='Biogas', renewable=False),
 FueltechSchema(code='bioenergy_biomass', label='Biomass', renewable=False),
 FueltechSchema(code='gas_wcmg', label='Gas (Coal Mine Waste)', renewable=False)]
```

## Example Project

Guided steps for starting a client implemention of the OpenNEM library that will access the API and return data.

First, create a directory for your project and enter that direcoty:

```sh
$ mkdir ~/Work/energy_data
$ cd ~/Work/energy_data
```

Next we need to create a virtual environment for this project, where all the python requirements will be installed. This command creates a virtual environment in the project directory in a folder called `.venv`

```sh
$ python -m venv .venv
```

Before continuing, we'd like to setup this project as a `git` repository so that we can track changes and revisions while we work to develop on it.

The `.venv` directory needs to be added to `.gitignore` so that it is not checked in as part of the repository. The virtual environment is local to the developers machine.

```sh
$ git init
Initialized empty Git repository in /Users/n/Work/energy_data/.git/
```

When you check the git status, you'll see that it picks up the virtual environment `.venv` folder:

```sh
$ git status
On branch main

No commits yet

Untracked files:
	.venv/

nothing added to commit but untracked files present
```

We do not want to commit the virtual environment to the repository so we ignore it by adding the path to a `.gitignore` file and commiting that file to the repository

```sh
$ echo ".venv" >> .gitignore
$ git add .gitignore
$ git commit -m "Added the venv to gitignore"
[main 469dddd] Added the venv to gitignore
 1 file changed, 1 insertion(+)
 create mode 100644 test.txt
