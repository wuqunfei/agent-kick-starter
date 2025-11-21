from enum import IntEnum
import sys
import typer


class ExitCode(IntEnum):
    """Standard exit codes for the CLI tool"""
    SUCCESS = 0
    GENERAL_ERROR = 1
    USAGE_ERROR = 2  # invalid arguments
    CONFIGURATION_ERROR = 10
    DEPLOYMENT_ERROR = 20
    AUTH_ERROR = 30  # authentication/authorization error


def handle_error(error_msg: str, exit_code: ExitCode = ExitCode.GENERAL_ERROR):
    """Handle an error by printing the message and exiting with the appropriate code"""
    typer.echo(f"Error: {error_msg}", err=True)
    sys.exit(exit_code)


def handle_configuration_error(error_msg: str):
    """Handle a configuration error"""
    handle_error(error_msg, ExitCode.CONFIGURATION_ERROR)


def handle_deployment_error(error_msg: str):
    """Handle a deployment error"""
    handle_error(error_msg, ExitCode.DEPLOYMENT_ERROR)


def handle_auth_error(error_msg: str):
    """Handle an authentication/authorization error"""
    handle_error(error_msg, ExitCode.AUTH_ERROR)


def success_exit(message: str = ""):
    """Exit successfully with an optional message"""
    if message:
        typer.echo(message)
    sys.exit(ExitCode.SUCCESS)