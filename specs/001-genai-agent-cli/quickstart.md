# Quickstart Guide: CLI Tool for Production-Ready Generative AI Agent Templates

## Overview
This guide will help you quickly get started with the CLI tool for creating, deploying, and managing GenAI agents across multiple frameworks and cloud platforms.

## Prerequisites
- Python 3.11 or higher
- `uv` package manager installed
- Cloud provider account credentials (AWS, Azure, or Google Cloud)
- Appropriate permissions to create resources in your cloud account

## Installation
```bash
# Install the CLI tool using uv
uv tool install genai-agent-cli

# Or install from source
git clone <repository-url>
cd agent-kick-starter
uv venv  # Create virtual environment
source .venv/bin/activate  # Activate virtual environment
uv pip install -e .
```

## Getting Started

### 1. Initialize a New GenAI Agent Project
```bash
# Initialize with a specific cloud provider
genai-agent init --provider aws --framework pydantic --name my-agent

# Initialize with interactive prompts for all options
genai-agent init

# Initialize for a specific framework
genai-agent init --framework amazon --name my-bedrock-agent
```

### 2. Configure Your Agent
After initialization, edit the configuration profile in the generated `config/` directory:

```bash
# Edit the default configuration
nano config/default.json
```

Configuration options include:
- Cloud credentials and region
- Model selection
- Security settings
- Environment variables
- Custom parameters for the specific framework

### 3. Deploy Your Agent
```bash
# Deploy to your configured cloud provider
genai-agent deploy --profile production

# Deploy with custom parameters
genai-agent deploy --param model=gpt-4 --param region=us-west-2

# Check deployment status
genai-agent status
```

### 4. Monitor and Evaluate
```bash
# View performance metrics
genai-agent metrics

# Run evaluation tests
genai-agent evaluate --tests all

# Monitor logs
genai-agent logs --follow

# Diagnose issues
genai-agent diagnose
```

## Common Workflows

### Creating an Agent for AWS Bedrock
```bash
genai-agent init --provider aws --framework amazon --name my-bedrock-agent
cd my-bedrock-agent
# Configure AWS credentials in config/aws.json
genai-agent deploy --profile aws
```

### Creating an Agent for Azure
```bash
genai-agent init --provider azure --framework microsoft --name my-azure-agent
cd my-azure-agent
# Configure Azure credentials in config/azure.json
genai-agent deploy --profile azure
```

### Creating an Agent for Google Cloud
```bash
genai-agent init --provider gcp --framework google --name my-gcp-agent
cd my-gcp-agent
# Configure GCP credentials in config/gcp.json
genai-agent deploy --profile gcp
```

### Creating an Agent with Pydantic AI
```bash
genai-agent init --provider aws --framework pydantic --name my-pydantic-agent
cd my-pydantic-agent
# This creates an agent that works across cloud providers
genai-agent deploy --profile default
```

## Useful Commands

### Help
```bash
genai-agent --help
genai-agent <command> --help
```

### List Available Templates
```bash
genai-agent list-templates
```

### Update Templates
```bash
genai-agent update-templates
```

### Version Information
```bash
genai-agent --version
```

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure your cloud credentials have necessary permissions to create resources.

2. **Template Not Found**: Run `genai-agent update-templates` to refresh available templates.

3. **Deployment Fails**: Check cloud provider quotas and ensure required services are enabled.

4. **Configuration Errors**: Validate your configuration files against the template schema.

### Getting Help
```bash
# Get detailed help
genai-agent help <command>

# View logs
genai-agent logs

# Diagnose common issues
genai-agent diagnose
```

## Next Steps
- Explore advanced configuration options
- Learn about custom templates
- Set up automated deployment pipelines
- Configure monitoring and alerts