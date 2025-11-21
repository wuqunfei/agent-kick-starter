import os
import platform
import subprocess
from pathlib import Path
from typing import Union
import tempfile


def get_platform() -> str:
    """Get the current platform"""
    return platform.system().lower()


def is_windows() -> bool:
    """Check if running on Windows"""
    return get_platform() == "windows"


def is_macos() -> bool:
    """Check if running on macOS"""
    return get_platform() == "darwin"


def is_linux() -> bool:
    """Check if running on Linux"""
    return get_platform() == "linux"


def normalize_path(path: Union[str, Path]) -> Path:
    """Normalize path for the current platform"""
    path_obj = Path(path).resolve()
    if is_windows():
        # On Windows, we might want to handle paths differently
        return Path(str(path_obj).replace("/", "\\"))
    else:
        # On Unix-like systems, normalize to forward slashes
        return Path(str(path_obj).replace("\\", "/"))


def ensure_directory_exists(path: Union[str, Path]) -> None:
    """Ensure that a directory exists, creating it if necessary"""
    Path(path).mkdir(parents=True, exist_ok=True)


def file_exists(path: Union[str, Path]) -> bool:
    """Check if a file exists"""
    return Path(path).is_file()


def directory_exists(path: Union[str, Path]) -> bool:
    """Check if a directory exists"""
    return Path(path).is_dir()


def run_command(cmd: str, cwd: Union[str, Path, None] = None) -> subprocess.CompletedProcess:
    """Run a shell command and return the result"""
    if isinstance(cmd, str):
        cmd = cmd.split()
    
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False
    )


def get_temp_dir() -> Path:
    """Get a temporary directory path"""
    return Path(tempfile.gettempdir())


def set_file_permissions(path: Union[str, Path], mode: int) -> None:
    """Set file permissions (useful for credential files)"""
    os.chmod(str(path), mode)


def secure_temp_file(suffix: str = "", prefix: str = "secure_") -> Path:
    """Create a secure temporary file"""
    return Path(tempfile.mktemp(suffix=suffix, prefix=prefix))