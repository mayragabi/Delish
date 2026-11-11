from pathlib import Path
import re

site = Path(__file__).resolve().parents[1] / 'outputs' / 'site'
page = site / 'index.html'
html = page.read_text(encoding='utf-8')
html = re.sub(r'(?<=>)0[1-8] / ', '', html)
html = re.sub(r'<span class="(?:step-number|gallery-number|code-line)">[^<]*</span>\s*', '', html)
html = re.sub(r'<span>0[1-6]</span>', '', html)
html = html.replace('Equipo: Mayra Acosta · Samira Quintana · Juan Bogado', 'Mayra Acosta · Samira Quintana · Juan Bogado')
html = html.replace('Ilustración conceptual de un basurero con dos sensores, tapa abierta y una mano activando la detección', 'Ilustración conceptual de un basurero ecológico verde con símbolo de reciclaje, sensores y una mano activando la apertura')
assert 'step-number' not in html and 'gallery-number' not in html and 'code-line' not in html
assert not re.search(r'>0[1-8](?: /)?<', html)
page.write_text(html, encoding='utf-8')

css_file = site / 'sections.css'
css = css_file.read_text(encoding='utf-8')
css = re.sub(r'^\s*\.(?:step-number|gallery-number|code-line|member-number|member-role|member-avatar)(?:\s+\.icon)?\s*\{[^}]*\}\n', '', css, flags=re.M)
css = re.sub(r'^\.team-card:nth-child\(even\) \.member-avatar\s*\{[^}]*\}\n', '', css, flags=re.M)
css = css.replace('.member-role, .gallery-card figcaption p', '.gallery-card figcaption p')
css = css.replace('top: 72px; height: 1px;', 'top: 32px; height: 1px;')
css = css.replace('top: 71px; left: 30px;', 'top: 31px; left: 30px;')
css = css.replace('margin: 18px 0 25px;', 'margin: 0 0 25px;')
css = css.replace('padding: 0 0 26px 104px;', 'padding: 0 0 26px 86px;')
css += '\n/* Tarjetas del equipo: únicamente nombres. */\n.team-card { text-align: center; padding-block: 42px; }\n'
css_file.write_text(css, encoding='utf-8')
print('Removed decorative numbering from headings, tags, steps, components, code and gallery.')
print('Team cards now show only the three names; demo uses phase labels.')
