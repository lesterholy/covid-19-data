import click

from cowidev import PATHS
from cowidev.cmd.commons.utils import OrderedGroup, feedback_log
from cowidev.oxcgrt.etl import run_etl
from cowidev.oxcgrt.grapher import run_grapheriser


@click.group(name="oxcgrt", chain=True, cls=OrderedGroup)
@click.pass_context
def click_oxcgrt(ctx):
    """COVID-19 stringency index (by OxCGRT) data pipeline."""
    pass


@click.command(name="get", short_help="Step 1: Download OxCGRT data.")
@click.pass_context
def click_oxcgrt_get(ctx):
    """Downloads all OxCGRT source files into project directory."""
    feedback_log(
        func=run_etl,
        output_path=PATHS.INTERNAL_INPUT_BSG_FILE,
        output_path_diff=PATHS.INTERNAL_INPUT_BSG_DIFF_FILE,
        server=ctx.obj["server"],
        domain="OxCGRT",
        step="get",
        hide_success=True,
    )


@click.command(name="grapher-io", short_help="Step 2: Generate grapher-ready files.")
@click.pass_context
def click_oxcgrt_grapher(ctx):
    feedback_log(
        func=run_grapheriser,
        input_path=PATHS.INTERNAL_INPUT_BSG_FILE,
        input_path_country_std=PATHS.INTERNAL_INPUT_BSG_STD_FILE,
        output_path=PATHS.INTERNAL_GRAPHER_BSG_FILE,
        server=ctx.obj["server"],
        domain="OxCGRT",
        step="grapher-io",
        text_success="Grapher files were correctly generated.",
    )


click_oxcgrt.add_command(click_oxcgrt_get)
click_oxcgrt.add_command(click_oxcgrt_grapher)
