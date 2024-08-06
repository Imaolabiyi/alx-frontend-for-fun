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
    in_paragraph = False
    paragraph_lines = []

    for line in markdown_content:
        line = line.rstrip()  # strip trailing spaces but keep leading spaces for indentation
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
            if in_paragraph:
                html_content.append('<br/>'.join(paragraph_lines))
                html_content.append('</p>')
                in_paragraph = False
                paragraph_lines = []
            level = len(header_match.group(1))
            html_content.append('<h{level}>{text}</h{level}>'.format(level=level, text=header_match.group(2)))
        elif unordered_list_match:
            if in_ordered_list:
                html_content.append('</ol>')
                in_ordered_list = False
            if in_paragraph:
                html_content.append('<br/>'.join(paragraph_lines))
                html_content.append('</p>')
                in_paragraph = False
                paragraph_lines = []
            if not in_unordered_list:
                html_content.append('<ul>')
                in_unordered_list = True
            html_content.append('<li>{}</li>'.format(unordered_list_match.group(1)))
        elif ordered_list_match:
            if in_unordered_list:
                html_content.append('</ul>')
                in_unordered_list = False
            if in_paragraph:
                html_content.append('<br/>'.join(paragraph_lines))
                html_content.append('</p>')
                in_paragraph = False
                paragraph_lines = []
            if not in_ordered_list:
                html_content.append('<ol>')
                in_ordered_list = True
            html_content.append('<li>{}</li>'.format(ordered_list_match.group(1)))
        elif line:
            if in_unordered_list:
                html_content.append('</ul>')
                in_unordered_list = False
            if in_ordered_list:
                html_content.append('</ol>')
                in_ordered_list = False
            if not in_paragraph:
                html_content.append('<p>')
                in_paragraph = True
            paragraph_lines.append(line)
        else:
            if in_paragraph:
                html_content.append('<br/>'.join(paragraph_lines))
                html_content.append('</p>')
                in_paragraph = False
                paragraph_lines = []

    if in_unordered_list:
        html_content.append('</ul>')
    if in_ordered_list:
        html_content.append('</ol>')
    if in_paragraph:
        html_content.append('<br/>'.join(paragraph_lines))
        html_content.append('</p>')

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

