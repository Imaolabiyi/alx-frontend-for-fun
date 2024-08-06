#!/usr/bin/python3
"""
Module to convert Markdown to HTML
"""

import sys
import os
import re

def markdown_to_html(markdown_content):
    html_content = []
    in_unordered_list = False
    in_ordered_list = False

    for line in markdown_content:
        line = line.strip()
        header_match = re.match(r'^(#{1,6})\s+(.*)', line)
        unordered_list_match = re.match(r'^-\s+(.*)', line)
        ordered_list_match = re.match(r'^\*\s+(.*)', line)
        
        if header_match:
            if in_unordered_list:
                html_content.append('</ul>')
                in_unordered_list = False
            if in_ordered_list:
                html_content.append('</ol>')
                in_ordered_list = False
            level = len(header_match.group(1))
            html_content.append('<h{level}>{text}</h{level}>'.format(level=level, text=header_match.group(2)))
        elif unordered_list_match:
            if in_ordered_list:
                html_content.append('</ol>')
                in_ordered_list = False
            if not in_unordered_list:
                html_content.append('<ul>')
                in_unordered_list = True
            html_content.append('<li>{}</li>'.format(unordered_list_match.group(1)))
        elif ordered_list_match:
            if in_unordered_list:
                html_content.append('</ul>')
                in_unordered_list = False
            if not in_ordered_list:
                html_content.append('<ol>')
                in_ordered_list = True
            html_content.append('<li>{}</li>'.format(ordered_list_match.group(1)))
        else:
            if in_unordered_list:
                html_content.append('</ul>')
                in_unordered_list = False
            if in_ordered_list:
                html_content.append('</ol>')
                in_ordered_list = False
            if line:  # To avoid adding empty lines
                html_content.append(line)

    if in_unordered_list:
        html_content.append('</ul>')
    if in_ordered_list:
        html_content.append('</ol>')

    return '\n'.join(html_content)

def main():
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html")
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.isfile(markdown_file):
        print("Missing {}".format(markdown_file))
        sys.exit(1)

    with open(markdown_file, 'r') as f:
        markdown_content = f.readlines()

    html_content = markdown_to_html(markdown_content)

    with open(html_file, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    main()

