import os
import sys
import click
from .Context import Context
from .Project import Project

context = None

@click.group()
def main():
    global context
    cwd = os.getcwd()
    project = Project.from_nearby(cwd)

    if project is None:
        click.echo("Could not find a Monkeyfile", err=True)
        sys.exit(1)
        return

    context = Context(project)

@main.command()
@click.argument("paths", nargs=-1)
def see(paths):
    """
    Scans all of the files in the project directory.
    """
    context.command("see", paths)

@main.command()
@click.argument("paths", nargs=-1)
def hear(paths):
    """
    Provide feedback and discussion on the project.
    """
    context.command("hear", paths)

@main.command(name="do")
@click.argument("paths", nargs=-1)
def _do(paths):
    """
    Perform a tasks in the project.
    """
    context.command("do", paths)

@main.command()
@click.argument("paths", nargs=-1)
@click.option("--project", is_flag=True, default=False)
def forget(paths, project):
    """
    Remove a file from the project.
    """
    if project:
        print("Forgetting the entire project")
        context.project.trash()
        return
    
    if not paths:
        print("No paths provided. If you want to forget the entire project, use --project")
        return

if __name__ == '__main__':
    main()