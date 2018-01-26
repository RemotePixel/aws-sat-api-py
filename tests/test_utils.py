"""tests aws_sat_api.utils"""

import pytest

from aws_sat_api import utils
from aws_sat_api.errors import (InvalidLandsatSceneId, InvalidCBERSSceneId)


def test_landsat_id_pre_invalid():
    """
    Should raise an error with invalid sceneid
    """

    scene = 'L0300342017083LGN00'
    with pytest.raises(InvalidLandsatSceneId):
        utils.landsat_parse_scene_id(scene)


def test_landsat_id_c1_invalid():
    """
    Should raise an error with invalid sceneid
    """

    scene = 'LC08_005004_20170410_20170414_01_T1'
    with pytest.raises(InvalidLandsatSceneId):
        utils.landsat_parse_scene_id(scene)


def test_landsat_id_pre_valid():
    """
    Should work as expected (parse landsat pre sceneid)
    """

    scene = 'LC80300342017083LGN00'
    expected_content = {
        'acquisitionJulianDay': '083',
        'acquisitionYear': '2017',
        'archiveVersion': '00',
        'category': 'pre',
        'acquisition_date': '20170324',
        'groundStationIdentifier': 'LGN',
        'key': 'L8/030/034/LC80300342017083LGN00/LC80300342017083LGN00',
        'path': '030',
        'row': '034',
        'satellite': 'L8',
        'scene_id': 'LC80300342017083LGN00',
        'sensor': 'C'}

    assert utils.landsat_parse_scene_id(scene) == expected_content


def test_landsat_id_c1_valid():
    """
    Should work as expected (parse landsat c1 sceneid)
    """

    scene = 'LC08_L1TP_005004_20170410_20170414_01_T1'
    expected_content = {
        'category': 'T1',
        'collection': '01',
        'acquisition_date': '20170410',
        'key': 'c1/L8/005/004/LC08_L1TP_005004_20170410_\
20170414_01_T1/LC08_L1TP_005004_20170410_20170414_01_T1',
        'path': '005',
        'correction_level': 'L1TP',
        'ingestion_date': '20170414',
        'row': '004',
        'satellite': 'L8',
        'scene_id': 'LC08_L1TP_005004_20170410_20170414_01_T1',
        'sensor': 'C'}

    assert utils.landsat_parse_scene_id(scene) == expected_content


def test_cbers_id_invalid():
    """
    Should raise an error with invalid sceneid
    """

    scene = 'CBERS_4_MUX_20171121_057_094'
    with pytest.raises(InvalidCBERSSceneId):
        utils.cbers_parse_scene_id(scene)


def test_cbers_id_valid():
    """
    Should work as expected (parse cbers scene id)
    """

    scene = 'CBERS_4_MUX_20171121_057_094_L2'
    expected_content = {
        'acquisition_date': '20171121',
        'sensor': 'MUX',
        'key': 'CBERS4/MUX/057/094/CBERS_4_MUX_20171121_057_094_L2',
        'path': '057',
        'processing_level': 'L2',
        'row': '094',
        'version': '4',
        'scene_id': 'CBERS_4_MUX_20171121_057_094_L2',
        'satellite': 'CBERS'}

    assert utils.cbers_parse_scene_id(scene) == expected_content


def test_zeroPad_valid():
    assert utils.zeroPad(3, 4) == '0003'


def test_zeroPad_validString():
    assert utils.zeroPad('3', 2) == '03'
