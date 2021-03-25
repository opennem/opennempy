# Fueltechs

Defines the primary fuel source for each facility energy or grouping in stats outputs.

```python
class FueltechSchema():
    code: str
    label: str
    renewable: bool
```

## Fields

 * `code` - a unique idenfifier
 * `label` - human readable label for the fueltech for display
 * `renewable` - if the fueltech is classed as renewable

## Exmples

```python
>>> opennem.api.fueltechs()
FueltechSchema(code='coal_brown', label='Coal (Brown)', renewable=False)
```
