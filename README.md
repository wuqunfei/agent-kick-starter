# GenAI Agent CLI Tool

A CLI tool for creating, deploying, and managing production-ready Generative AI agent templates across multiple platforms and frameworks.

## Features

- Generate GenAI agent projects from production-ready templates
- Support for multiple agent frameworks (Microsoft, Amazon, Google, Pydantic)
- Multi-cloud deployment (AWS, Azure, Google Cloud)
- Built-in evaluation and monitoring capabilities
- Configuration management for multiple environments

## Installation

```bash
# Using uv (recommended)
uv tool install genai-agent-cli

# Or install from source
git clone <repository-url>
cd agent-kick-starter
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

```bash
# Initialize a new agent project
genai-agent init --provider aws --framework amazon --name my-agent

# Deploy an agent
genai-agent deploy --profile development

# Monitor agent performance
genai-agent metrics --time-range 24h

# View logs
genai-agent logs --follow
```

## Development

1. Set up your development environment:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e '.[dev]'
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Run the CLI:
   ```bash
   python -m src.cli.main --help
   ```

## Contributing

See the [CONTRIBUTING.md](docs/contributing.md) file for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.