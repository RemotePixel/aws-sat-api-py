"""aws_sat_api.utils"""

import os
import re
import datetime

from aws_sat_api.errors import (InvalidLandsatSceneId, InvalidCBERSSceneId)


def landsat_parse_scene_id(sceneid):
    """Parse Landsat-8 scene id
    Author @perrygeo - http://www.perrygeo.com
    """
    pre_collection = r'(L[COTEM]8\d{6}\d{7}[A-Z]{3}\d{2})'
    collection_1 = r'(L[COTEM]08_L\d{1}[A-Z]{2}_\d{6}_\d{8}_\d{8}_\d{2}_(T1|T2|RT))'
    if not re.match('^{}|{}$'.format(pre_collection, collection_1), sceneid):
        raise InvalidLandsatSceneId('Could not match {}'.format(sceneid))

    precollection_pattern = (
        r'^L'
        r'(?P<sensor>\w{1})'
        r'(?P<satellite>\w{1})'
        r'(?P<path>[0-9]{3})'
        r'(?P<row>[0-9]{3})'
        r'(?P<acquisitionYear>[0-9]{4})'
        r'(?P<acquisitionJulianDay>[0-9]{3})'
        r'(?P<groundStationIdentifier>\w{3})'
        r'(?P<archiveVersion>[0-9]{2})$')

    collection_pattern = (
        r'^L'
        r'(?P<sensor>\w{1})'
        r'(?P<satellite>\w{2})'
        r'_'
        r'(?P<correction_level>\w{4})'
        r'_'
        r'(?P<path>[0-9]{3})'
        r'(?P<row>[0-9]{3})'
        r'_'
        r'(?P<acquisition_date>[0-9]{4}[0-9]{2}[0-9]{2})'
        r'_'
        r'(?P<ingestion_date>[0-9]{4}[0-9]{2}[0-9]{2})'
        r'_'
        r'(?P<collection>\w{2})'
        r'_'
        r'(?P<category>\w{2})$')

    meta = None
    for pattern in [collection_pattern, precollection_pattern]:
        match = re.match(pattern, sceneid, re.IGNORECASE)
        if match:
            meta = match.groupdict()
            break

    if meta.get('acquisitionJulianDay'):
        date = datetime.datetime(int(meta['acquisitionYear']), 1, 1) \
            + datetime.timedelta(int(meta['acquisitionJulianDay']) - 1)
        meta['acquisition_date'] = date.strftime('%Y%m%d')
        meta['category'] = 'pre'

    collection = meta.get('collection', '')
    if collection != '':
        collection = 'c{}'.format(int(collection))

    meta['scene_id'] = sceneid
    meta['satellite'] = 'L{}'.format(meta['satellite'].lstrip('0'))
    meta['key'] = os.path.join(collection, 'L8', meta['path'], meta['row'], sceneid, sceneid)

    return meta


def cbers_parse_scene_id(sceneid):
    """Parse CBERS scene id"""

    if not re.match('^CBERS_4_MUX_[0-9]{8}_[0-9]{3}_[0-9]{3}_L[0-9]$', sceneid):
        raise InvalidCBERSSceneId('Could not match {}'.format(sceneid))

    cbers_pattern = (
        r'(?P<satellite>\w{5})'
        r'_'
        r'(?P<version>[0-9]{1})'
        r'_'
        r'(?P<sensor>\w{3})'
        r'_'
        r'(?P<acquisition_date>[0-9]{4}[0-9]{2}[0-9]{2})'
        r'_'
        r'(?P<path>[0-9]{3})'
        r'_'
        r'(?P<row>[0-9]{3})'
        r'_'
        r'(?P<processing_level>L[0-9]{1})$')

    meta = None
    match = re.match(cbers_pattern, sceneid, re.IGNORECASE)
    if match:
        meta = match.groupdict()

    meta['scene_id'] = sceneid
    meta['key'] = 'CBERS4/MUX/{}/{}/{}'.format(meta['path'], meta['row'], sceneid)

    return meta


def zeroPad(n, l):
    """ Add leading 0
    """
    return str(n).zfill(l)
