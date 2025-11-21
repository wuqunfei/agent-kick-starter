import typer
from pathlib import Path
from typing import Optional

from services.init_service import TemplateInitializationService
from models.template import AgentFramework, CloudProvider

# Create a Typer instance for the init command group
init_app = typer.Typer(
    name="init",
    help="Initialize a new GenAI agent project from a template"
)


@init_app.callback()
def callback():
    """Initialize a new GenAI agent project from a template"""
    pass


@init_app.command("init")
def init_command(
    name: Optional[str] = typer.Argument(None, help="Name for the new agent project"),
    provider: Optional[str] = typer.Option(None, "--provider", help="Cloud provider (aws, azure, gcp)"),
    framework: Optional[str] = typer.Option(None, "--framework", help="Agent framework (microsoft, amazon, google, pydantic)"),
    template_version: Optional[str] = typer.Option(None, "--template-version", help="Version of the template to use")
):
    """
    Initialize a new GenAI agent project from a template.

    If provider or framework are not specified, the user will be prompted to select them.
    """
    # Initialize the service
    init_service = TemplateInitializationService()

    # Get project name
    if not name:
        name = typer.prompt("Enter project name")

    # Get provider
    if not provider:
        provider = typer.prompt("Enter cloud provider (aws, azure, gcp)", type=str)
        # Validate provider
        try:
            CloudProvider(provider.lower())
        except ValueError:
            typer.echo(f"Invalid cloud provider: {provider}")
            raise typer.Exit(code=2)  # Usage error

    # Get framework
    if not framework:
        framework = typer.prompt("Enter agent framework (microsoft, amazon, google, pydantic)", type=str)
        # Validate framework
        try:
            AgentFramework(framework.lower())
        except ValueError:
            typer.echo(f"Invalid agent framework: {framework}")
            raise typer.Exit(code=2)  # Usage error

    # Generate template ID based on framework, provider, and version
    version = template_version or "1.0.0"
    template_id = f"{framework.lower()}-{provider.lower()}-v{version}"

    # Initialize the project in the current directory
    current_dir = Path.cwd()
    success = init_service.initialize_project(
        project_name=name,
        template_id=template_id,
        target_directory=current_dir
    )

    if success:
        typer.echo(f"Successfully created project '{name}' using {framework} framework on {provider}")
        typer.echo(f"Template used: {template_id}")
        typer.echo(f"Project location: {current_dir / name}")
    else:
        typer.echo(f"Failed to initialize project '{name}'")
        raise typer.Exit(code=1)  # General error