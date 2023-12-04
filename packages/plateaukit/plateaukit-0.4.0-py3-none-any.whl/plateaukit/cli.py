import glob
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path

import click
from loguru import logger
from prettytable import PrettyTable
from rich.console import Console

from plateaukit import extractors, generators
from plateaukit.config import Config
from plateaukit.download import downloader


def is_dataset_installed(dataset_id, format):
    config = Config()
    path = config.datasets.get(dataset_id, {}).get(format)
    return True if path else False
    # return path and Path(path).exists()


def list_available_datasets(is_all=False):
    from plateaukit.download import city_list

    table = PrettyTable()
    table.field_names = ["id", "name", "version", "homepage"]
    table.add_row(["all", "(全都市)", "", ""])
    for city in city_list:
        if city.get("latest", False) or is_all:
            table.add_row(
                [
                    city["dataset_id"],
                    city["city_name"],
                    city["version"],
                    city["homepage"],
                ]
            )
    print(table)


# def setup_property_db(infiles, db_filename):
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     run_async(extractors.commands.extract_properties(expanded_infiles, db_filename))


# https://alexdelorenzo.dev/notes/click.html
class OrderCommands(click.Group):
    def list_commands(self, ctx):
        return list(self.commands)


@click.group(
    cls=OrderCommands,
    context_settings=dict(help_option_names=["-h", "--help"]),
    no_args_is_help=True,
)
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Enable verbose mode."
)
def cli(verbose):
    if verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.remove()


@cli.command("list")
@click.option(
    "--local", is_flag=True, default=False, help="Show installed datasets only."
)
@click.option(
    "--all",
    is_flag=True,
    default=False,
    help="Show all versions of datasets including old ones.",
)
def list_cmd(local, all):
    """List available and installed PLATEAU datasets."""
    from plateaukit.download import city_list

    config = Config()

    if local:
        table = PrettyTable()
        table.field_names = ["id", "name", "homepage", "formats"]
        for dataset_id, record in config.datasets.items():
            city = next(
                filter(lambda x: x["dataset_id"] == dataset_id, city_list), None
            )
            if not city:
                continue
            table.add_row(
                [
                    dataset_id,
                    city["city_name"],
                    city["homepage"],
                    " ".join([x for x in ["citygml", "3dtiles"] if x in record]),
                ]
            )
        print(table)
        return
    else:
        list_available_datasets(is_all=all)
        return


@cli.command("install")
@click.argument("dataset_id", nargs=1, required=False)
@click.option(
    "--format",
    type=click.Choice(["citygml", "3dtiles"], case_sensitive=False),
    default="citygml",
)
@click.option("--local", help="Install local file. (without copying)")
@click.option("--force", is_flag=True, default=False, help="Force install.")
@click.option("--download-only", is_flag=True, default=False)
@click.option("-l", "--list", is_flag=True, help="List all latest available datasets.")
@click.option(
    "--list-all", is_flag=True, help="List all available datasets including old ones."
)
def install_cmd(dataset_id, format, local, force, download_only, list, list_all):
    """Download and install PLATEAU datasets."""
    from plateaukit.download import city_list

    if not dataset_id and not (list or list_all):
        raise click.UsageError("Missing argument/option: dataset_id or -l/--list")

    if list or list_all:
        list_available_datasets(is_all=list_all)
        return

    if dataset_id:
        city = next(filter(lambda x: x["dataset_id"] == dataset_id, city_list), None)

        if not city:
            raise click.UsageError("Invalid dataset name")

        if local:
            local = Path(local).resolve()
            if not local.exists():
                raise click.UsageError("Local file not found")
            # print(local)
            config = Config()
            config.datasets[dataset_id][format] = local
            config.save()
            return
        else:
            # Abort if a dataset is already installed
            installed = is_dataset_installed(dataset_id, format)
            if not force and installed:
                click.echo(
                    f'ERROR: Dataset "{dataset_id}" ({format}) is already installed.',
                    err=True,
                )
                exit(-1)
            resource_id = city[format]
            # print(dataset_id, resource_id)
            config = Config()
            destfile_path = downloader.download_resource(
                resource_id, dest=config.data_dir
            )
            config.datasets[dataset_id][format] = destfile_path
            config.save()
            return


@cli.command("uninstall")
@click.argument("dataset_id", nargs=1, required=False)
@click.option(
    "--format",
    type=click.Choice(["citygml", "3dtiles"], case_sensitive=False),
    default="citygml",
)
@click.option("--keep-files", is_flag=True, default=False)
def uninstall_cmd(dataset_id, format, keep_files):
    """Uninstall PLATEAU datasets."""
    if not dataset_id:
        raise Exception("Missing argument")

    if not keep_files:
        config = Config()
        path = config.datasets[dataset_id][format]
        if not path:
            raise RuntimeError("Missing files in record")
        if click.confirm(f'Delete "{path}"?'):
            os.remove(path)

    config = Config()
    del config.datasets[dataset_id][format]
    if len(config.datasets[dataset_id].items()) == 0:
        del config.datasets[dataset_id]
    config.save()


