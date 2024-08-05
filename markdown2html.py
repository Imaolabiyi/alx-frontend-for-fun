#!/usr/bin/python3
"""
Script to convert Markdown to HTML
"""

import sys
import os


def convert_markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to HTML and writes it to an output file.

    Args:
        input_file (str): Path to the input Markdown file.
        output_file (str): Path to the output HTML file.
    """
    try:
        with open(input_file, 'r') as md_file:
            md_lines = md_file.readlines()

        html_content = ""
        for line in md_lines:
            # Check for heading syntax
            if line.startswith('#'):
                heading_level = len(line.split(' ')[0])
                heading_text = line.strip('#').strip()
                html_content += (
                    f"<h{heading_level}>{heading_text}</h{heading_level}>\n"
                )
            else:
                html_content += line

        with open(output_file, 'w') as html_file:
            html_file.write(html_content)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)
