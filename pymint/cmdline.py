import json
import os
import pathlib
from pathlib import Path
from typing import List

import click
import networkx as nx
import pyfiglet

from pymint.mintdevice import MINTDevice

OUTPUT_DIR = pathlib.Path(os.getcwd())


def print_version(ctx, param, value):

    if not value or ctx.resilient_parsing:
        return

    import pkg_resources

    click.echo(pkg_resources.get_distribution("pymint").version)
    ctx.exit()


def convert_to_parchmint(
    input_file: Path,
    outpath: Path,
    skip_constraints: bool = True,
    generate_graph_view: bool = False,
):
    """
    Convert a .mint file to a .parchmint.json file
    """
    extension = input_file.suffix
    if extension == ".mint" or extension == ".uf":
        current_device = MINTDevice.from_mint_file(str(input_file), skip_constraints)

        # Save the device parchmint v1_2 to a file
        parchmint_text = current_device.to_parchmint()

        # Create new file in outpath with the same name as the current device
        outpath.mkdir(parents=True, exist_ok=True)
        with open(str(outpath.joinpath(input_file.stem + ".json")), "w") as f:
            print("Writing to file: {}".format(f.name))

            json.dump(parchmint_text, f, indent=4)

        # Generate a graph view of the device
        if generate_graph_view:
            printgraph(current_device.device.graph, current_device.device.name)
    else:
        raise Exception("Unsupported file extension: {}".format(extension))


def printgraph(G, filename: str) -> None:
    tt = pathlib.Path(OUTPUT_DIR).joinpath(filename + ".dot")
    print("output:", str(tt.absolute()))
    nx.nx_agraph.to_agraph(G).write(str(tt.absolute()))

    os.system(
        "dot -Tpdf {} -o {}.pdf".format(
            str(tt.absolute()), pathlib.Path(OUTPUT_DIR).joinpath(tt.stem)
        )
    )


@click.command()
@click.option(
    "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True
)
@click.argument(
    "input_files",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--outpath",
    "-o",
    default=".",
    help="This is the output directory",
    type=click.Path(exists=False, path_type=Path),
)
@click.option(
    "--skip-layout-constraints",
    type=click.BOOL,
    default=False,
    is_flag=True,
    help="Sets the flag to skip layout constraints",
)
@click.option(
    "--generate-graph-view",
    type=click.BOOL,
    default=False,
    is_flag=True,
    help="Sets the flag to generate the graph",
)
def default_cli(
    input_files: List[Path],
    outpath: Path,
    skip_layout_constraints: bool,
    generate_graph_view: bool,
):
    ascii_banner = pyfiglet.figlet_format("MINT")
    print(ascii_banner)

    for input_file in input_files:
        convert_to_parchmint(
            input_file=input_file,
            outpath=outpath,
            skip_constraints=skip_layout_constraints,
            generate_graph_view=generate_graph_view,
        )


if __name__ == "__main__":
    default_cli()