@cli.command("prebuild")
@click.argument("dataset_id", nargs=1, required=True)
def prebuild(dataset_id):
    """Prebuild PLATEAU datasets."""

    import geopandas as gpd
    import pandas as pd
    from pyogrio import read_dataframe, write_dataframe

    console = Console()

    if not dataset_id:
        raise Exception("Missing argument: dataset_id")

    config = Config()
    record = config.datasets.get(dataset_id)
    # print(dataset_id, record)

    # TODO: All types
    type = "bldg"

    with tempfile.TemporaryDirectory() as tdir:
        outfile = Path(tdir, f"{dataset_id}.{type}.geojson")

        _generate_geojson(
            None,
            outfile,
            dataset_id,
            type,
            10,
            progress={"description": "Generating GeoJSON files..."},
        )

        with console.status("Writing GeoPackage...") as status:
            df = gpd.GeoDataFrame()

            for filename in glob.glob(str(Path(tdir, "*.geojson"))):
                subdf = read_dataframe(filename)
                df = pd.concat([df, subdf])

            # click.echo("Writing GeoPackage...")
            dest_path = Path(config.data_dir, f"{dataset_id}.gpkg")
            write_dataframe(df, dest_path, driver="GPKG")

            config.datasets[dataset_id]["gpkg"] = dest_path
            config.save()

        console.print("Writing GeoPackage... [green]Done")

        # click.echo(f"\nCreated: {dest_path}")


@cli.command("generate-cityjson")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
@click.option("--dataset", help='Dataset ID (e.g. "plateau-tokyo23ku")')
@click.option("--split", default=10)
# # @click.option(
# #     "--precision",
# #     help="Number of decimal places to keep for geometry vertices (default: 16).",
# )
def generate_cityjson(infiles, outfile, dataset, split):
    """Generate CityJSON from PLATEAU datasets."""
    # print(infiles)

    if not infiles and not dataset:
        raise click.UsageError("Missing argument/option: infiles or --dataset")

    if infiles and dataset:
        raise click.UsageError("Too many argument")

    params = {}

    # if precision:
    #     params["precision"] = precision

    type = "bldg"

    if dataset:
        with tempfile.TemporaryDirectory() as tdir:
            config = Config()
            record = config.datasets[dataset]
            if "citygml" not in record:
                raise Exception("Missing CityGML data")
            file_path = Path(record["citygml"])
            # TODO: fix
            pat = re.compile(rf".*udx\/{type}\/.*\.gml$")
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path) as f:
                    namelist = f.namelist()
                    targets = list(filter(lambda x: pat.match(x), namelist))
                    # print(targets, tdir)
                    f.extractall(tdir, members=targets)
                    # TODO: fix
                    infiles = [
                        str(Path(tdir, Path(file_path).stem, "udx", type, "*.gml"))
                    ]
            else:
                infiles = [str(Path(file_path, "udx", type, "*.gml"))]
            logger.debug([infiles, outfile])

            expanded_infiles = []
            for infile in infiles:
                expanded_infiles.extend(glob.glob(infile))

            expanded_infiles = sorted(expanded_infiles)

            # print(infiles, expanded_infiles)

            generators.simplecityjson.cityjson_from_gml(
                expanded_infiles,
                outfile,
                split=split,
                lod=[1],
            )

            # with open(outfile, "w") as f:
            #     json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    else:
        generators.simplecityjson.cityjson_from_gml(infiles, outfile, **params)
        # with open(outfile, "w") as f:
        #     json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def _generate_geojson(infiles, outfile, dataset: str, type: str, split: int, **kwargs):
    """Generate GeoJSON from PLATEAU datasets."""

    if not infiles and not dataset:
        raise click.UsageError("Missing argument: infiles or dataset")

    if infiles and dataset:
        raise click.UsageError("Too many arguments")

    # NOTE: this is intentional but to be refactored in the future
    with tempfile.TemporaryDirectory() as tdir:
        if dataset:
            if not type:
                raise Exception("Missing type")
            config = Config()
            record = config.datasets[dataset]
            if "citygml" not in record:
                raise Exception("Missing CityGML data")
            file_path = Path(record["citygml"])
            # TODO: fix
            pat = re.compile(rf".*udx\/{type}\/.*\.gml$")
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path) as f:
                    namelist = f.namelist()
                    targets = list(filter(lambda x: pat.match(x), namelist))
                    # print(targets, tdir)
                    f.extractall(tdir, members=targets)
                    # TODO: fix
                    infiles = [
                        str(Path(tdir, Path(file_path).stem, "udx", type, "*.gml"))
                    ]
            else:
                infiles = [str(Path(file_path, "udx", type, "*.gml"))]
            logger.debug([infiles, outfile])

        expanded_infiles = []
        for infile in infiles:
            expanded_infiles.extend(glob.glob(infile))

        expanded_infiles = sorted(expanded_infiles)

        if type == "bldg":
            generators.geojson_from_gml(
                expanded_infiles,
                outfile,
                split=split,
                lod=[0],
                altitude=True,
                allow_geometry_collection=False,
                **kwargs,
            )
        elif type == "brid":
            generators.geojson_from_gml(
                expanded_infiles,
                outfile,
                split=split,
                lod=[1],
                attributes=[],
                altitude=True,
                allow_geometry_collection=True,
                **kwargs,
            )
        elif type == "dem":
            # TODO: implement
            raise NotImplementedError("dem")
        elif type == "fld":
            raise NotImplementedError("fld")
        elif type == "lsld":
            raise NotImplementedError("lsld")
        elif type == "luse":
            raise NotImplementedError("luse")
            # generate.geojson_from_gml(
            #     expanded_infiles,
            #     outfile,
            #     split=split,
            #     lod=[1],
            #     attributes=[],
            #     altitude=True,
            #     allow_geometry_collection=True,
            # )
        elif type == "tran":
            generators.geojson_from_gml(
                expanded_infiles,
                outfile,
                split=split,
                lod=[1],
                attributes=[],
                altitude=True,  # TODO: can be False
                allow_geometry_collection=True,
                **kwargs,
            )
        elif type == "urf":
            raise NotImplementedError("urf")
            # generate.geojson_from_gml(
            #     expanded_infiles,
            #     outfile,
            #     split=split,
            #     lod=[0],
            #     attributes=[],
            #     altitude=True,
            #     allow_geometry_collection=False,
            # )
        else:
            raise NotImplementedError(type)


