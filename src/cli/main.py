import typer
from typing import Optional

# Initialize the main Typer application
app = typer.Typer(
    name="genai-agent",
    help="A CLI tool for production-ready Generative AI Agent templates",
    no_args_is_help=True
)

# Import and register subcommands
from .init import init_app
from .deploy import deploy_app
from .monitor import monitor_app

# Import services for top-level commands
from services.template_service import TemplateService

# Register subcommands
app.add_typer(init_app, name="init", help="Initialize a new GenAI agent project")
app.add_typer(deploy_app, name="deploy", help="Deploy a GenAI agent to cloud platform")
app.add_typer(monitor_app, name="metrics", help="Retrieve performance metrics for deployed agents")

# Additional commands that will be implemented later
@app.command()
def status():
    """Check the deployment status of the GenAI agent"""
    typer.echo("Status command - implementation pending")

@app.command()
def logs():
    """View logs from the deployed agent"""
    typer.echo("Logs command - implementation pending")

@app.command()
def list_templates():
    """List available agent templates"""
    template_service = TemplateService()
    templates = template_service.list_templates()

    typer.echo(f"Available templates: {len(templates)}")
    for template in templates:
        typer.echo(f"  - {template.id}: {template.name} ({template.framework} on {template.cloud_provider})")

@app.command()
def update_templates():
    """Update local template cache with latest versions"""
    template_service = TemplateService()
    templates = template_service.fetch_templates()

    typer.echo(f"Updated template cache with {len(templates)} templates")


def main():
    """Main entry point for the CLI application"""
    app()


if __name__ == "__main__":
    main()