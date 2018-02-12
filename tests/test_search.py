"""tests aws_sat_api.search"""

import os
from io import BytesIO

from mock import patch

from aws_sat_api import search


@patch('aws_sat_api.aws.get_object')
def test_get_s2_info_valid(get_object):
    """Should work as expected
    """

    bucket = 'sentinel-s2-l1c'
    scene_path = 'tiles/38/S/NG/2017/10/9/1/'
    full = False
    s3 = None
    request_pays = False

    expected = {
        'acquisition_date': '20171009',
        'browseURL': 'https://sentinel-s2-l1c.s3.amazonaws.com/tiles/38/S/NG/2017/10/9/1/preview.jpg',
        'grid_square': 'NG',
        'latitude_band': 'S',
        'num': '1',
        'path': 'tiles/38/S/NG/2017/10/9/1/',
        'sat': 'S2A',
        'scene_id': 'S2A_tile_20171009_38SNG_1',
        'utm_zone': '38'}

    assert search.get_s2_info(bucket, scene_path, full, s3, request_pays) == expected
    get_object.assert_not_called()


@patch('aws_sat_api.aws.get_object')
def test_get_s2_info_validFull(get_object):
    """Should work as expected
    """

    path = os.path.join(os.path.dirname(__file__), f'fixtures/tileInfo.json')
    with open(path, 'rb') as f:
        tileInfo = f.read()

    get_object.return_value = tileInfo

    bucket = 'sentinel-s2-l1c'
    scene_path = 'tiles/38/S/NG/2017/10/9/1/'
    full = True
    s3 = None
    request_pays = False

    expected = {
        'acquisition_date': '20171009',
        'browseURL': 'https://sentinel-s2-l1c.s3.amazonaws.com/tiles/38/S/NG/2017/10/9/1/preview.jpg',
        'cloud_coverage': 5.01,
        'coverage': 36.52,
        'geometry': {
            'coordinates': [[
                [499980.0, 4200000.0],
                [609780.0, 4200000.0],
                [609780.0, 4090200.0],
                [499980.0, 4090200.0],
                [499980.0, 4200000.0]]],
            'crs': {'properties': {'name': 'urn:ogc:def:crs:EPSG:8.8.1:32638'}, 'type': 'name'},
            'type': 'Polygon'},
        'grid_square': 'NG',
        'latitude_band': 'S',
        'num': '1',
        'path': 'tiles/38/S/NG/2017/10/9/1/',
        'sat': 'S2B',
        'scene_id': 'S2B_tile_20171009_38SNG_1',
        'utm_zone': '38'}

    assert search.get_s2_info(bucket, scene_path, full, s3, request_pays) == expected
    get_object.assert_called_once()


@patch('aws_sat_api.aws.get_object')
def test_get_s2_info_validFullPays(get_object):
    """Should work as expected
    """

    path = os.path.join(os.path.dirname(__file__), f'fixtures/tileInfo.json')
    with open(path, 'rb') as f:
        tileInfo = f.read()

    get_object.return_value = tileInfo

    bucket = 'sentinel-s2-l1c'
    scene_path = 'tiles/38/S/NG/2017/10/9/1/'
    full = True
    s3 = None
    request_pays = True

    expected = {
        'acquisition_date': '20171009',
        'browseURL': 'https://sentinel-s2-l1c.s3.amazonaws.com/tiles/38/S/NG/2017/10/9/1/preview.jpg',
        'cloud_coverage': 5.01,
        'coverage': 36.52,
        'geometry': {
            'coordinates': [[
                [499980.0, 4200000.0],
                [609780.0, 4200000.0],
                [609780.0, 4090200.0],
                [499980.0, 4090200.0],
                [499980.0, 4200000.0]]],
            'crs': {'properties': {'name': 'urn:ogc:def:crs:EPSG:8.8.1:32638'}, 'type': 'name'},
            'type': 'Polygon'},
        'grid_square': 'NG',
        'latitude_band': 'S',
        'num': '1',
        'path': 'tiles/38/S/NG/2017/10/9/1/',
        'sat': 'S2B',
        'scene_id': 'S2B_tile_20171009_38SNG_1',
        'utm_zone': '38'}

    assert search.get_s2_info(bucket, scene_path, full, s3, request_pays) == expected
    get_object.assert_called_once()
    assert get_object.call_args[1].get('request_pays')


