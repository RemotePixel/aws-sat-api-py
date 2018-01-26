"""Errors and warnings"""


class SatApiError(Exception):
    """Base exception class"""


class InvalidLandsatSceneId(SatApiError):
    """Invalid Landsat-8 scene id"""


class InvalidSentinelSceneId(SatApiError):
    """Invalid Sentinel-2 scene id"""


class InvalidCBERSSceneId(SatApiError):
    """Invalid CBERS scene id"""
