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
    out = [f'<div class="pratique" id="pratique-{n}">',
           f'<h3>Pratique: página {n}</h3>',
           '<p class="pr-intro">Responda de cabeça antes de conferir. '
           f'<span class="score">Acertos nas de alternativa: <b>0</b> de {len(mcs)}</span></p>',
           '<ol class="pr-list">']
    for it in items:
        if it[0] == 'mc':
            _, ans, q, opts = it
            out.append(f'<li class="mc" data-answer="{ans}"><p class="q">{q}</p><div class="opts">')
            for letter, o in zip('ABCD', opts):
                out.append(f'<button type="button" data-o="{letter}"><b>{letter})</b> {o}</button>')
            out.append('</div><p class="fb" aria-live="polite"></p></li>')
        else:
            _, q, a = it
            out.append(f'<li class="open"><p class="q">{q}</p><details><summary>Ver resposta esperada</summary>'
                       f'<p>{a}</p></details></li>')
    out.append('</ol></div>')
    return '\n'.join(out)


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
    body = '\n'.join(process(open(os.path.join(SRC, f), encoding='utf-8').read()) for f in order)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(body)
    # contagens
    print('bytes', len(body.encode()))
    print('mc', body.count('class="mc"'), 'open', body.count('class="open"'))


if __name__ == '__main__':
    main()
