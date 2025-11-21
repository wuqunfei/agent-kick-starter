from typing import Dict, List, Optional
from pathlib import Path
from models.template import GenAiAgentTemplate, AgentFramework, CloudProvider
import requests
import tempfile
import zipfile
import os


class TemplateService:
    """
    Service for managing remote templates according to FR-015
    Templates are fetched remotely on each use rather than stored locally
    """

    def __init__(self, base_url: str = "https://example.com/genai-templates"):
        self.base_url = base_url
        self.templates: Dict[str, GenAiAgentTemplate] = {}
        self.temp_dir = Path(tempfile.gettempdir()) / "genai-agent-templates"
        self.temp_dir.mkdir(exist_ok=True)

    def fetch_templates(self) -> List[GenAiAgentTemplate]:
        """
        Fetch the list of available templates from the remote repository
        """
        # In a real implementation, this would fetch from a remote source
        # For now, we'll return some example templates
        example_templates = [
            GenAiAgentTemplate(
                id="microsoft-aws-v1.0.0",
                name="Microsoft Agent on AWS",
                description="Template for Microsoft Agent Framework on AWS",
                framework=AgentFramework.MICROSOFT,
                cloud_provider=CloudProvider.AWS,
                version="1.0.0",
                path="",
                parameters=[{"region": "us-east-1"}],
                dependencies=["microsoft-agent-framework>=1.0.0", "boto3>=1.28.0"]
            ),
            GenAiAgentTemplate(
                id="microsoft-azure-v1.0.0",
                name="Microsoft Agent on Azure",
                description="Template for Microsoft Agent Framework on Azure",
                framework=AgentFramework.MICROSOFT,
                cloud_provider=CloudProvider.AZURE,
                version="1.0.0",
                path="",
                parameters=[{"region": "eastus"}],
                dependencies=["microsoft-agent-framework>=1.0.0", "azure-core>=1.29.0"]
            ),
            GenAiAgentTemplate(
                id="microsoft-gcp-v1.0.0",
                name="Microsoft Agent on GCP",
                description="Template for Microsoft Agent Framework on Google Cloud Platform",
                framework=AgentFramework.MICROSOFT,
                cloud_provider=CloudProvider.GCP,
                version="1.0.0",
                path="",
                parameters=[{"region": "us-central1"}],
                dependencies=["microsoft-agent-framework>=1.0.0", "google-cloud-core>=2.3.0"]
            ),
            GenAiAgentTemplate(
                id="amazon-aws-v1.0.0",
                name="Amazon Bedrock Agent on AWS",
                description="Template for Amazon Bedrock AgentCore on AWS",
                framework=AgentFramework.AMAZON,
                cloud_provider=CloudProvider.AWS,
                version="1.0.0",
                path="",
                parameters=[{"region": "us-east-1"}],
                dependencies=["amazon-bedrock-agentcore>=1.0.0"]
            ),
            GenAiAgentTemplate(
                id="google-gcp-v1.0.0",
                name="Google ADK on GCP",
                description="Template for Google ADK on Google Cloud Platform",
                framework=AgentFramework.GOOGLE,
                cloud_provider=CloudProvider.GCP,
                version="1.0.0",
                path="",
                parameters=[{"region": "us-central1"}],
                dependencies=["google-adk>=1.0.0"]
            ),
            GenAiAgentTemplate(
                id="pydantic-cross-v1.0.0",
                name="Pydantic AI Cross-Platform",
                description="Template for Pydantic AI framework that works across platforms",
                framework=AgentFramework.PYDANTIC,
                cloud_provider=CloudProvider.AWS,  # Just a default
                version="1.0.0",
                path="",
                parameters=[{"model": "gpt-4"}],
                dependencies=["pydantic-ai>=0.0.1"]
            )
        ]

        # Store templates in the registry
        for template in example_templates:
            self.templates[template.id] = template

        return example_templates

    def get_template(self, template_id: str) -> Optional[GenAiAgentTemplate]:
        """Get a specific template by ID"""
        # In real implementation, fetch fresh from remote each time per FR-015
        if template_id not in self.templates:
            # Attempt to fetch from remote
            all_templates = self.fetch_templates()
            for template in all_templates:
                if template.id == template_id:
                    self.templates[template_id] = template
                    break

        return self.templates.get(template_id)

    def get_templates_by_framework(self, framework: AgentFramework) -> List[GenAiAgentTemplate]:
        """Get templates filtered by agent framework"""
        # Always fetch latest templates to ensure up-to-date list
        self.fetch_templates()
        return [t for t in self.templates.values() if t.framework == framework]

    def get_templates_by_provider(self, provider: CloudProvider) -> List[GenAiAgentTemplate]:
        """Get templates filtered by cloud provider"""
        # Always fetch latest templates to ensure up-to-date list
        self.fetch_templates()
        return [t for t in self.templates.values() if t.cloud_provider == provider]

    def fetch_and_extract_template(self, template_id: str, target_dir: Path) -> Optional[Path]:
        """
        Fetch and extract a template from the remote repository to target directory
        This implements FR-015: Templates stored only remotely and fetched on each use
        """
        template = self.get_template(template_id)
        if not template:
            return None

        # In a real implementation, we'd download the actual template from remote
        # For now, we'll create a basic template structure in the target directory
        target_dir.mkdir(parents=True, exist_ok=True)

        # Create a basic template structure
        (target_dir / "README.md").write_text(f"# {template.name}\n\n{template.description}\n")
        (target_dir / "pyproject.toml").write_text(f"""[project]
name = "{template.name.lower().replace(' ', '-')}"
version = "{template.version}"
description = "{template.description}"
dependencies = [
    {", ".join([f'"{dep}"' for dep in template.dependencies])}
]
""")
        (target_dir / "src").mkdir(exist_ok=True)
        (target_dir / "tests").mkdir(exist_ok=True)
        (target_dir / ".gitignore").write_text("""__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
""")

        (target_dir / ".env.example").write_text(
            f"AGENT_NAME=hello-agent\nMODEL_NAME=gpt-4\nMODEL_PROVIDER={template.cloud_provider}\n"
        )
        (target_dir / "src" / "config.py").write_text(
            "from pydantic_settings import BaseSettings, SettingsConfigDict\n\n"
            "class Settings(BaseSettings):\n"
            "    agent_name: str = \"hello-agent\"\n"
            "    model_name: str = \"gpt-4\"\n"
            "    model_provider: str | None = None\n\n"
            "    model_config = SettingsConfigDict(env_file=\".env\", env_file_encoding=\"utf-8\")\n"
        )
        (target_dir / "src" / "app.py").write_text(
            "from config import Settings\n\n"
            "def run():\n"
            f"    s = Settings()\n    print(f\"{{s.agent_name}}: Hello from {template.framework} on {{s.model_provider or 'unknown'}} using {{s.model_name}}\")\n\n"
            "if __name__ == \"__main__\":\n"
            "    run()\n"
        )

        # Create framework-specific files
        if template.framework == AgentFramework.MICROSOFT:
            (target_dir / "src" / "microsoft_agent.py").write_text("# Microsoft Agent implementation\n")
        elif template.framework == AgentFramework.AMAZON:
            (target_dir / "src" / "bedrock_agent.py").write_text("# Amazon Bedrock Agent implementation\n")
        elif template.framework == AgentFramework.GOOGLE:
            (target_dir / "src" / "google_agent.py").write_text("# Google ADK Agent implementation\n")
        elif template.framework == AgentFramework.PYDANTIC:
            (target_dir / "src" / "pydantic_agent.py").write_text("# Pydantic AI Agent implementation\n")

        # Create cloud provider-specific files
        if template.cloud_provider == CloudProvider.AWS:
            (target_dir / "infrastructure").mkdir(exist_ok=True)
            pulumi_dir = target_dir / "infrastructure" / "pulumi" / "aws"
            pulumi_dir.mkdir(parents=True, exist_ok=True)
            (pulumi_dir / "Pulumi.yaml").write_text("name: agent-aws-infra\nruntime: python\n")
            (pulumi_dir / "__main__.py").write_text(
                "import pulumi\nfrom pulumi_aws import s3\n"
                "bucket = s3.Bucket('agent-bucket')\n"
                "pulumi.export('bucket_name', bucket.id)\n"
            )
            (pulumi_dir / "requirements.txt").write_text("pulumi>=3.0.0\npulumi-aws>=6.0.0\n")
        elif template.cloud_provider == CloudProvider.AZURE:
            (target_dir / "infrastructure").mkdir(exist_ok=True)
            pulumi_dir = target_dir / "infrastructure" / "pulumi" / "azure"
            pulumi_dir.mkdir(parents=True, exist_ok=True)
            (pulumi_dir / "Pulumi.yaml").write_text("name: agent-azure-infra\nruntime: python\n")
            (pulumi_dir / "__main__.py").write_text(
                "import pulumi\nfrom pulumi_azure_native import resources\n"
                "rg = resources.ResourceGroup('agent-rg')\n"
                "pulumi.export('resource_group', rg.name)\n"
            )
            (pulumi_dir / "requirements.txt").write_text("pulumi>=3.0.0\npulumi-azure-native>=2.0.0\n")
        elif template.cloud_provider == CloudProvider.GCP:
            (target_dir / "infrastructure").mkdir(exist_ok=True)
            pulumi_dir = target_dir / "infrastructure" / "pulumi" / "gcp"
            pulumi_dir.mkdir(parents=True, exist_ok=True)
            (pulumi_dir / "Pulumi.yaml").write_text("name: agent-gcp-infra\nruntime: python\n")
            (pulumi_dir / "__main__.py").write_text(
                "import pulumi\nfrom pulumi_gcp import storage\n"
                "bucket = storage.Bucket('agent-bucket')\n"
                "pulumi.export('bucket_name', bucket.name)\n"
            )
            (pulumi_dir / "requirements.txt").write_text("pulumi>=3.0.0\npulumi-gcp>=7.0.0\n")

        return target_dir

    def list_templates(self) -> List[GenAiAgentTemplate]:
        """List all available templates"""
        # Always fetch latest templates to ensure up-to-date list
        self.fetch_templates()
        return list(self.templates.values())