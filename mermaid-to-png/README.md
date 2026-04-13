# Mermaid to PNG Skill for Gemini CLI

A simple Gemini CLI skill that converts Mermaid diagrams into PNG images using a zero-dependency Python script and the `mermaid.ink` API.

## Features

- **Zero Dependencies**: Uses standard Python libraries (`base64`, `urllib`).
- **Easy Integration**: Designed to be triggered by Gemini CLI for visual documentation tasks.
- **Fast Rendering**: Leverages the `mermaid.ink` service for high-quality PNG output.

## Installation

1. Package the skill:
   ```bash
   gemini skills package .
   ```
2. Install the skill:
   ```bash
   gemini skills install mermaid-to-png.skill --scope user
   ```
3. Reload your skills:
   ```bash
   /skills reload
   ```

## Usage

Ask Gemini CLI to generate a diagram and save it as a PNG:

> "Create a flowchart for a CI/CD pipeline and save it as pipeline.png using the mermaid-to-png skill."

## Project Structure

- `SKILL.md`: Metadata and instructions for the Gemini CLI agent.
- `scripts/mermaid_plot.py`: The Python rendering script.
- `.gitignore`: Standard Python ignore rules.
