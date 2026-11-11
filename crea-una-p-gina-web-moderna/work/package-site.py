from pathlib import Path
import base64
import zipfile

root = Path(__file__).resolve().parents[1]
site = root / 'outputs' / 'site'
html = (site / 'index.html').read_text(encoding='utf-8')
for stylesheet in ('styles.css', 'sections.css'):
    html = html.replace(
        f'<link rel="stylesheet" href="{stylesheet}">',
        '<style>\n' + (site / stylesheet).read_text(encoding='utf-8') + '</style>'
    )
html = html.replace(
    '<script src="script.js" defer></script>',
    ''
)
html = html.replace(
    '</body>',
    '<script>\n' + (site / 'script.js').read_text(encoding='utf-8') + '\n</script>\n</body>'
)
image = base64.b64encode((site / 'assets' / 'smart-bin.png').read_bytes()).decode('ascii')
html = html.replace('src="assets/smart-bin.png"', f'src="data:image/png;base64,{image}"')
single = root / 'outputs' / 'Basurero-Inteligente.html'
single.write_text(html, encoding='utf-8')
archive = root / 'outputs' / 'Basurero-Inteligente-codigo.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
    for file in sorted(site.rglob('*')):
        if file.is_file():
            bundle.write(file, 'Basurero-Inteligente/' + file.relative_to(site).as_posix())
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None, 'Invalid archive'
    assert len(bundle.namelist()) == 6
assert 'src="script.js"' not in html and 'href="styles.css"' not in html
assert 'data:image/png;base64,' in html
print('Standalone page:', single.name, single.stat().st_size, 'bytes')
print('Source archive:', archive.name, archive.stat().st_size, 'bytes, 6 verified files')
