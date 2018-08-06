"""CLI."""

import re
import json

import click

from aws_sat_api import search


@click.group(short_help="AWS Satellite API")
def awssat():
    """Search."""
    pass


class CustomType:
    """Click CustomType."""

    class PathRow(click.ParamType):
        """PathRow."""

        name = "pathrow"

        def convert(self, value, param, ctx):
            """Validate and parse path-row."""
            try:
                pr = [x for x in value.split(",")]
                assert all(re.match(r'\d+-\d+', b) for b in pr)
                return pr

            except (ValueError, AttributeError, AssertionError):
                raise click.ClickException(
                    "pathrow."
                )

    pathrow = PathRow()

    class S2Tile(click.ParamType):
        """PathRow."""

        name = "s2tile"

        def convert(self, value, param, ctx):
            """Validate and parse sentineltile."""
            try:
                pr = [x for x in value.split(",")]
                assert all(re.match(r'[0-9]{2}\w{1}\w{2}', b) for b in pr)
                return pr

            except (ValueError, AttributeError, AssertionError):
                raise click.ClickException(
                    "tile."
                )

    s2tile = S2Tile()


@awssat.command(name="landsat")
@click.option(
    "--path",
    "-p",
    type=str,
    help="path",
)
@click.option(
    "--row",
    "-r",
    type=str,
    help="row",
)
@click.option(
    "--pathrow",
    "-pr",
    type=CustomType.pathrow,
    help="path-row",
)
@click.option(
    "--full/--simple",
    default=True,
    help="full"
)
def landsat(
    path,
    row,
    pathrow,
    full,
):
    """Landsat search CLI."""
    # TODO: add tests for pathrow and path+row options
    if pathrow:
        pr_info = [dict(path=x.split('-')[0], row=x.split('-')[1]) for x in pathrow]
    else:
        pr_info = [dict(path=path, row=row)]

    for el in pr_info:
        for scene in search.landsat(**el, full=full):
            click.echo(json.dumps(scene))


@awssat.command(name="sentinel")
@click.option(
    "--utm",
    "-u",
    type=str,
    help="utm",
)
@click.option(
    "--lat",
    "-l",
    type=str,
    help="lat",
)
@click.option(
    "--grid",
    "-g",
    type=str,
    help="grid",
)
@click.option(
    "--tile",
    "-t",
    type=CustomType.s2tile,
    help="tile",
)
@click.option(
    "--level",
    type=click.Choice(['l1c', 'l2a']),
    default='l1c',
    help="level",
)
@click.option(
    "--full/--simple",
    default=True,
    help="full"
)
def sentinel(
    utm,
    lat,
    grid,
    tile,
    level,
    full,
):
    """Sentinel search CLI."""
    # TODO: add tests for tile and utm+grid+lat options
    if tile:
        sentinel_pattern = r'^(?P<utm>[0-9]{1,2})(?P<lat>\w{1})(?P<grid>\w{2})$'
        tile_info = [
            re.match(sentinel_pattern, x, re.IGNORECASE).groupdict()
            for x in tile
        ]
    else:
        tile_info = [dict(utm=utm, lat=lat, grid=grid)]

    for el in tile_info:
        for scene in search.sentinel2(**el, level=level, full=full):
            click.echo(json.dumps(scene))


@awssat.command(name="cbers")
@click.option(
    "--path",
    "-p",
    type=str,
    help="path",
)
@click.option(
    "--row",
    "-r",
    type=str,
    help="row",
)
@click.option(
    "--pathrow",
    "-pr",
    type=CustomType.pathrow,
    help="path-row",
)
@click.option(
    "--sensor",
    "-s",
    type=click.Choice(["MUX", "AWFI", "PAN5M", "PAN10M"]),
    default="MUX",
    help="CBERS4 sensor",
)
def cbers(
    path,
    row,
    pathrow,
    sensor,
):
    """CBERS search CLI."""
    # TODO: add tests for pathrow and path+row options
    if pathrow:
        pr_info = [dict(path=x.split('-')[0], row=x.split('-')[1]) for x in pathrow]
    else:
        pr_info = [dict(path=path, row=row)]

    for el in pr_info:
        for scene in search.cbers(**el, sensor=sensor):
            click.echo(json.dumps(scene))
