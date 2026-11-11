from pathlib import Path
from html.parser import HTMLParser
import re

site = Path(__file__).resolve().parents[1] / 'outputs' / 'site'

# Expand the compact base CSS without touching text inside strings/comments.
path = site / 'styles.css'
text = path.read_text(encoding='utf-8')
lines, token, indent, quote, escaped = [], '', 0, None, False
for char in text:
    if quote:
        token += char
        if escaped:
            escaped = False
        elif char == '\\':
            escaped = True
        elif char == quote:
            quote = None
        continue
    if char in ('"', "'"):
        quote = char
        token += char
    elif char == '{':
        lines.append('  ' * indent + token.strip() + ' {')
        token = ''
        indent += 1
    elif char == ';':
        if token.strip():
            lines.append('  ' * indent + token.strip() + ';')
        token = ''
    elif char == '}':
        if token.strip():
            lines.append('  ' * indent + token.strip() + ';')
        token = ''
        indent -= 1
        assert indent >= 0, 'Unbalanced CSS braces'
        lines.append('  ' * indent + '}')
        if indent == 0:
            lines.append('')
    elif char in '\n\r':
        token += ' '
    else:
        token += char
assert indent == 0 and quote is None, 'Invalid CSS structure'
if token.strip():
    lines.append(token.strip())
path.write_text('\n'.join(lines).strip() + '\n', encoding='utf-8')

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.assets = [], [], []
        self.stack = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if 'id' in data:
            self.ids.append(data['id'])
        for key in ('href', 'src'):
            value = data.get(key, '')
            if value.startswith('#'):
                self.refs.append(value[1:])
            elif value and not re.match(r'^(https?:|data:)', value):
                self.assets.append(value)
        if tag not in {'meta', 'link', 'img', 'br', 'input', 'hr', 'source', 'area', 'embed', 'wbr'}:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1] == tag, f'Incorrect nesting: {tag} / {self.stack[-5:]}'
        self.stack.pop()
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in self.stack and self.stack[-1] == tag:
            self.stack.pop()

parser = PageParser()
parser.feed((site / 'index.html').read_text(encoding='utf-8'))
assert not parser.stack, f'Unclosed HTML: {parser.stack}'
assert len(parser.ids) == len(set(parser.ids)), 'Duplicate IDs'
assert set(parser.refs) <= set(parser.ids), 'Broken internal links'
for asset in parser.assets:
    assert (site / asset).is_file(), f'Missing asset: {asset}'
required = {'inicio', 'proyecto', 'funcionamiento', 'componentes', 'tecnologia', 'objetivo', 'galeria', 'equipo', 'conclusion'}
assert required <= set(parser.ids), 'Missing section'
for path in site.glob('*.css'):
    css = path.read_text(encoding='utf-8')
    assert css.count('{') == css.count('}'), f'Unbalanced CSS: {path.name}'
assert (site / 'assets' / 'smart-bin.png').stat().st_size > 100_000
print(f'HTML: correctly nested, {len(parser.ids)} unique IDs, {len(parser.refs)} internal references resolved.')
print(f'Assets: {len(parser.assets)} local references verified. All requested sections present.')
print('CSS: balanced rules, readable formatting. Hero image present.')
