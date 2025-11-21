import typer
from typing import List, Optional
from pathlib import Path
import sys

from services.deploy_service import DeploymentService
from models.deployment import DeploymentManifest, DeploymentStatus
from models.config_profile import ConfigurationProfile
from lib.config import ConfigManager
from lib.errors import ExitCode, handle_error


# Create a Typer instance for the deploy command group
deploy_app = typer.Typer(
    name="deploy",
    help="Deploy the GenAI agent to the configured cloud provider"
)


@deploy_app.callback()
def callback():
    """Deploy the GenAI agent to the configured cloud provider"""
    pass


@deploy_app.command("deploy")
def deploy_command(
    profile: str = typer.Option("default", "--profile", help="Configuration profile to use (dev, staging, prod)"),
    param: List[str] = typer.Option([], "--param", help="Additional parameters in key=value format"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be deployed without actually deploying")
):
    """
    Deploy the GenAI agent to the configured cloud provider.
    """
    typer.echo(f"Deploying GenAI agent with profile: {profile}")

    if dry_run:
        typer.echo("Dry run mode - no actual deployment will occur")

    for p in param:
        typer.echo(f"Using parameter: {p}")

    # Initialize services
    config_manager = ConfigManager()
    deploy_service = DeploymentService()

    # Load the configuration profile
    profile_data = config_manager.load_config(profile)
    if not profile_data:
        handle_error(f"Configuration profile '{profile}' not found", ExitCode.CONFIGURATION_ERROR)

    # Create ConfigurationProfile object from loaded data
    try:
        from pydantic import parse_obj_as
        config_profile = parse_obj_as(ConfigurationProfile, profile_data)
    except Exception:
        handle_error(f"Invalid configuration profile format for '{profile}'", ExitCode.CONFIGURATION_ERROR)

    # Create a deployment manifest (in a real implementation, this would be more complex)
    manifest = DeploymentManifest(
        id=f"deploy_{profile}_{Path.cwd().name}",
        template_id=config_profile.template_id,
        profile_id=config_profile.id,
        cloud_provider=profile_data.get('cloud_provider', 'unknown'),
        resources=[],
        deployment_path=str(Path.cwd()),
        status=DeploymentStatus.PENDING
    )

    # Perform the deployment
    success = deploy_service.deploy(manifest, config_profile, dry_run)

    if success:
        typer.echo("Deployment completed successfully!")
        if not dry_run:
            typer.echo(f"Deployment ID: {manifest.id}")
    else:
        handle_error("Deployment failed", ExitCode.DEPLOYMENT_ERROR)


@deploy_app.command("status")
def status_command(
    deployment_id: Optional[str] = typer.Argument(None, help="ID of the deployment to check status for")
):
    """
    Check the deployment status of the GenAI agent.
    """
    if not deployment_id:
        # Default to checking status for current directory
        deployment_id = f"deploy_default_{Path.cwd().name}"

    deploy_service = DeploymentService()
    status = deploy_service.get_deployment_status(deployment_id)

    if status:
        typer.echo(f"Deployment {deployment_id} status: {status.value}")
    else:
        typer.echo(f"Deployment {deployment_id} not found or status unknown")