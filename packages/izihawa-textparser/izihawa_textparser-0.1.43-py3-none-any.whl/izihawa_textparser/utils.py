import markdownify

import re


BANNED_SECTIONS = {
    "author contribution",
    "data availability statement",
    "declaration of competing interest",
    "acknowledgments",
    "acknowledgements",
    "supporting information",
    "conflict of interest disclosures",
    "conflict of interest",
    "conflict of interest statement",
    "ethics statement",
    "references",
    "external links",
    "further reading",
    "works cited",
    "bibliography",
    "notes",
    "sources",
    "footnotes",
    "suggested readings",
}


class MarkdownConverter(markdownify.MarkdownConverter):
    convert_b = markdownify.abstract_inline_conversion(lambda self: "**")
    convert_i = markdownify.abstract_inline_conversion(lambda self: "__")
    convert_em = markdownify.abstract_inline_conversion(lambda self: "__")

    def convert_header(self, el, text, convert_as_inline):
        return self.convert_hn(2, el, text, convert_as_inline)

    def convert_title(self, el, text, convert_as_inline):
        return self.convert_hn(2, el, text, convert_as_inline)

    def convert_soup(self, soup):
        r = super().convert_soup(soup)
        return re.sub(r"\n{2,}", "\n\n", r).replace("\r\n", "").strip()

    def convert_td(self, el, text, convert_as_inline):
        return ' ' + text.strip().replace("\n", "  ") + ' |'

    def convert_th(self, el, text, convert_as_inline):
        return super().convert_th(el, text.strip().replace("\n", "  "), convert_as_inline)

    def convert_li(self, el, text, convert_as_inline):
        parent = el.parent
        if parent is not None and parent.name == 'ol':
            if parent.get("start"):
                start = int(parent.get("start"))
            else:
                start = 1
            bullet = '%s.' % (start + parent.index(el))
        else:
            depth = -1
            while el:
                if el.name == 'ul':
                    depth += 1
                el = el.parent
            bullets = self.options['bullets']
            bullet = bullets[depth % len(bullets)]
        return '%s %s\n' % (bullet, (text or '').strip().replace('\n'," "))

    def convert_tr(self, el, text, convert_as_inline):
        cells = el.find_all(['td', 'th'])
        is_headrow = (
                all([cell.name == 'th' for cell in cells])
                or (not el.previous_sibling and not el.parent.name == 'tbody')
                or (not el.previous_sibling and el.parent.name == 'tbody' and len(
            el.parent.parent.find_all(['thead'])) < 1)
        )
        overline = ''
        underline = ''
        if is_headrow and not el.previous_sibling:
            # first row and is headline: print headline underline
            underline += '| ' + ' | '.join(['---'] * len(cells)) + ' |' + '\n'
        elif (not el.previous_sibling
              and (el.parent.name == 'table'
                   or (el.parent.name == 'tbody'
                       and not el.parent.previous_sibling))):
            # first row, not headline, and:
            # - the parent is table or
            # - the parent is tbody at the beginning of a table.
            # print empty headline above this row
            overline += '| ' + ' | '.join([''] * len(cells)) + ' |' + '\n'
            overline += '| ' + ' | '.join(['---'] * len(cells)) + ' |' + '\n'
        return overline + '|' + text.strip().replace("\n", "  ") + '\n' + underline

    def convert_blockquote(self, el, text, convert_as_inline):
        if convert_as_inline:
            return text

        return '\n' + (markdownify.line_beginning_re.sub('> ', text.strip()) + '\n\n') if text else ''


md = MarkdownConverter(
    sub_symbol='~',
    sup_symbol='^',
    heading_style=markdownify.ATX,
    newline_style=markdownify.BACKSLASH,
    autolinks=False,
)
