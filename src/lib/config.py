import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from .utils import set_file_permissions, ensure_directory_exists


class ConfigManager:
    """
    Configuration management system for handling cloud credentials 
    with appropriate file permissions (0600)
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".genai-agent"
        ensure_directory_exists(self.config_dir)
        
    def save_credentials(self, provider: str, credentials: Dict[str, Any]) -> Path:
        """Save cloud provider credentials with secure file permissions"""
        # Create provider-specific config file
        config_path = self.config_dir / f"{provider}_credentials.json"
        
        # Write credentials to file
        with open(config_path, 'w') as f:
            json.dump(credentials, f, indent=2)
        
        # Set secure file permissions (owner read/write only)
        set_file_permissions(config_path, 0o600)
        
        return config_path
    
    def load_credentials(self, provider: str) -> Optional[Dict[str, Any]]:
        """Load cloud provider credentials"""
        config_path = self.config_dir / f"{provider}_credentials.json"
        
        if not config_path.exists():
            return None
            
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def save_config(self, config_name: str, config_data: Dict[str, Any]) -> Path:
        """Save general configuration with standard permissions"""
        config_path = self.config_dir / f"{config_name}.json"
        
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        return config_path
    
    def load_config(self, config_name: str) -> Optional[Dict[str, Any]]:
        """Load general configuration"""
        config_path = self.config_dir / f"{config_name}.json"
        
        if not config_path.exists():
            return None
            
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def get_config_path(self) -> Path:
        """Get the configuration directory path"""
        return self.config_dir