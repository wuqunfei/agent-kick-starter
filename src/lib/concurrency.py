import os
import time
from pathlib import Path
from typing import Optional
import fcntl
import errno


class ConcurrencyManager:
    """
    Single-user, single-task execution constraint system
    Uses file locking to ensure only one instance of the CLI runs at a time
    """
    
    def __init__(self, lock_dir: Optional[Path] = None):
        self.lock_dir = lock_dir or Path.home() / ".genai-agent" / "locks"
        self.lock_dir.mkdir(parents=True, exist_ok=True)
        self.lock_file: Optional[Path] = None
        self.lock_fd: Optional[int] = None
        
    def acquire_lock(self, operation_name: str = "default") -> bool:
        """Acquire a lock for the operation, return True if successful"""
        lock_filename = f"genai-agent-{operation_name}.lock"
        self.lock_file = self.lock_dir / lock_filename
        
        try:
            # Open the lock file
            self.lock_fd = os.open(str(self.lock_file), os.O_CREAT | os.O_RDWR)
            
            # Try to acquire an exclusive lock (non-blocking)
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            
            # Write the PID to the lock file
            os.write(self.lock_fd, str(os.getpid()).encode())
            
            return True
            
        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                # Another process holds the lock
                print(f"Another instance is already running. Operation {operation_name} cannot proceed.")
                if self.lock_fd is not None:
                    os.close(self.lock_fd)
                return False
            else:
                raise e
    
    def release_lock(self) -> None:
        """Release the lock"""
        if self.lock_fd is not None:
            fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
            os.close(self.lock_fd)
            self.lock_fd = None
            
        if self.lock_file is not None and self.lock_file.exists():
            self.lock_file.unlink()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.release_lock()