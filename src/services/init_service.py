from pathlib import Path
from typing import Dict, Any, List
from models.template import GenAiAgentTemplate
from .template_service import TemplateService


class TemplateInitializationService:
    """
    Service for initializing new agent projects from templates
    """
    
    def __init__(self):
        self.template_service = TemplateService()
        
    def initialize_project(self, 
                          project_name: str, 
                          template_id: str, 
                          target_directory: Path,
                          parameters: Dict[str, Any] = None) -> bool:
        """
        Initialize a new project from a template
        """
        # Get the template
        template = self.template_service.get_template(template_id)
        if not template:
            print(f"Template {template_id} not found")
            return False
            
        # Create the project directory
        project_dir = target_directory / project_name
        if project_dir.exists():
            print(f"Project directory {project_dir} already exists")
            return False
            
        # Fetch and extract the template to the project directory
        result = self.template_service.fetch_and_extract_template(template_id, project_dir)
        
        if result is None:
            print(f"Failed to fetch template {template_id}")
            return False
            
        # Update the project configuration with user parameters if provided
        if parameters:
            self._update_project_config(project_dir, parameters)
            
        print(f"Successfully initialized project '{project_name}' from template '{template_id}'")
        return True
    
    def _update_project_config(self, project_dir: Path, parameters: Dict[str, Any]):
        """
        Update project configuration with user parameters
        """
        # This would update configuration files with provided parameters
        # For now, we'll just create a simple config file
        config_content = f"""
# Project Configuration for {project_dir.name}
# Generated from template initialization

[parameters]
"""
        for key, value in parameters.items():
            config_content += f"{key} = {value}\n"
            
        config_path = project_dir / "config.ini"
        config_path.write_text(config_content)
    
    def list_available_templates(self) -> List[GenAiAgentTemplate]:
        """
        List all available templates
        """
        return self.template_service.list_templates()