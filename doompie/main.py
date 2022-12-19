import click

from doompie import WAD, Map
from doompie.render import render


@click.command()
@click.argument(
    'path_to_wad',
)
def main(
    path_to_wad,
):
    with open(path_to_wad, 'rb') as fh:
        wad_data = fh.read()
    wad = WAD(wad_data)
    click.echo(click.style('Allowed maps:'.upper(), fg='green', bold=True))
    click.echo('- ' + '\n- '.join(wad.maps))
    value: str = click.prompt('Select map', type=str)
    map = Map(value.upper(), wad=wad)
    render(map)



