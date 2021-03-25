# Network Definitions

OpenNEM defines a network which has multiple network regions (which usually map to geopgraphic boundaries such as states or grids)

## Networks

Supported networks are accessible via the `/networks` endpoint and `.networks()` client call.

The return schema is

```python
class NetworkSchema():
    """ Defines a network """

    code: str
    country: str
    label: str

    regions: [List[NetworkRegionSchema]]
    timezone: Optional[str]
    interval_size: int
```

## Network Region

```python
class NetworkRegionSchema(BaseConfig):
    """ Defines a network region """

    code: str
    timezone: Optional[str] = Field(None, description="Network region timezone")
```


