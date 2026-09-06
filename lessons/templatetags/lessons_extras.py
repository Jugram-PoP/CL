import re
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def split_into_sections(html, max_words=130):
    """First split by <h2>/<h3>, then further split any long chunk into
    smaller word-count-limited pages. A literal <!--pagebreak--> comment
    anywhere in the content forces a new page at that exact point,
    regardless of word count. <style> and <script> blocks are always
    kept whole, never split. Returns a list of
    (heading, level, page_html, is_last_page) where level is 2 or 3."""
    macro_parts = re.split(r'(<h[23]>.*?</h[23]>)', html, flags=re.DOTALL)
    macro_sections = []
    current_heading = ""
    current_level = 2
    current_html = ""
    for part in macro_parts:
        heading_match = re.match(r'<h([23])>(.*?)</h[23]>', part, flags=re.DOTALL)
        if heading_match:
            if current_html.strip():
                macro_sections.append((current_heading, current_level, current_html))
            current_level = int(heading_match.group(1))
            current_heading = re.sub(r'<[^>]+>', '', heading_match.group(2)).strip()
            current_html = part
        else:
            current_html += part
    if current_html.strip():
        macro_sections.append((current_heading, current_level, current_html))

    final = []
    block_pattern = (
        r'(<!--pagebreak-->'
        r'|<style[^>]*>.*?</style>'
        r'|<script[^>]*>.*?</script>'
        r'|<h4>.*?</h4>'
        r'|<p>.*?</p>'
        r'|<ul>.*?</ul>'
        r'|<ol>.*?</ol>'
        r'|<div class="pw-checker">.*?</div>'
        r'|<div class="[^"]*">.*?</div>'
        r'|<blockquote>.*?</blockquote>)'
    )

    for heading, level, chunk_html in macro_sections:
        raw_blocks = re.split(block_pattern, chunk_html, flags=re.DOTALL)
        blocks = [b for b in raw_blocks if b and b.strip()]

        pages = []
        current_page = ""
        current_words = 0
        for block in blocks:
            if block.strip() == "<!--pagebreak-->":
                if current_page.strip():
                    pages.append(current_page)
                current_page = ""
                current_words = 0
                continue

            is_chrome = bool(re.match(r'^<style[^>]*>', block)) or bool(re.match(r'^<script[^>]*>', block))
            if is_chrome:
                current_page += block
                continue

            block_word_count = len(re.sub(r'<[^>]+>', '', block).split())
            if current_page and current_words + block_word_count > max_words:
                pages.append(current_page)
                current_page = block
                current_words = block_word_count
            else:
                current_page += block
                current_words += block_word_count
        if current_page.strip():
            pages.append(current_page)
        if not pages:
            pages = [chunk_html]

        for i, page_html in enumerate(pages):
            is_last = (i == len(pages) - 1)
            final.append((heading, level, page_html, is_last))

    return final


def build_lesson_pages(lesson):
    """Build the full ordered page sequence for a lesson: each content chunk
    from split_into_sections, followed by one standalone page per
    OpenQuestion attached to that heading (MCQ questions stay inline on
    the content page, open questions each get their own page)."""
    sections = split_into_sections(lesson.content)
    pages = []
    for heading, level, html, is_last in sections:
        page = {"type": "content", "heading": heading, "level": level, "html": html}
        if is_last:
            page["questions"] = lesson.questions.filter(section=heading)
        else:
            page["questions"] = lesson.questions.none()
        pages.append(page)

        if is_last:
            for oq in lesson.open_questions.filter(section=heading):
                pages.append({"type": "open_question", "heading": heading, "level": level, "open_question": oq})
    return pages