@patch('aws_sat_api.aws.get_object')
def test_get_l8_info_valid(get_object):
    """Should work as expected
    """

    scene_id = 'LC81782462014232LGN00'
    full = False
    s3 = None

    expected = {
        'acquisitionJulianDay': '232',
        'acquisitionYear': '2014',
        'acquisition_date': '20140820',
        'archiveVersion': '00',
        'browseURL':
            'https://landsat-pds.s3.amazonaws.com/L8/178/246/LC81782462014232LGN00/LC81782462014232LGN00_thumb_large.jpg',
        'category': 'pre',
        'groundStationIdentifier': 'LGN',
        'key': 'L8/178/246/LC81782462014232LGN00/LC81782462014232LGN00',
        'path': '178',
        'row': '246',
        'satellite': 'L8',
        'scene_id': 'LC81782462014232LGN00',
        'sensor': 'C',
        'thumbURL':
            'https://landsat-pds.s3.amazonaws.com/L8/178/246/LC81782462014232LGN00/LC81782462014232LGN00_thumb_small.jpg'}

    assert search.get_l8_info(scene_id, full, s3) == expected
    get_object.assert_not_called()


@patch('aws_sat_api.aws.get_object')
def test_get_l8_info_validFull(get_object):
    """Should work as expected
    """

    path = os.path.join(os.path.dirname(__file__), f'fixtures/LC81782462014232LGN00_MTL.json')
    with open(path, 'rb') as f:
        tileInfo = f.read()

    get_object.return_value = tileInfo

    scene_id = 'LC81782462014232LGN00'
    full = True
    s3 = None

    expected = {
        'acquisitionJulianDay': '232',
        'acquisitionYear': '2014',
        'acquisition_date': '20140820',
        'archiveVersion': '00',
        'browseURL':
            'https://landsat-pds.s3.amazonaws.com/L8/178/246/LC81782462014232LGN00/LC81782462014232LGN00_thumb_large.jpg',
        'category': 'pre',
        'cloud_coverage': 38.13,
        'cloud_coverage_land': 50.55,
        'geometry': {
            'coordinates': [[
                [100.4436, 82.63078],
                [86.61133, 82.64704],
                [87.8273, 80.91159],
                [99.02993, 80.89847],
                [100.4436, 82.63078]]],
            'type': 'Polygon'},
        'groundStationIdentifier': 'LGN',
        'key': 'L8/178/246/LC81782462014232LGN00/LC81782462014232LGN00',
        'path': '178',
        'row': '246',
        'satellite': 'L8',
        'scene_id': 'LC81782462014232LGN00',
        'sensor': 'C',
        'sun_azimuth': -115.79513548,
        'sun_elevation': 16.11011632,
        'thumbURL':
            'https://landsat-pds.s3.amazonaws.com/L8/178/246/LC81782462014232LGN00/LC81782462014232LGN00_thumb_small.jpg'}

    assert search.get_l8_info(scene_id, full, s3) == expected
    get_object.assert_called_once()


@patch('aws_sat_api.aws.get_object')
def test_get_l8_info_validC1(get_object):
    """Should work as expected
    """

    scene_id = 'LC08_L1GT_178119_20180103_20180103_01_RT'
    full = False
    s3 = None

    expected = {
        'acquisition_date': '20180103',
        'browseURL':
            'https://landsat-pds.s3.amazonaws.com/c1/L8/178/119/LC08_L1GT_178119_20180103_20180103_01_RT/LC08_L1GT_178119_20180103_20180103_01_RT_thumb_large.jpg',
        'category': 'RT',
        'collection': '01',
        'correction_level': 'L1GT',
        'ingestion_date': '20180103',
        'key': 'c1/L8/178/119/LC08_L1GT_178119_20180103_20180103_01_RT/LC08_L1GT_178119_20180103_20180103_01_RT',
        'path': '178',
        'row': '119',
        'satellite': 'L8',
        'scene_id': 'LC08_L1GT_178119_20180103_20180103_01_RT',
        'sensor': 'C',
        'thumbURL':
            'https://landsat-pds.s3.amazonaws.com/c1/L8/178/119/LC08_L1GT_178119_20180103_20180103_01_RT/LC08_L1GT_178119_20180103_20180103_01_RT_thumb_small.jpg'}

    assert search.get_l8_info(scene_id, full, s3) == expected
    get_object.assert_not_called()


