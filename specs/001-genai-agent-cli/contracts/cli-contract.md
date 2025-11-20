# CLI Command Interface Contract

## Overview
This document defines the contract for the GenAI Agent CLI tool commands and their expected behaviors.

## Command: init
Initialize a new GenAI agent project from a template.

### Request
```bash
genai-agent init [OPTIONS] [NAME]
```

### Options
- `--provider TEXT`: Cloud provider (aws, azure, gcp). Defaults to interactive selection.
- `--framework TEXT`: Agent framework (microsoft, amazon, google, pydantic). Defaults to interactive selection.
- `--name TEXT`: Name for the new agent project.
- `--template-version TEXT`: Version of the template to use. Defaults to latest.

### Response
- Success: Creates a new directory with the agent template populated
- Error: Returns exit code 1 with error message

## Command: deploy
Deploy the GenAI agent to the configured cloud provider.

### Request
```bash
genai-agent deploy [OPTIONS]
```

### Options
- `--profile TEXT`: Configuration profile to use (dev, staging, prod). Defaults to 'default'.
- `--param TEXT`: Additional parameters in key=value format. Can be used multiple times.
- `--dry-run`: Show what would be deployed without actually deploying.

### Response
- Success: Returns exit code 0 with deployment summary
- Error: Returns exit code 1 with error message

## Command: status
Check the deployment status of the GenAI agent.

### Request
```bash
genai-agent status
```

### Response
- Success: Returns exit code 0 with status information
- Error: Returns exit code 1 with error message

## Command: metrics
Retrieve performance metrics for the deployed agent.

### Request
```bash
genai-agent metrics [OPTIONS]
```

### Options
- `--time-range TEXT`: Time range for metrics (1h, 24h, 7d). Defaults to 1h.
- `--output FORMAT`: Output format (table, json, csv). Defaults to table.

### Response
- Success: Returns exit code 0 with metrics data
- Error: Returns exit code 1 with error message

## Command: logs
View logs from the deployed agent.

### Request
```bash
genai-agent logs [OPTIONS]
```

### Options
- `--follow BOOLEAN`: Follow logs in real-time. Defaults to false.
- `--lines INTEGER`: Number of recent lines to show. Defaults to 50.
- `--level TEXT`: Log level filter (debug, info, warn, error). Defaults to all.

### Response
- Success: Returns exit code 0 with log data
- Error: Returns exit code 1 with error message

## Command: evaluate
Run evaluation tests on the deployed agent.

### Request
```bash
genai-agent evaluate [OPTIONS]
```

### Options
- `--tests TEXT`: Specific tests to run (all, performance, accuracy, custom). Defaults to 'all'.
- `--baseline TEXT`: Baseline to compare against for regression tests.

### Response
- Success: Returns exit code 0 with evaluation results
- Error: Returns exit code 1 with error message

## Command: diagnose
Diagnose common issues with the agent deployment.

### Request
```bash
genai-agent diagnose
```

### Response
- Success: Returns exit code 0 with diagnosis report
- Error: Returns exit code 1 with error message

## Command: list-templates
List available agent templates.

### Request
```bash
genai-agent list-templates [OPTIONS]
```

### Options
- `--framework TEXT`: Filter by agent framework.
- `--provider TEXT`: Filter by cloud provider.
- `--search TEXT`: Search term for template names/descriptions.

### Response
- Success: Returns exit code 0 with list of available templates
- Error: Returns exit code 1 with error message

## Command: update-templates
Update local template cache with latest versions.

### Request
```bash
genai-agent update-templates
```

### Response
- Success: Returns exit code 0 with update summary
- Error: Returns exit code 1 with error message

## Standard Exit Codes
- 0: Success
- 1: General error
- 2: Usage error (invalid arguments)
- 10: Configuration error
- 20: Deployment error
- 30: Authentication/authorization error