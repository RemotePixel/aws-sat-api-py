# aws-sat-api-py
Python port of https://github.com/RemotePixel/aws-sat-api

A really simple non-spatial API to get Landsat-8, Sentinel-2(A and B) and CBERS-4 images hosed on AWS S3

# Installation

##### Requirement
  - AWS Account (to access AWS S3).
Please see http://boto3.readthedocs.io/en/latest/guide/configuration.html to configure AWS Credentials env.


```bash
pip install aws-sat-api
```

### Usage

```Python

from aws_sat_api.search import landsat, cbers, sentinel2

l8_path = 178
l8_row = 80
full_search = False
l8_meta = landsat(l8_path, l8_row, full_search)


cbers_path = 178
cbers_row = 80
cbers_sensor = 'MUX'
cbers_meta = cbers(cbers_path, cbers_row, sensor)


utm = 16
lat = 'S'
grid = 'DF'
full_search = False
level = 'l1c'
s2_meta = sentinel2(utm, lat, grid, full_search, level)
```


### CLI

```
awssat --help
Usage: awssat [OPTIONS] COMMAND [ARGS]...

  Search.

Options:
  --help  Show this message and exit.

Commands:
  cbers     CBERS search CLI.
  landsat   Landsat search CLI.
  sentinel  Sentinel search CLI.
```

Example:

Get Zoom 8 mercator tiles covering all landsat images for path/row 015/033 and 015/034
```
awssat landsat -pr 015-033,015-034 | jq -c '. | {"type": "Feature", "properties": {}, geometry: .geometry}' | fio collect | fio extent | supermercado burn 8 | xt -d'-'
8-72-96
8-73-96
8-74-96
8-72-97
8-73-97
8-74-97
8-72-98
8-73-98
8-74-98
8-72-99
8-73-99
8-74-99
8-72-100
8-73-100
8-74-100
```
