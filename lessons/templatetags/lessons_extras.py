from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

import re

def split_into_sections(html):
    """Split lesson HTML into a list of (heading_text, section_html) chunks,
    breaking at every <h2> AND <h3>. Content before the first heading becomes
    a chunk with heading_text = "" (the module overview)."""
    parts = re.split(r'(<h[23]>.*?</h[23]>)', html, flags=re.DOTALL)
    sections = []
    current_heading = ""
    current_html = ""
    for part in parts:
        heading_match = re.match(r'<h[23]>(.*?)</h[23]>', part, flags=re.DOTALL)
        if heading_match:
            if current_html.strip():
                sections.append((current_heading, current_html))
            current_heading = re.sub(r'<[^>]+>', '', heading_match.group(1)).strip()
            current_html = part
        else:
            current_html += part
    if current_html.strip():
        sections.append((current_heading, current_html))
    return sections