@cli.command("generate-geojson")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
@click.option("--dataset", help='Dataset ID (e.g. "plateau-tokyo23ku")')
@click.option(
    "--type",
    "-t",
    type=click.Choice(
        ["bldg", "brid", "dem", "fld", "frn", "lsld", "luse", "tran", "urf"],
        case_sensitive=True,
    ),
    default="bldg",
)
@click.option("--split", default=10)
def generate_geojson(infiles, outfile, dataset: str, type: str, split: int):
    """Generate GeoJSON from PLATEAU datasets."""

    _generate_geojson(infiles, outfile, dataset, type, split)


# @cli.command("generate-gpkg")
# @click.argument("infiles", nargs=-1, required=True)
# @click.argument("outfile", nargs=1, required=True)
# def generate_gpkg(infiles, outfile):
#     """Generate GeoPackage from PLATEAU GeoJSON."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     generators.utils.geojson_to_gpkg(expanded_infiles, outfile)


@cli.command("generate-qmesh")
@click.argument("infiles", nargs=-1)
@click.argument("outfile", nargs=1, required=True)
def generate_qmesh(infiles, outfile):
    """Generate Quantized Mesh from PLATEAU datasets."""
    generators.triangles_from_gml(infiles)


# @cli.command("generate-heightmap")
# @click.argument("infiles", nargs=-1)
# @click.argument("outfile", nargs=1, required=True)
# def generate_heightmap(infiles, outfile):
#     """Generate GeoTIFF heightmap from PLATEAU CityGML."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     generators.triangles_from_gml(expanded_infiles)


# @cli.command("extract-properties")
# @click.argument("infiles", nargs=-1, required=True)
# @click.argument("outfile", nargs=1, required=True)
# def extract_properties(infiles, outfile):
#     """Extract properties from PLATEAU CityGML."""
#     expanded_infiles = []
#     for infile in infiles:
#         expanded_infiles.extend(glob.glob(infile))
#     run_async(extractors.commands.extract_properties(expanded_infiles, outfile))


@cli.command("info")
def info_cmd():
    """Show PlateauKit configuration information."""
    import importlib.metadata
    import json

    try:
        __version__ = importlib.metadata.version("plateaukit")
    except importlib.metadata.PackageNotFoundError:
        __version__ = "unknown"

    config = Config()
    click.echo(f"Version: {__version__}")
    click.echo(f"Config path: {config.path}")
    click.echo(f"Data directory: {config.data_dir}")
    click.echo(f"{json.dumps(config.datasets, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    cli()
