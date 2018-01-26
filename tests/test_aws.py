"""tests aws_sat_api.aws"""

from io import BytesIO

import pytest

from mock import patch
from botocore.exceptions import ClientError

from aws_sat_api import aws


@pytest.fixture(autouse=True)
def testing_env_var(monkeypatch):
    # This is optional (just make sure we don't hit aws)
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'foo')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'bar')
    monkeypatch.delenv('AWS_PROFILE', raising=False)
    monkeypatch.setenv('AWS_CONFIG_FILE', '/tmp/asdfasdfaf/does/not/exist')
    monkeypatch.setenv('AWS_SHARED_CREDENTIALS_FILE',
                       '/tmp/asdfasdfaf/does/not/exist2')


@patch('aws_sat_api.aws.boto3_session')
def test_aws_list_directory_valid(session):
    """Should work as expected
    """

    session.return_value.client.return_value.get_paginator.return_value.paginate.return_value = [
        {'CommonPrefixes': [{'Prefix': 'L8/178/246/LC81782462014232LGN00/'}]}]

    bucket = "landsat-pds"
    prefix = "L8/178/246/"

    expected_value = [
        'L8/178/246/LC81782462014232LGN00/']

    assert aws.list_directory(bucket, prefix) == expected_value


@patch('aws_sat_api.aws.boto3_session.client')
def test_aws_list_directory_validClient(client):
    """Should work as expected
    """

    client.return_value.get_paginator.return_value.paginate.return_value = [
        {'CommonPrefixes': [{'Prefix': 'L8/178/246/LC81782462014232LGN00/'}]}]

    bucket = "landsat-pds"
    prefix = "L8/178/246/"

    expected_value = [
        'L8/178/246/LC81782462014232LGN00/']

    assert aws.list_directory(bucket, prefix, s3=client()) == expected_value


@patch('aws_sat_api.aws.boto3_session')
def test_aws_list_directory_validPays(session):
    """Should work as expected
    """

    session.return_value.client.return_value.get_paginator.return_value.paginate.return_value = [
        {'CommonPrefixes': [{'Prefix': 'L8/178/246/LC81782462014232LGN00/'}]}]

    bucket = "landsat-pds"
    prefix = "L8/178/246/"

    expected_value = ['L8/178/246/LC81782462014232LGN00/']

    assert aws.list_directory(bucket, prefix, request_pays=True) == expected_value
    pag = session.return_value.client.return_value.get_paginator.return_value.paginate
    assert pag.call_args[1].get('RequestPayer') == 'requester'


@patch('aws_sat_api.aws.boto3_session')
def test_aws_list_directory_nodir(session):
    """Should return an empty list
    """

    session.return_value.client.return_value.get_paginator.return_value.paginate.return_value = [{}]

    bucket = "landsat-pds"
    prefix = "L8/178/246/"

    assert not aws.list_directory(bucket, prefix)


@patch('aws_sat_api.aws.boto3_session')
def test_aws_list_directory_awserror(session):
    """Should raise an 'ClientError' error
    """

    session.return_value.client.return_value.get_paginator.return_value.paginate.side_effect = [
        ClientError({'Error': {'Code': 500, 'Message': 'Error'}}, 'list_objects_v2')]

    bucket = "landsat-pds"
    prefix = "L8/178/246/"

    with pytest.raises(ClientError):
        aws.list_directory(bucket, prefix)


@patch('aws_sat_api.aws.boto3_session')
def test_aws_get_object_valid(session):
    """Should work as expected
    """

    session.return_value.client.return_value.get_object.return_value = {'Body': BytesIO(b'0101010')}

    bucket = "landsat-pds"
    key = "L8/178/246/LC81782462014232LGN00/LC81782462014232LGN00_MTL.json"

    assert aws.get_object(bucket, key)


@patch('aws_sat_api.aws.boto3_session')
def test_aws_get_object_validPays(session):
    """Should work as expected
    """

    session.return_value.client.return_value.get_object.return_value = {'Body': BytesIO(b'0101010')}

    bucket = "landsat-pds"
    key = "L8/178/246/LC81782462014232LGN00/LC81782462014232LGN00_MTL.json"

    assert aws.get_object(bucket, key, request_pays=True)
    assert session.return_value.client.return_value.get_object.call_args[1].get('RequestPayer') == 'requester'


@patch('aws_sat_api.aws.boto3_session.client')
def test_aws_get_object_validClient(client):
    """Should work as expected
    """

    client.return_value.get_object.return_value = {'Body': BytesIO(b'0101010')}

    bucket = "landsat-pds"
    key = "L8/178/246/LC81782462014232LGN00/LC81782462014232LGN00_MTL.json"

    assert aws.get_object(bucket, key, s3=client())


@patch('aws_sat_api.aws.boto3_session')
def test_aws_get_object_awserror(session):
    """
    Should raise an 'ClientError' error
    """

    session.return_value.client.return_value.get_object.side_effect = ClientError({'Error': {
        'Code': 500, 'Message': 'Error'}}, 'get_object')

    bucket = "landsat-pds"
    key = "L8/178/246/LC81782462014232LGN00/LC81782462014232LGN00_MTL.json"

    with pytest.raises(ClientError):
        aws.get_object(bucket, key)
