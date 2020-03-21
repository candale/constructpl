import click

from . import __version__
from .core import build_docx_context_from_cli, load_docxtpl_file, save_rendered


@click.group()
def ctpl():
    pass


@ctpl.command()
def version():
    click.echo(__version__)


@ctpl.command()
@click.argument('file_path', type=str)
@click.argument('output_path', type=str)
def render(file_path, output_path):
    doc = load_docxtpl_file(file_path)
    context = build_docx_context_from_cli(doc)
    save_rendered(doc, context, output_path)


if __name__ == '__main__':
    ctpl()
