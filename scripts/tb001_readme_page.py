"""Dependency-free UTF-8 documentation page; preserve a BOM-tagged raw download."""
from html import escape

def write_readme_page(out):
    source=out/'README.md'
    if not source.exists(): return
    text=source.read_text(encoding='utf-8-sig')
    # Raw Markdown served without a charset remains unambiguous to browsers.
    source.write_text(text,encoding='utf-8-sig')
    blocks=[];code=False
    for line in text.splitlines():
        if line.startswith('```'):
            blocks.append('</code></pre>' if code else '<pre><code>');code=not code
        elif code: blocks.append(escape(line)+'\n')
        elif line.startswith('#') and ' ' in line:
            prefix,title=line.split(' ',1);level=min(len(prefix),6)
            blocks.append(f'<h{level}>{escape(title)}</h{level}>')
        elif line.startswith('- '):blocks.append('<p class="bullet">• '+escape(line[2:])+'</p>')
        elif line.strip():blocks.append('<p>'+escape(line)+'</p>')
    if code:blocks.append('</code></pre>')
    (out/'README.html').write_text('''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TB001 工程說明</title><style>body{max-width:850px;margin:48px auto;padding:0 24px;background:#faf7f1;color:#392f27;font:17px/1.8 system-ui}h1,h2,h3{line-height:1.4}h2{margin-top:2em}a{color:#775038}pre{overflow:auto;background:#eee8df;padding:18px}.bullet{margin:.3em 0}</style><nav><a href="TB001_D07_viewer.html">← 互動檢視</a> · <a href="README.md" download>下載 Markdown</a></nav><main>'''+''.join(blocks)+'</main></html>',encoding='utf-8')
