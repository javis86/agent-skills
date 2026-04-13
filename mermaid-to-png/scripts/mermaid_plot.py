import base64
import urllib.request
import sys
import os

def main():
    """
    Easiest example to plot a Mermaid diagram and export to PNG using Python.
    Uses the mermaid.ink API to render the diagram.
    """
    if len(sys.argv) < 3:
        print("Usage: python mermaid_plot.py '<diagram_code>' <output_file>")
        sys.exit(1)

    diagram_code = sys.argv[1]
    output_path = sys.argv[2]

    # Step 1: Encode the diagram code to base64
    # The mermaid.ink API expects a base64 encoded diagram string in the URL
    try:
        diagram_bytes = diagram_code.encode('utf-8')
        base64_bytes = base64.b64encode(diagram_bytes)
        base64_string = base64_bytes.decode('utf-8')

        # Step 2: Build the API URL
        url = f"https://mermaid.ink/img/{base64_string}"

        # Step 3: Fetch and save the image
        print(f"Fetching diagram from: {url}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())

        print(f"✅ Successfully exported diagram to: {os.path.abspath(output_path)}")
    except Exception as e:
        print(f"❌ Error rendering diagram: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
