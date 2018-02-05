"""aws_sat_api.search"""

import os
import json
import itertools
from functools import partial
from concurrent import futures
from datetime import datetime, timezone

from boto3.session import Session as boto3_session

from aws_sat_api import utils, aws

region = os.environ.get('AWS_REGION', 'us-east-1')

landsat_bucket = 'landsat-pds'
cbers_bucket = 'cbers-meta-pds'
sentinel_bucket = 'sentinel-s2'


def get_s2_info(bucket, scene_path, full=False, s3=None, request_pays=False):
    """return Sentinel metadata
    """

    scene_info = scene_path.split('/')

    year = scene_info[4]
    month = utils.zeroPad(scene_info[5], 2)
    day = utils.zeroPad(scene_info[6], 2)
    acquisition_date = f'{year}{month}{day}'

    latitude_band = scene_info[2]
    grid_square = scene_info[3]
    num = scene_info[7]

    info = {
        'sat': 'S2A',
        'path': scene_path,
        'utm_zone': scene_info[1],
        'latitude_band': latitude_band,
        'grid_square': grid_square,
        'num': num,
        'acquisition_date': acquisition_date,
        'browseURL': f'https://sentinel-s2-l1c.s3.amazonaws.com/{scene_path}preview.jpg'}

    utm = utils.zeroPad(info['utm_zone'], 2)
    info['scene_id'] = f'S2A_tile_{acquisition_date}_{utm}{latitude_band}{grid_square}_{num}'

    if full:
        data = json.loads(aws.get_object(bucket, f'{scene_path}tileInfo.json', s3=s3, request_pays=request_pays))
        sat_name = data['productName'][0:3]
        info['sat'] = sat_name
        info['geometry'] = data.get('tileGeometry')
        info['coverage'] = data.get('dataCoveragePercentage')
        info['cloud_coverage'] = data.get('cloudyPixelPercentage')
        info['scene_id'] = f'{sat_name}_tile_{acquisition_date}_{utm}{latitude_band}{grid_square}_{num}'

    return info


def get_l8_info(scene_id, full=False, s3=None):
    """return Landsat-8 metadata
    """

    info = utils.landsat_parse_scene_id(scene_id)
    aws_url = f'https://{landsat_bucket}.s3.amazonaws.com'
    scene_key = info["key"]
    info['browseURL'] = f'{aws_url}/{scene_key}_thumb_large.jpg'
    info['thumbURL'] = f'{aws_url}/{scene_key}_thumb_small.jpg'

    if full:
        data = json.loads(aws.get_object(landsat_bucket, f'{scene_key}_MTL.json', s3=s3))
        image_attr = data['L1_METADATA_FILE']['IMAGE_ATTRIBUTES']
        prod_meta = data['L1_METADATA_FILE']['PRODUCT_METADATA']

        info['sun_azimuth'] = image_attr.get('SUN_AZIMUTH')
        info['sun_elevation'] = image_attr.get('SUN_ELEVATION')
        info['cloud_coverage'] = image_attr.get('CLOUD_COVER')
        info['cloud_coverage_land'] = image_attr.get('CLOUD_COVER_LAND')
        info['geometry'] = {
            'type': 'Polygon',
            'coordinates': [[
                [prod_meta['CORNER_UR_LON_PRODUCT'], prod_meta['CORNER_UR_LAT_PRODUCT']],
                [prod_meta['CORNER_UL_LON_PRODUCT'], prod_meta['CORNER_UL_LAT_PRODUCT']],
                [prod_meta['CORNER_LL_LON_PRODUCT'], prod_meta['CORNER_LL_LAT_PRODUCT']],
                [prod_meta['CORNER_LR_LON_PRODUCT'], prod_meta['CORNER_LR_LAT_PRODUCT']],
                [prod_meta['CORNER_UR_LON_PRODUCT'], prod_meta['CORNER_UR_LAT_PRODUCT']]
            ]]}

    return info


def landsat(path, row, full=False):
    """
    """

    path = utils.zeroPad(path, 3)
    row = utils.zeroPad(row, 3)

    levels = ['L8', 'c1/L8']
    prefixes = [f'{l}/{path}/{row}/' for l in levels]

    # WARNING: This is fast but not thread safe
    session = boto3_session(region_name=region)
    s3 = session.client('s3')

    _ls_worker = partial(aws.list_directory, landsat_bucket, s3=s3)
    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(_ls_worker, prefixes)
        results = itertools.chain.from_iterable(results)

    scene_ids = [os.path.basename(key.strip('/')) for key in results]

    _info_worker = partial(get_l8_info, full=full, s3=s3)
    with futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(_info_worker, scene_ids)

    return results


def cbers(path, row):
    """
    """

    path = utils.zeroPad(path, 3)
    row = utils.zeroPad(row, 3)

    prefix = f'CBERS4/MUX/{path}/{row}/'

    session = boto3_session(region_name=region)
    s3 = session.client('s3')

    results = aws.list_directory(cbers_bucket, prefix, s3=s3)
    scene_ids = [os.path.basename(key.strip('/')) for key in results]
    results = []
    for scene_id in scene_ids:
        info = utils.cbers_parse_scene_id(scene_id)
        scene_key = info["key"]
        preview_id = '_'.join(scene_id.split('_')[0:-1])
        info['thumbURL'] = f'https://s3.amazonaws.com/{cbers_bucket}/{scene_key}/{preview_id}_small.jpeg'
        results.append(info)

    return results


def sentinel2(utm, lat, grid, full=False, level='l1c'):

    if level not in ['l1c', 'l2a']:
        raise Exception('Sentinel 2 Level must be "l1c" or "l2a"')

    s2_bucket = f'{sentinel_bucket}-{level}'
    request_pays = True if level == 'l2a' else False

    current_year = datetime.now(timezone.utc).year + 1
    years = range(2015, current_year)

    utm = str(utm).lstrip('0')

    prefixes = [f'tiles/{utm}/{lat}/{grid}/{y}/' for y in years]

    # WARNING: This is fast but not thread safe
    session = boto3_session(region_name=region)
    s3 = session.client('s3')

    _ls_worker = partial(aws.list_directory, s2_bucket, s3=s3, request_pays=request_pays)
    with futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(_ls_worker, prefixes)
        months_dirs = itertools.chain.from_iterable(results)

    _ls_worker = partial(aws.list_directory, s2_bucket, s3=s3, request_pays=request_pays)
    with futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(_ls_worker, months_dirs)
        days_dirs = itertools.chain.from_iterable(results)

    _ls_worker = partial(aws.list_directory, s2_bucket, s3=s3, request_pays=request_pays)
    with futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(_ls_worker, days_dirs)
        version_dirs = itertools.chain.from_iterable(results)

    _info_worker = partial(get_s2_info, s2_bucket, full=full, s3=s3, request_pays=request_pays)
    with futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(_info_worker, version_dirs)

    return results
