"""Console script for massdevextractor"""
import click

from massdevextractor import core


@click.command()
@click.argument("filename", default="massdevchart.json", type=click.Path())
def main(filename: str):
    """extract mass dev chart"""
    core.main(filename)