@patch('aws_sat_api.aws.get_object')
def test_get_l8_info_validFullc1(get_object):
    """Should work as expected
    """

    path = os.path.join(os.path.dirname(__file__), f'fixtures/LC08_L1GT_178119_20180103_20180103_01_RT_MTL.json')
    with open(path, 'rb') as f:
        tileInfo = f.read()

    get_object.return_value = tileInfo

    scene_id = 'LC08_L1GT_178119_20180103_20180103_01_RT'
    full = True
    s3 = None

    expected = {
        'acquisition_date': '20180103',
        'browseURL':
            'https://landsat-pds.s3.amazonaws.com/c1/L8/178/119/LC08_L1GT_178119_20180103_20180103_01_RT/LC08_L1GT_178119_20180103_20180103_01_RT_thumb_large.jpg',
        'category': 'RT',
        'cloud_coverage': 64.66,
        'cloud_coverage_land': 64.66,
        'collection': '01',
        'correction_level': 'L1GT',
        'geometry': {
            'coordinates': [[
                [-36.27662, -80.68672],
                [-45.77772, -79.24248],
                [-55.38046, -80.6257],
                [-45.97596, -82.33114],
                [-36.27662, -80.68672]]],
            'type': 'Polygon'},
        'ingestion_date': '20180103',
        'key': 'c1/L8/178/119/LC08_L1GT_178119_20180103_20180103_01_RT/LC08_L1GT_178119_20180103_20180103_01_RT',
        'path': '178',
        'row': '119',
        'satellite': 'L8',
        'scene_id': 'LC08_L1GT_178119_20180103_20180103_01_RT',
        'sensor': 'C',
        'sun_azimuth': 93.74503077,
        'sun_elevation': 22.51092792,
        'thumbURL':
            'https://landsat-pds.s3.amazonaws.com/c1/L8/178/119/LC08_L1GT_178119_20180103_20180103_01_RT/LC08_L1GT_178119_20180103_20180103_01_RT_thumb_small.jpg'}

    assert search.get_l8_info(scene_id, full, s3) == expected
    get_object.assert_called_once()


@patch('aws_sat_api.search.boto3_session')
@patch('aws_sat_api.aws.list_directory')
def test_landsat_valid(list_directory, session):
    """Should work as expected
    """

    session.return_value.client.return_value.get_object.return_value = True

    list_directory.side_effect = [
        ['c1/L8/178/119/LC08_L1GT_178119_20180103_20180103_01_RT/'],
        ['L8/178/119/LC81781192017016LGN00/']]

    path = '178'
    row = '119'
    full = False

    assert list(search.landsat(path, row, full))
    session.return_value.client.return_value.get_object.assert_not_called()
    assert list_directory.call_count == 2


@patch('aws_sat_api.search.boto3_session')
@patch('aws_sat_api.aws.list_directory')
def test_landsat_validFull(list_directory, session):
    """Should work as expected
    """

    path = os.path.join(os.path.dirname(__file__), f'fixtures/LC08_L1GT_178119_20180103_20180103_01_RT_MTL.json')
    with open(path, 'rb') as f:
        c1L8 = {'Body': BytesIO(f.read())}

    path = os.path.join(os.path.dirname(__file__), f'fixtures/LC81781192017016LGN00_MTL.json')
    with open(path, 'rb') as f:
        L8 = {'Body': BytesIO(f.read())}

    session.return_value.client.return_value.get_object.side_effect = [c1L8, L8]

    list_directory.side_effect = [
        ['c1/L8/178/119/LC08_L1GT_178119_20180103_20180103_01_RT/'],
        ['L8/178/119/LC81781192017016LGN00/']]

    path = '178'
    row = '119'
    full = True

    assert list(search.landsat(path, row, full))
    assert session.return_value.client.return_value.get_object.call_count == 2
    assert list_directory.call_count == 2


@patch('aws_sat_api.search.boto3_session')
@patch('aws_sat_api.aws.list_directory')
def test_cbers_valid(list_directory, session):
    """Should work as expected
    """

    session.return_value.client.return_value = True
    list_directory.return_value = [
        'CBERS4/MUX/217/063/CBERS_4_MUX_20160416_217_063_L2/']

    path = '217'
    row = '063'

    expected = [{
        'acquisition_date': '20160416',
        'key': 'CBERS4/MUX/217/063/CBERS_4_MUX_20160416_217_063_L2',
        'path': '217',
        'processing_level': 'L2',
        'row': '063',
        'satellite': 'CBERS',
        'scene_id': 'CBERS_4_MUX_20160416_217_063_L2',
        'sensor': 'MUX',
        'thumbURL':
            'https://s3.amazonaws.com/cbers-meta-pds/CBERS4/MUX/217/063/CBERS_4_MUX_20160416_217_063_L2/CBERS_4_MUX_20160416_217_063_small.jpeg',
        'browseURL':
            'https://s3.amazonaws.com/cbers-meta-pds/CBERS4/MUX/217/063/CBERS_4_MUX_20160416_217_063_L2/CBERS_4_MUX_20160416_217_063.jpg',
        'version': '4'}]

    assert list(search.cbers(path, row)) == expected
