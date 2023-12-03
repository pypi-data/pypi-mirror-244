import os
import typer
from mako.template import Template


app = typer.Typer()


@app.command()
def init(project_name: str = "Default"):
    """
    Create a new project with the given name.
    """
    # Check if the project directory exists
    project_dir = os.path.join(os.getcwd(), project_name)
    if os.path.exists(project_dir):
        typer.echo(f"Error: Project '{project_name}' already exists.")
        raise typer.Abort()

    # Create project directory
    os.makedirs(project_dir)

    # Create files using Mako templates
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    for root, _, files in os.walk(templates_dir):
        for file in files:
            template_path = os.path.join(root, file)
            output_file = os.path.relpath(template_path, templates_dir)
            output_file = Template(output_file).render(project_name=project_name)

            # Change the file extension as needed
            output_file = output_file.replace('.mako', '')  # Remove .mako extension

            output_path = os.path.join(project_dir, output_file)

            with open(template_path, 'r') as template_file, open(output_path, 'w') as output:
                template = Template(template_file.read())
                output.write(template.render(project_name=project_name))

    typer.echo(f"Project '{project_name}' created successfully.")


if __name__ == "__main__":
    app()
