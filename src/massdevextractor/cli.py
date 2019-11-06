"""Console script for massdevextractor"""
import click

from massdevextractor import core


@click.command()
def main():
    """extract mass dev chart"""
    core.main()
