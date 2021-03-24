# Getting Started

## Requirements

- Python 3.8+ (see `.python-version` with `pyenv`)

## Quickstart

In an existing project:

```sh
$ pip install opennem
```

With poetry:


```sh
$ poetry add opennem
```


## Usage

```
>>> import opennem
>>> opennem.api.networks()
[NetworkSchema(code='WEM', country='au', label='WEM', regions=[NetworkRegionSchema(code='WEM', timezone=None)], timezone='Australia/Perth', interval_size=30),
 NetworkSchema(code='NEM', country='au', label='NEM', regions=[NetworkRegionSchema(code='NSW1', timezone=None), NetworkRegionSchema(code='QLD1', timezone=None), NetworkRegionSchema(code='VIC1', timezone=None), NetworkRegionSchema(code='TAS1', timezone=None), NetworkRegionSchema(code='SA1', timezone=None)], timezone='Australia/Sydney', interval_size=5)]
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
