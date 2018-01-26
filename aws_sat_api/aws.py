"""aws_sat_api.aws"""

import os

from boto3.session import Session as boto3_session

region = os.environ.get('AWS_REGION', 'us-east-1')


def list_directory(bucket, prefix, s3=None, request_pays=False):
    """AWS s3 list directory
    """
    if not s3:
        session = boto3_session(region_name=region)
        s3 = session.client('s3')

    pag = s3.get_paginator('list_objects_v2')

    params = {
        'Bucket': bucket,
        'Prefix': prefix,
        'Delimiter': '/'}

    if request_pays:
        params['RequestPayer'] = 'requester'

    directories = []
    for subset in pag.paginate(**params):
        if 'CommonPrefixes' in subset.keys():
            directories.extend(subset.get('CommonPrefixes'))

    return [r['Prefix'] for r in directories]


def get_object(bucket, key, s3=None, request_pays=False):
    """AWS s3 get object content
    """
    if not s3:
        session = boto3_session(region_name=region)
        s3 = session.client('s3')

    params = {
        'Bucket': bucket,
        'Key': key}

    if request_pays:
        params['RequestPayer'] = 'requester'

    response = s3.get_object(**params)
    return response['Body'].read()
