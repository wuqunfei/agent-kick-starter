import typer
from pathlib import Path
from typing import Optional

from services.init_service import TemplateInitializationService
from models.template import AgentFramework, CloudProvider


def run_init(
    name: Optional[str],
    provider: Optional[str],
    framework: Optional[str],
    template_version: Optional[str]
):
    init_service = TemplateInitializationService()

    if not name:
        name = typer.prompt("Project name", default="my-agent")

    if not framework:
        framework = typer.prompt("Agent framework (microsoft, amazon, google, pydantic)", default="microsoft")
    try:
        AgentFramework(framework.lower())
    except ValueError:
        typer.echo(f"Invalid agent framework: {framework}")
        raise typer.Exit(code=2)

    default_provider = "aws"
    if framework.lower() == "microsoft":
        default_provider = "azure"
    if not provider:
        provider = typer.prompt("Cloud provider (aws, azure, gcp)", default=default_provider)
    try:
        CloudProvider(provider.lower())
    except ValueError:
        typer.echo(f"Invalid cloud provider: {provider}")
        raise typer.Exit(code=2)

    version = template_version or typer.prompt("Template version", default="1.0.0")

    if framework.lower() == "pydantic":
        template_id = f"pydantic-cross-v{version}"
    else:
        template_id = f"{framework.lower()}-{provider.lower()}-v{version}"

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
        raise typer.Exit(code=1)


# Removed redundant subcommand; `ak init` handles both interactive and direct args