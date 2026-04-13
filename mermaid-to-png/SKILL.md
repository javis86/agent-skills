---
name: mermaid-to-png
description: Converts Mermaid diagrams into PNG images using a Python script. Use this skill when you need to generate a visual representation (PNG) of a Mermaid diagram description (e.g. flowcharts, sequence diagrams).
---

# Mermaid to PNG

This skill provides a simple way to render Mermaid diagrams into PNG images using a Python script that leverages the `mermaid.ink` API.

## Workflow

1.  **Extract/Generate Mermaid Code**: Ensure you have the Mermaid diagram code (e.g., `graph TD; A-->B;`).
2.  **Run the Script**: Execute the bundled Python script to perform the conversion.
3.  **Check Output**: The script will save the rendered diagram as a PNG file at the specified path.

### Example Usage

```bash
python scripts/mermaid_plot.py "graph TD; A-->B; B-->C;" diagram.png
```

## Bundled Resources

### scripts/

- `mermaid_plot.py`: The core rendering script. It uses standard Python libraries (`base64`, `urllib`) to encode the diagram and fetch the rendered image from `mermaid.ink`. Requires an active internet connection.
