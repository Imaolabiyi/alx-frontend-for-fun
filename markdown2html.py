#!/usr/bin/python3
"""
Markdown to HTML script with additional parsing for custom bold syntax.
"""
import sys
import re
import hashlib

def md5_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def remove_c(content):
    return re.sub(r'c', '', content, flags=re.IGNORECASE)

def parse_markdown_to_html(markdown_text):
    html_lines = []
    in_list = False
    paragraphs = []
    
    for line in markdown_text.split('\n'):
        line = line.strip()
        
        if not line:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if paragraphs:
                html_lines.append('<p>' + '<br/>\n'.join(paragraphs) + '</p>')
                paragraphs = []
            continue
        
        # Heading
        if line.startswith('# '):
            if paragraphs:
                html_lines.append('<p>' + '<br/>\n'.join(paragraphs) + '</p>')
                paragraphs = []
            html_lines.append(f'<h1>{line[2:].strip()}</h1>')
        elif line.startswith('- '):
            if paragraphs:
                html_lines.append('<p>' + '<br/>\n'.join(paragraphs) + '</p>')
                paragraphs = []
            if not in_list:
                in_list = True
                html_lines.append('<ul>')
            # Bold with ** inside list
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line[2:].strip())
            html_lines.append(f'<li>{line}</li>')
        else:
            # Bold with **
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            # Italic with __
            line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
            # MD5 hash with [[...]]
            line = re.sub(r'\[\[(.*?)\]\]', lambda match: md5_hash(match.group(1)), line)
            # Remove 'c' with ((...))
            line = re.sub(r'\(\((.*?)\)\)', lambda match: remove_c(match.group(1)), line)
            paragraphs.append(line)
    
    if in_list:
        html_lines.append('</ul>')
    if paragraphs:
        html_lines.append('<p>' + '<br/>\n'.join(paragraphs) + '</p>')

    return '\n'.join(html_lines)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    html_file = sys.argv[2]
    
    try:
        with open(markdown_file, 'r') as md_file:
            markdown_text = md_file.read()
        
        html_content = parse_markdown_to_html(markdown_text)
        
        with open(html_file, 'w') as html_file:
            html_file.write(html_content)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

