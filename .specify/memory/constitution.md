<!--
SYNC IMPACT REPORT:
Version change: 1.1.0 → 1.2.0
Modified principles: Updated principles to include Pydantic AI alongside existing frameworks
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending
- .specify/templates/spec-template.md ⚠ pending
- .specify/templates/tasks-template.md ⚠ pending
- .qwen/commands/*.toml ⚠ pending
Follow-up TODOs: Update dependent templates to align with inclusion of Pydantic AI framework
-->
# GenAI Agent Framework Constitution

## Core Principles

### Multi-Platform Agent Development
All GenAI agents must be developed to support Microsoft Agent Framework, Amazon Bedrock AgentCore, Google ADK, and Pydantic AI, enabling deployment across major cloud platforms and local development environments. Code must be architected to maintain compatibility across these platforms while leveraging platform-specific capabilities.

### Agent Framework Standards
All implementations must follow standards and best practices from the four specified agent frameworks (Microsoft Agent Framework, Amazon Bedrock AgentCore, Google ADK, and Pydantic AI). Agents must adhere to framework-specific patterns for conversation management, tool integration, and external API interactions.

### AI-Agent First Architecture
All services and components must be designed to work seamlessly with GenAI agent patterns and capabilities. Architecture decisions must prioritize agent integration, state management, and interaction flow over traditional application patterns.

### Cloud-Native Agent Deployment
All agents must support deployment to AWS, Azure, and Google Cloud with appropriate observability, scaling, and security configurations. Deployment processes must handle infrastructure provisioning, service configuration, and monitoring setup automatically.

### Agent Lifecycle Management
All agents must include capabilities for deployment, monitoring, evaluation, and updates. This includes health checks, performance metrics collection, evaluation frameworks, and zero-downtime update mechanisms.

## Technology Stack

All GenAI agent projects must use:
- Python as the primary language for agent logic and orchestration
- Microsoft Agent Framework, Amazon Bedrock AgentCore, Google ADK, and Pydantic AI for platform-specific agent implementations
- uv for dependency management
- unittest for unit testing and testcontainers for integration testing
- GitHub for CI/CD pipeline
- Cloud-native observability tools for monitoring and evaluation

## Development Workflow

- All code changes go through pull requests with agent-specific validation
- Code reviews must verify compliance with all four agent framework requirements (Microsoft, Amazon, Google, and Pydantic AI)
- All tests must pass in CI before merging, including multi-platform compatibility checks across all supported frameworks
- Agent templates must include comprehensive monitoring, evaluation, and observability practices
- Multi-cloud deployment workflows must be documented and tested

## Governance

This constitution supersedes all other practices. Amendments must be documented, approved by maintainers, and include migration plans where applicable. All PRs and reviews must verify compliance with agent framework standards.

**Version**: 1.2.0 | **Ratified**: 2025-11-20 | **Last Amended**: 2025-11-20
