#!/usr/bin/python3
"""
A script that converts markdown to HTML
"""
import sys
import os
import re
import hashlib

if __name__ == '__main__':

    # Check if the number of arguments passed is 2
    if len(sys.argv[1:]) != 2:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
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
        md_content = [line.strip() for line in file_1.readlines()]

        in_list = False
        in_ordered_list = False

        for line in md_content:
            # Handle headings
            heading = re.split(r'#{1,6} ', line)
            if len(heading) > 1:
                h_level = len(line[:line.find(heading[1])-1])
                html_content.append(
                    f'<h{h_level}>{heading[1]}</h{h_level}>\n'
                )

            # Handle unordered lists
            elif line.startswith('- '):
                if not in_list:
                    html_content.append('<ul>\n')
                    in_list = True
                html_content.append(f'  <li>{line[2:]}</li>\n')
            elif in_list:
                html_content.append('</ul>\n')
                in_list = False

            # Handle ordered lists
            elif line.startswith('* '):
                if not in_ordered_list:
                    html_content.append('<ol>\n')
                    in_ordered_list = True
                html_content.append(f'  <li>{line[2:]}</li>\n')
            elif in_ordered_list:
                html_content.append('</ol>\n')
                in_ordered_list = False

            # Handle paragraphs and line breaks
            elif line:
                if line != "":
                    line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
                    line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)
                    line = re.sub(r'\[\[(.+?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), line)
                    line = re.sub(r'\(\((.+?)\)\)', lambda match: match.group(1).replace('c', '').replace('C', ''), line)
                    if html_content and html_content[-1].strip() and not html_content[-1].startswith('<p>'):
                        html_content.append('<p>\n')
                    html_content.append(line + '\n')
                if html_content and html_content[-1].strip() and not html_content[-1].startswith('<br/>'):
                    html_content.append('<br/>\n')

            # Add a closing </p> tag after the last paragraph
            if line == "" and html_content and html_content[-1].strip().startswith('<p>'):
                html_content.append('</p>\n')

        # Ensure any open lists are closed
        if in_list:
            html_content.append('</ul>\n')
        if in_ordered_list:
            html_content.append('</ol>\n')

    with open(output_file, 'w', encoding='utf-8') as file_2:
        file_2.writelines(html_content)

