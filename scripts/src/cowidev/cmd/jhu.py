import click

from cowidev.cmd.commons.utils import OrderedGroup, feedback_log
from cowidev.jhu.__main__ import download_csv, generate_dataset


@click.group(name="jhu", chain=True, cls=OrderedGroup)
@click.pass_context
def click_jhu(ctx):
    """COVID-19 Cases/Deaths data pipeline. [DEPRECATED]"""
    pass


@click.command(name="get", short_help="Step 1: Download JHU data.")
@click.pass_context
def click_jhu_download(ctx):
    """Downloads all JHU source files into project directory."""
    feedback_log(
        func=download_csv,
        server=ctx.obj["server"],
        domain="JHU",
        step="get",
        hide_success=True,
        logger=ctx.obj["logger"],
    )


@click.command(name="generate", short_help="Step 2: Generate dataset.")
@click.pass_context
def click_jhu_generate(ctx):
    feedback_log(
        func=generate_dataset,
        server=ctx.obj["server"],
        server_mode=ctx.obj["server"],
        domain="JHU",
        step="generate",
        text_success="Public data files generated.",
        logger=ctx.obj["logger"],
        skip_download=True,
    )


click_jhu.add_command(click_jhu_download)
click_jhu.add_command(click_jhu_generate)
