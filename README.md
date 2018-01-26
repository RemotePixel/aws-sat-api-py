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

# Usage

```Python

from aws_sat_api.search import landsat, cbers, sentinel2

l8_path = 178
l8_row = 80
full_search = False
l8_meta = landsat(l8_path, l8_row, full_search)


cbers_path = 178
cbers_row = 80
cbers_meta = cbers(cbers_path, cbers_row)


utm = 16
lat = 'S'
grid = 'DF'
full_search = False
level = 'l1c'
s2_meta = sentinel2(utm, lat, grid, full_search, level)
```
