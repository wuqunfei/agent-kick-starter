import typer
from typing import Optional
import json
from pathlib import Path

from services.monitor_service import MonitoringService
from lib.config import ConfigManager
from lib.errors import ExitCode, handle_error


# Create a Typer instance for the monitor command group
monitor_app = typer.Typer(
    name="monitor",
    help="Monitor and evaluate deployed GenAI agent performance"
)


@monitor_app.callback()
def callback():
    """Monitor and evaluate deployed GenAI agent performance"""
    pass


@monitor_app.command("metrics")
def metrics_command(
    deployment_id: Optional[str] = typer.Argument(None, help="ID of the deployment to get metrics for"),
    time_range: str = typer.Option("1h", "--time-range", help="Time range for metrics (1h, 24h, 7d)"),
    output_format: str = typer.Option("table", "--output", help="Output format (table, json, csv)")
):
    """
    Retrieve performance metrics for the deployed agent.
    """
    if not deployment_id:
        # Default to using current directory name
        deployment_id = f"deploy_default_{Path.cwd().name}"

    typer.echo(f"Retrieving metrics for deployment: {deployment_id}, time range: {time_range}")
    typer.echo(f"Output format: {output_format}")

    # Load configuration to determine cloud provider
    config_manager = ConfigManager()
    # Try to get provider from config
    # For this example, we'll assume a default provider is configured for the current directory
    profile_name = "default"
    profile_data = config_manager.load_config(profile_name)

    if not profile_data:
        typer.echo("Configuration not found, using default provider (aws)")
        cloud_provider = "aws"
    else:
        cloud_provider = profile_data.get('cloud_provider', 'aws')

    # Initialize monitoring service
    monitoring_service = MonitoringService()

    # Get metrics
    metrics = monitoring_service.get_metrics(deployment_id, cloud_provider, time_range)

    if not metrics:
        handle_error(f"Could not retrieve metrics for deployment {deployment_id}", ExitCode.GENERAL_ERROR)

    # Output based on format
    if output_format == "json":
        typer.echo(json.dumps(metrics.dict(), indent=2, default=str))
    elif output_format == "csv":
        # Simple CSV output
        typer.echo("metric,value")
        if metrics.latency is not None:
            typer.echo(f"latency,{metrics.latency}")
        if metrics.throughput is not None:
            typer.echo(f"throughput,{metrics.throughput}")
        if metrics.accuracy is not None:
            typer.echo(f"accuracy,{metrics.accuracy}")
        if metrics.error_rate is not None:
            typer.echo(f"error_rate,{metrics.error_rate}")
        if metrics.user_satisfaction is not None:
            typer.echo(f"user_satisfaction,{metrics.user_satisfaction}")
    else:  # table format
        typer.echo(f"Metrics for deployment: {deployment_id}")
        typer.echo(f"  Latency: {metrics.latency}s" if metrics.latency is not None else "  Latency: N/A")
        typer.echo(f"  Throughput: {metrics.throughput} req/min" if metrics.throughput is not None else "  Throughput: N/A")
        typer.echo(f"  Accuracy: {metrics.accuracy * 100}%" if metrics.accuracy is not None else "  Accuracy: N/A")
        typer.echo(f"  Error Rate: {metrics.error_rate * 100}%" if metrics.error_rate is not None else "  Error Rate: N/A")
        typer.echo(f"  User Satisfaction: {metrics.user_satisfaction}/5.0" if metrics.user_satisfaction is not None else "  User Satisfaction: N/A")
        if metrics.resource_utilization:
            typer.echo(f"  Resource Utilization: {metrics.resource_utilization}")


@monitor_app.command("logs")
def logs_command(
    deployment_id: Optional[str] = typer.Argument(None, help="ID of the deployment to get logs for"),
    follow: bool = typer.Option(False, "--follow", help="Follow logs in real-time"),
    lines: int = typer.Option(50, "--lines", help="Number of recent lines to show"),
    level: str = typer.Option("all", "--level", help="Log level filter (debug, info, warn, error)")
):
    """
    View logs from the deployed agent.
    """
    if not deployment_id:
        # Default to using current directory name
        deployment_id = f"deploy_default_{Path.cwd().name}"

    typer.echo(f"Showing logs for deployment: {deployment_id} (last {lines} lines, level: {level})")
    if follow:
        typer.echo("Following logs in real-time")

    # Load configuration to determine cloud provider
    config_manager = ConfigManager()
    profile_name = "default"
    profile_data = config_manager.load_config(profile_name)

    if not profile_data:
        typer.echo("Configuration not found, using default provider (aws)")
        cloud_provider = "aws"
    else:
        cloud_provider = profile_data.get('cloud_provider', 'aws')

    # Initialize monitoring service
    monitoring_service = MonitoringService()

    # Get logs
    logs = monitoring_service.get_logs(deployment_id, cloud_provider, lines, level)

    for log_line in logs:
        typer.echo(log_line)


@monitor_app.command("evaluate")
def evaluate_command(
    deployment_id: Optional[str] = typer.Argument(None, help="ID of the deployment to evaluate"),
    tests: str = typer.Option("all", "--tests", help="Specific tests to run (all, performance, accuracy, custom)")
):
    """
    Run evaluation tests on the deployed agent.
    """
    if not deployment_id:
        # Default to using current directory name
        deployment_id = f"deploy_default_{Path.cwd().name}"

    typer.echo(f"Running evaluation tests: {tests} for deployment: {deployment_id}")

    # Initialize monitoring service
    monitoring_service = MonitoringService()

    # Run evaluation
    results = monitoring_service.run_evaluation(deployment_id, tests)

    typer.echo(f"Evaluation results for deployment: {deployment_id}")
    typer.echo(json.dumps(results, indent=2))


@monitor_app.command("diagnose")
def diagnose_command(
    deployment_id: Optional[str] = typer.Argument(None, help="ID of the deployment to diagnose")
):
    """
    Diagnose common issues with the agent deployment.
    """
    if not deployment_id:
        # Default to using current directory name
        deployment_id = f"deploy_default_{Path.cwd().name}"

    typer.echo(f"Running diagnosis for deployment: {deployment_id}")

    # Initialize monitoring service
    monitoring_service = MonitoringService()

    # Run diagnosis
    diagnosis = monitoring_service.run_diagnosis(deployment_id)

    typer.echo(f"Diagnosis results for deployment: {deployment_id}")
    typer.echo(json.dumps(diagnosis, indent=2))