import click
import argparse
from compute_distance.functions import compute_distance_debug
from compute_distance.functions import compute_distance


@click.command()
@click.option('--apath', '-a', 'admin_path', type = click.Path(exists = True, dir_okay = False), help = 'Path to admin0 file')
@click.option('--apath', '-v', 'vector_file_path', type = click.Path(exists = True, dir_okay = False), help = 'Path to vector file')
@click.option('--apath', '-r', 'raster_template_path', type = click.Path(exists = True, dir_okay = False), help = 'Path to raster template file')
@click.option('--apath', '-o', 'outdir_path', type = click.Path(exists = True, dir_okay = True), help = 'Path to output directory')
def cli_debug(admin_path, vector_file_path, raster_template_path, outdir_path) -> None:
    print('Start of Distance Computation Debug')
    compute_distance_debug(admin_path, vector_file_path, raster_template_path, outdir_path)

    pass



@click.command()
@click.option('--apath', '-a', 'admin_path', type = click.Path(exists = True, dir_okay = False), help = 'Path to admin0 file')
@click.option('--apath', '-v', 'vector_file_path', type = click.Path(exists = True, dir_okay = False), help = 'Path to vector file')
@click.option('--apath', '-r', 'raster_template_path', type = click.Path(exists = True, dir_okay = False), help = 'Path to raster template file')
@click.option('--apath', '-o', 'outdir_path', type = click.Path(exists = True, dir_okay = True), help = 'Path to output directory')
def cli(admin_path, vector_file_path, raster_template_path, outdir_path) -> None:
    print('Start of Distance Computation')
    compute_distance(admin_path, vector_file_path, raster_template_path, outdir_path)

    pass
