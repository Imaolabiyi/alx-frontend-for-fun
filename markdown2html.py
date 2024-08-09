#!/usr/bin/python3
"""
A script that converts markdown to HTML.
"""
import sys
import os
import re
import hashlib

if __name__ == '__main__':
    # Check if the number of arguments passed is 2
    if len(sys.argv[1:]) != 2:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        sys.exit(1)

    # Store the arguments into variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the markdown file exists and is a file
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    with open(input_file, encoding='utf-8') as file_1:
        html_content = []
        md_content = [line.rstrip() for line in file_1.readlines()]

        in_list = False
        in_ordered_list = False
        paragraph_open = False

        for line in md_content:
            # Handle headings
            heading = re.match(r'^(#{1,6})\s+(.*)', line)
            if heading:
                if paragraph_open:
                    html_content.append('</p>\n')
                    paragraph_open = False
                h_level = len(heading.group(1))
                html_content.append(f'<h{h_level}>{heading.group(2)}</h{h_level}>\n')

            # Handle unordered lists
            elif line.startswith('- '):
                if paragraph_open:
                    html_content.append('</p>\n')
                    paragraph_open = False
                if not in_list:
                    html_content.append('<ul>\n')
                    in_list = True
                html_content.append(f'  <li>{line[2:]}</li>\n')
            elif in_list and not line.startswith('- '):
                html_content.append('</ul>\n')
                in_list = False

            # Handle ordered lists
            elif re.match(r'^\d+\.\s+', line):
                if paragraph_open:
                    html_content.append('</p>\n')
                    paragraph_open = False
                if not in_ordered_list:
                    html_content.append('<ol>\n')
                    in_ordered_list = True
                html_content.append(f'  <li>{line[line.find(" ") + 1:]}</li>\n')
            elif in_ordered_list and not re.match(r'^\d+\.\s+', line):
                html_content.append('</ol>\n')
                in_ordered_list = False

            # Handle paragraphs and line breaks
            elif line:
                if not paragraph_open:
                    html_content.append('<p>\n')
                    paragraph_open = True
                # Replace **text** with <b>text</b> and __text__ with <em>text</em>
                line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
                line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)
                # Replace [[text]] with MD5 hash of text
                line = re.sub(r'\[\[(.+?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), line)
                # Replace ((text)) by removing 'c' or 'C' from the text
                line = re.sub(r'\(\((.+?)\)\)', lambda match: match.group(1).replace('c', '').replace('C', ''), line)
                html_content.append(line + '<br/>\n')

            # Close paragraph on empty line
            if not line and paragraph_open:
                html_content[-1] = html_content[-1].replace('<br/>', '')
                html_content.append('</p>\n')
                paragraph_open = False

        # Ensure any open lists or paragraphs are closed
        if in_list:
            html_content.append('</ul>\n')
        if in_ordered_list:
            html_content.append('</ol>\n')
        if paragraph_open:
            html_content.append('</p>\n')

    with open(output_file, 'w', encoding='utf-8') as file_2:
        file_2.writelines(html_content)
