#!/usr/bin/env python3
"""Monta index.html a partir dos parciais em src/.
Formato especial dentro dos parciais:
@pratique N
@mc B :: Pergunta :: alt A :: alt B :: alt C :: alt D
@open :: Pergunta :: Resposta esperada
@end
"""
import os, re, html, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
OUT = os.path.dirname(ROOT)


def render_pratique(n, items):
    mcs = [i for i in items if i[0] == 'mc']
    out = [f'<div class="pratica" id="pratique-{n}"><h3 class="prat-h">Pratique: página {n}</h3>',
           f'<p class="prat-sub">Responda de cabeça antes de conferir. Acertos nas de alternativa: <span class="placar">0 de {len(mcs)}</span></p>']
    k = 0
    for it in items:
        k += 1
        if it[0] == 'mc':
            _, ans, q, opts = it
            certa = 'ABCD'.index(ans)
            out.append(f'<div class="q mc" data-certa="{certa}"><p class="perg"><span class="qn">{k}.</span> {q}</p><div class="ops">')
            for i, (letter, o) in enumerate(zip('ABCD', opts)):
                out.append(f'<button type="button" class="op" data-i="{i}">{letter}) {o}</button>')
            out.append('</div><p class="fb" hidden><b class="fbt"></b></p></div>')
        else:
            _, q, a = it
            out.append(f'<div class="q ab"><p class="perg"><span class="qn">{k}.</span> {q}</p><details><summary>Ver resposta esperada</summary><p>{a}</p></details></div>')
    out.append('</div>')
    return '\n'.join(out)


def estilo_capitaes(html):
    import re as _re
    html = _re.sub(r'<p class="pg-label">(Página \d+)</p>\s*<h2>([\s\S]*?)</h2>',
                   r'<header class="pag-head"><span class="pag-num">\1</span><h2>\2</h2></header>', html)
    html = html.replace('<article class="cena"', '<article class="cap"')
    html = html.replace('<nav class="nesta"', '<nav class="toc"')
    html = html.replace('<div class="tabela-wrap">', '<div class="tbl">')
    html = html.replace('<div class="analise">\n<h4>Análise</h4>', '<div class="analise">\n<p class="rotulo">Análise</p>')
    html = html.replace('<h4>Análise</h4>', '<p class="rotulo">Análise</p>')
    html = _re.sub(r'<h3([^>]*)>★ ', r'<h3\1><span class="star" aria-label="cena importante">★</span> ', html)
    return html


def process(text):
    lines = text.split('\n')
    res, items, n, inside = [], [], None, False
    for ln in lines:
        s = ln.strip()
        if s.startswith('@pratique'):
            inside, n, items = True, s.split()[1], []
            continue
        if inside:
            if s == '@end':
                res.append(render_pratique(n, items)); inside = False
            elif s.startswith('@mc'):
                head, *rest = [p.strip() for p in s[3:].split('::')]
                items.append(('mc', head.strip(), rest[0], rest[1:5]))
            elif s.startswith('@open'):
                parts = [p.strip() for p in s[5:].split('::')]
                items.append(('open', parts[1], parts[2]))
            elif s:
                raise SystemExit(f'linha estranha na prática: {s}')
            continue
        res.append(ln)
    return '\n'.join(res)


def main():
    order = sorted(f for f in os.listdir(SRC) if f.endswith('.html'))
    body = estilo_capitaes('\n'.join(process(open(os.path.join(SRC, f), encoding='utf-8').read()) for f in order))
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(body)
    # contagens
    print('bytes', len(body.encode()))
    print('mc', body.count('class="mc"'), 'open', body.count('class="open"'))


if __name__ == '__main__':
    main()
