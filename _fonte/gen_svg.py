#!/usr/bin/env python3
"""Gera as ilustrações SVG do site (estilo noturno, chapado)."""
import os, random
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'img')
os.makedirs(OUT, exist_ok=True)

W, H = 800, 450
SKY = ('#0a0e1c', '#1b2444')
GOLD = '#e6b85c'; GOLD2 = '#f3d59a'; ROSE = '#e27d8f'; BLUE = '#7fa7e0'
INK = '#06080f'; DARK = '#121827'; MID = '#232c45'; WALL = '#2c3553'


def svg(body, title, w=W, h=H, sky=SKY, extra_defs=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
<title>{title}</title>
<defs>
<linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky[0]}"/><stop offset="1" stop-color="{sky[1]}"/></linearGradient>
<radialGradient id="luz" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{GOLD2}" stop-opacity=".9"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<radialGradient id="luzfraca" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{GOLD2}" stop-opacity=".45"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
{extra_defs}
</defs>
<rect width="{w}" height="{h}" fill="url(#ceu)"/>
{body}
</svg>'''


def stars(n, seed, ymax=260, w=W):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = r.uniform(0, w), r.uniform(4, ymax)
        s = r.choice([0.8, 1, 1.2, 1.6])
        o = r.uniform(.35, 1)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s}" fill="#fff" opacity="{o:.1f}"/>')
    return '\n'.join(out)


def mountains(y, color, seed, w=W, amp=60):
    r = random.Random(seed)
    pts = [f'0,{H}', f'0,{y}']
    x = 0
    while x < w:
        x += r.uniform(60, 140)
        pts.append(f'{x:.0f},{y - r.uniform(0, amp):.0f}')
    pts += [f'{w},{y}', f'{w},{H}']
    return f'<polygon points="{" ".join(pts)}" fill="{color}"/>'


def person(x, y, s=1.0, color=INK, dress=False, hair=None, hat=False, cane=False, guitar=False):
    """Silhueta simples. (x,y) = pés no chão."""
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    if dress:
        g.append(f'<path d="M-16,0 L-10,-58 Q0,-66 10,-58 L16,0 Z" fill="{color}"/>')
    else:
        g.append(f'<rect x="-11" y="-40" width="8" height="40" rx="3" fill="{color}"/><rect x="3" y="-40" width="8" height="40" rx="3" fill="{color}"/>')
        g.append(f'<path d="M-13,-38 L-12,-70 Q0,-78 12,-70 L13,-38 Z" fill="{color}"/>')
    top = -66 if dress else -78
    g.append(f'<rect x="-3" y="{top-8}" width="6" height="9" fill="{color}"/>')
    g.append(f'<circle cx="0" cy="{top-17}" r="11" fill="{color}"/>')
    if hair:
        g.append(f'<path d="M-11,{top-19} Q0,{top-34} 11,{top-19} Q8,{top-26} 0,{top-27} Q-8,{top-26} -11,{top-19}Z" fill="{hair}"/>')
    if hat:
        g.append(f'<rect x="-14" y="{top-27}" width="28" height="4" rx="2" fill="{color}"/><rect x="-8" y="{top-38}" width="16" height="12" rx="3" fill="{color}"/>')
    if cane:
        g.append(f'<line x1="16" y1="{top+20}" x2="22" y2="0" stroke="{color}" stroke-width="3" stroke-linecap="round"/>')
    if guitar:
        g.append(f'<g transform="translate(6,{top+40}) rotate(-35)"><ellipse cx="0" cy="12" rx="11" ry="13" fill="#8a5a2b"/><ellipse cx="0" cy="-4" rx="8" ry="9" fill="#8a5a2b"/><circle cx="0" cy="6" r="3" fill="#1a1006"/><rect x="-1.6" y="-36" width="3.2" height="32" fill="#5a3a1b"/></g>')
    g.append('</g>')
    return ''.join(g)


def chalet(x, y, w, h, wall=WALL, roof='#3a2a2a', lit=True, door=True):
    out = [f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{wall}"/>',
           f'<polygon points="{x-10},{y-h} {x+w/2},{y-h-h*0.55} {x+w+10},{y-h}" fill="{roof}"/>']
    ww = w * 0.2
    for i, wx in enumerate([x + w * 0.15, x + w * 0.65]):
        fill = GOLD if lit and i == 0 else '#1a2036'
        out.append(f'<rect x="{wx}" y="{y-h*0.7}" width="{ww}" height="{h*0.3}" fill="{fill}"/>')
    if door:
        out.append(f'<rect x="{x+w*0.43}" y="{y-h*0.55}" width="{w*0.14}" height="{h*0.55}" fill="#151a2b"/>')
    return ''.join(out)


def tree(x, y, s=1, color='#0f1a17'):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-5" y="-60" width="10" height="60" fill="#1a130d"/>'
            f'<circle cx="0" cy="-80" r="38" fill="{color}"/><circle cx="-28" cy="-62" r="26" fill="{color}"/><circle cx="28" cy="-64" r="28" fill="{color}"/></g>')


def lamp(x, y, h=150):
    return (f'<circle cx="{x}" cy="{y-h}" r="60" fill="url(#luzfraca)"/>'
            f'<rect x="{x-2}" y="{y-h}" width="4" height="{h}" fill="#0b0d14"/>'
            f'<rect x="{x-7}" y="{y-h-12}" width="14" height="14" rx="2" fill="{GOLD2}"/>')


def write(name, content):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(content)

# ---------------- HERO: Clara na janela, céu, violão
body = stars(160, 1, 300) + mountains(330, '#141a30', 2, amp=70) + mountains(360, '#10152a', 3, amp=40)
body += '<path d="M610,70 l6,18 l-6,18 l-6,-18z" fill="#fff" opacity=".9"/>'  # estrela grande
# Cruzeiro do Sul
for cx, cy, r in [(640, 60, 3.2), (640, 120, 3.6), (612, 92, 2.8), (668, 88, 2.8), (650, 104, 1.6)]:
    body += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>'
body += '<ellipse cx="700" cy="120" rx="34" ry="22" fill="#05070d" opacity=".95"/>'  # mancha negra
# casa
body += '<rect x="80" y="170" width="380" height="280" fill="#232c47"/><polygon points="60,170 270,70 480,170" fill="#3b2a2c"/>'
body += '<rect x="200" y="230" width="140" height="140" fill="url(#luz)"/>'
body += '<rect x="215" y="245" width="110" height="115" fill="#f0c97a"/>'
body += '<rect x="215" y="245" width="110" height="115" fill="none" stroke="#1a1f30" stroke-width="8"/><line x1="270" y1="245" x2="270" y2="360" stroke="#1a1f30" stroke-width="5"/>'
body += person(270, 362, 1.05, '#2a1a14', dress=True, hair='#140c08')
body += '<rect x="205" y="356" width="130" height="10" fill="#141a2a"/>'
body += person(420, 450, 1.25, '#0b0e17', guitar=True)
body += tree(560, 450, 1.6, '#0c1513') + tree(740, 450, 1.3, '#0e1816')
body += '<rect x="0" y="440" width="800" height="10" fill="#0b0f19"/>'
write('hero.svg', svg(body, 'Clara na janela olhando o céu; um tocador de violão na rua'))

# ---------------- FICHA: casinha + trem + montanhas
body = stars(90, 4, 220) + mountains(250, '#18203b', 5, amp=80) + mountains(290, '#121831', 6, amp=50)
body += '<rect x="0" y="330" width="800" height="120" fill="#0e1322"/>'
body += '<rect x="0" y="318" width="800" height="5" fill="#2b3350"/><rect x="0" y="328" width="800" height="3" fill="#2b3350"/>'
for i in range(6):
    x = 380 + i * 70
    body += f'<rect x="{x}" y="270" width="64" height="46" rx="4" fill="#1e2740"/>'
    for j in range(3):
        body += f'<rect x="{x+6+j*19}" y="280" width="14" height="12" fill="{GOLD}" opacity=".85"/>'
body += '<rect x="330" y="262" width="52" height="54" rx="6" fill="#2a3352"/><circle cx="342" cy="290" r="8" fill="#fff6d0"/>'
body += '<polygon points="330,290 230,330 230,250" fill="#fff6d0" opacity=".08"/>'
body += chalet(70, 330, 150, 90) + tree(260, 330, 1.0)
body += lamp(240, 330, 120)
write('ficha.svg', svg(body, 'Casinha de subúrbio à noite com trem iluminado passando'))

# ---------------- AUTOR: mesa com papéis, lampião, garrafa, jornal
body = '<rect x="0" y="0" width="800" height="450" fill="#151827"/>'
body += '<rect x="560" y="40" width="180" height="230" fill="#0f1220"/>' + stars(30, 7, 260, 800).replace('<circle', '<circle clip-path="url(#jan)"')
body += '<rect x="560" y="40" width="180" height="230" fill="none" stroke="#2c3553" stroke-width="10"/><line x1="650" y1="40" x2="650" y2="270" stroke="#2c3553" stroke-width="6"/>'
body += '<circle cx="250" cy="170" r="160" fill="url(#luz)" opacity=".55"/>'
body += '<rect x="0" y="300" width="800" height="150" fill="#2a1d14"/><rect x="0" y="296" width="800" height="8" fill="#3a2a1c"/>'
body += '<path d="M240,300 L240,230 Q250,215 260,230 L260,300 Z" fill="#7a5a2a"/><ellipse cx="250" cy="212" rx="20" ry="26" fill="#fff3c4" opacity=".9"/><rect x="236" y="190" width="28" height="8" fill="#3a2a1c"/>'
body += '<rect x="330" y="250" width="200" height="60" fill="#e9e1cc" transform="rotate(-4 430 280)"/>'
for k in range(6):
    body += f'<line x1="345" y1="{262+k*8}" x2="{500-k*6}" y2="{258+k*8}" stroke="#7d7564" stroke-width="2"/>'
body += '<rect x="420" y="248" width="150" height="56" fill="#d8ceb2" transform="rotate(6 495 276)"/><text x="440" y="276" font-family="Georgia,serif" font-size="16" fill="#3a3326" transform="rotate(6 495 276)">JORNAL</text>'
body += '<rect x="610" y="225" width="22" height="75" rx="6" fill="#2f5a3a" opacity=".9"/><rect x="616" y="208" width="10" height="20" fill="#2f5a3a"/>'
body += '<ellipse cx="160" cy="292" rx="26" ry="8" fill="#d9d2c0"/><rect x="140" y="268" width="40" height="24" rx="4" fill="#efe8d6"/>'
body += '<line x1="380" y1="300" x2="450" y2="240" stroke="#c9a74a" stroke-width="4" stroke-linecap="round"/>'
write('autor.svg', svg(body, 'Mesa de escritor com papéis, jornal, garrafa e lampião', extra_defs='<clipPath id="jan"><rect x="560" y="40" width="180" height="230"/></clipPath>'))

# ---------------- PRÉ-MODERNISMO: linha do tempo
body = '<rect width="800" height="450" fill="#121625"/>'
body += '<line x1="60" y1="230" x2="740" y2="230" stroke="#3a4466" stroke-width="6" stroke-linecap="round"/>'
marks = [(100, '1881', 'Realismo / Naturalismo', '#6c7aa6'), (290, '1902', 'Início do Pré-Modernismo', BLUE),
         (500, '1921–22', 'Clara dos Anjos escrito', GOLD), (690, '1922', 'Semana de Arte Moderna', ROSE)]
for x, ano, txt, c in marks:
    body += f'<circle cx="{x}" cy="230" r="14" fill="{c}"/><text x="{x}" y="190" text-anchor="middle" font-family="Georgia,serif" font-size="26" fill="#fff">{ano}</text>'
    body += f'<text x="{x}" y="275" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="#d6d0c2">{txt}</text>'
body += '<rect x="300" y="300" width="350" height="40" rx="20" fill="#1f2a48"/><text x="475" y="326" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" fill="#f3d59a">Pré-Modernismo: denúncia e transição</text>'
body += '<text x="400" y="80" text-anchor="middle" font-family="Georgia,serif" font-size="30" fill="#f3d59a">Entre o Realismo e a Semana de 22</text>'
write('premodernismo.svg', svg(body, 'Linha do tempo: Realismo, Pré-Modernismo e Semana de 22'))

# ---------------- CAP1: solo debaixo do tamarineiro
body = '<rect width="800" height="450" fill="#1b2a38"/>' + '<rect width="800" height="450" fill="url(#ceu)" opacity=".4"/>'
body += '<circle cx="680" cy="80" r="40" fill="#f6e7b0" opacity=".9"/>'
body += mountains(260, '#22364a', 8, amp=70)
body += '<rect x="0" y="300" width="800" height="150" fill="#1d2b22"/>'
body += '<rect x="380" y="120" width="26" height="200" fill="#2b1d12"/>'
for cx, cy, r in [(393, 110, 120), (290, 150, 80), (500, 150, 85), (393, 60, 80)]:
    body += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#162619"/>'
body += '<rect x="260" y="300" width="260" height="14" rx="4" fill="#5a3d22"/><rect x="280" y="314" width="10" height="60" fill="#4a3220"/><rect x="490" y="314" width="10" height="60" fill="#4a3220"/>'
body += '<rect x="378" y="268" width="16" height="34" rx="4" fill="#cfe3d7" opacity=".55"/><rect x="383" y="258" width="6" height="12" fill="#cfe3d7" opacity=".55"/>'
for i, x in enumerate([300, 340, 430, 470]):
    body += f'<rect x="{x}" y="294" width="20" height="5" fill="#f2efe4" transform="rotate({(-8+i*6)} {x+10} 296)"/>'
body += person(225, 380, 1.05, '#101820', hat=False)
body += person(575, 380, 1.05, '#101820', cane=True)
body += person(400, 395, 1.0, '#0c131a')
body += chalet(620, 330, 160, 110, wall='#2a3a4c', lit=True)
write('cap1-solo.svg', svg(body, 'Três homens jogando cartas debaixo de um tamarineiro'))

# ---------------- CAP2: Cassi, pastinha, violão e galos
body = '<rect width="800" height="450" fill="#161a2a"/>' + '<rect x="0" y="330" width="800" height="120" fill="#10131f"/>'
body += '<circle cx="330" cy="170" r="190" fill="url(#luzfraca)"/>'
for i in range(3):
    x = 520 + i * 90
    body += f'<rect x="{x}" y="250" width="80" height="80" fill="none" stroke="#6b5a3a" stroke-width="3"/>'
    for k in range(1, 5):
        body += f'<line x1="{x+k*16}" y1="250" x2="{x+k*16}" y2="330" stroke="#6b5a3a" stroke-width="2"/>'
    body += f'<path d="M{x+25},315 q10,-30 30,-25 q8,-12 0,-18 q14,2 10,16 q10,10 0,27 z" fill="#b8442e"/>'
body += f'<g transform="translate(300,420) scale(2.3)">'
body += '<path d="M-14,0 L-12,-38 L12,-38 L14,0 Z" fill="#1c2236"/><path d="M-16,-38 L-14,-82 Q0,-92 14,-82 L16,-38 Z" fill="#26304c"/>'
body += '<path d="M-4,-82 L0,-60 L4,-82 Z" fill="#c8b98e"/><rect x="-4" y="-92" width="8" height="10" fill="#e4c3a0"/>'
body += '<ellipse cx="0" cy="-104" rx="12" ry="14" fill="#e8c8a6"/>'
body += '<path d="M-12,-108 Q-12,-122 0,-122 Q12,-122 12,-108 Q8,-116 1,-116 L0,-110 L-1,-116 Q-8,-116 -12,-108Z" fill="#2b1a0c"/>'
for sx, sy in [(-5, -102), (4, -101), (-2, -98), (6, -105)]:
    body += f'<circle cx="{sx}" cy="{sy}" r=".9" fill="#a8693a"/>'
body += '<g transform="translate(10,-52) rotate(-40)"><ellipse cx="0" cy="12" rx="11" ry="13" fill="#9a6532"/><ellipse cx="0" cy="-4" rx="8" ry="9" fill="#9a6532"/><circle cx="0" cy="6" r="3" fill="#1a1006"/><rect x="-1.6" y="-38" width="3.2" height="34" fill="#5a3a1b"/></g>'
body += '</g>'
write('cap2-cassi.svg', svg(body, 'Cassi com cabelo repartido ao meio, violão e gaiolas de galos de briga'))

# ---------------- CAP4: baile
body = '<rect width="800" height="450" fill="#2a2433"/>' + '<rect x="0" y="360" width="800" height="90" fill="#3a2a22"/>'
body += '<rect x="0" y="0" width="800" height="40" fill="#1f1a26"/>'
for x in [120, 400, 680]:
    body += f'<circle cx="{x}" cy="60" r="70" fill="url(#luzfraca)"/><circle cx="{x}" cy="50" r="10" fill="{GOLD2}"/>'
body += '<path d="M0,40 Q100,70 200,40 Q300,70 400,40 Q500,70 600,40 Q700,70 800,40" fill="none" stroke="#e27d8f" stroke-width="3" opacity=".7"/>'
body += person(170, 400, 1.15, '#14111c', dress=True) + person(205, 400, 1.15, '#14111c')
body += person(330, 400, 1.1, '#14111c', dress=True) + person(360, 400, 1.1, '#14111c')
body += person(640, 405, 1.35, '#0d0b12', guitar=True)
body += person(500, 405, 1.25, '#f1e6d2', dress=True, hair='#1a110a')
body += '<path d="M610,250 q-40,-30 -90,-10" fill="none" stroke="#f3d59a" stroke-width="2" stroke-dasharray="4 6"/>'
body += '<text x="560" y="230" font-family="Georgia,serif" font-size="22" fill="#f3d59a">♪ ♫</text>'
body += person(80, 405, 1.15, '#14111c', cane=True)
write('cap4-baile.svg', svg(body, 'Baile pequeno; Cassi toca violão olhando Clara'))

# ---------------- CAP5: venda
body = '<rect width="800" height="450" fill="#1d1a20"/>' + '<rect x="0" y="360" width="800" height="90" fill="#2a2018"/>'
body += '<rect x="40" y="40" width="720" height="180" fill="#2a2228"/>'
for row in range(3):
    body += f'<rect x="60" y="{80+row*55}" width="680" height="6" fill="#5a4030"/>'
    for i in range(20):
        c = random.Random(row*50+i).choice(['#3f6e4a', '#7a3e2a', '#c9a74a', '#5a5aa0', '#a0a0a0'])
        body += f'<rect x="{70+i*33}" y="{50+row*55}" width="12" height="30" rx="3" fill="{c}" opacity=".85"/>'
body += '<rect x="80" y="260" width="640" height="100" fill="#4a3424"/><rect x="70" y="252" width="660" height="12" fill="#6a4a30"/>'
body += '<circle cx="400" cy="30" r="120" fill="url(#luzfraca)"/><circle cx="400" cy="30" r="12" fill="#f3d59a"/>'
body += person(400, 300, 1.0, '#120f12')  # nascimento atrás balcão (cortado)
body += person(170, 420, 1.15, '#0e0c10', cane=True) + person(250, 420, 1.1, '#0e0c10')
body += person(600, 420, 1.15, '#0e0c10', hat=True) + person(680, 420, 1.0, '#0e0c10')
for x in [120, 330, 520]:
    body += f'<rect x="{x}" y="380" width="44" height="6" fill="#6a4a30"/><line x1="{x+6}" y1="386" x2="{x+38}" y2="420" stroke="#6a4a30" stroke-width="4"/><line x1="{x+38}" y1="386" x2="{x+6}" y2="420" stroke="#6a4a30" stroke-width="4"/>'
write('cap5-venda.svg', svg(body, 'Venda de subúrbio com balcão, prateleiras e fregueses conversando'))

# ---------------- CAP7: subúrbio
body = stars(40, 9, 120) + '<rect width="800" height="450" fill="#2a3a5a" opacity=".35"/>'
body += '<path d="M0,300 Q150,120 330,170 Q480,90 640,180 Q720,150 800,200 L800,450 L0,450Z" fill="#2a3a2e"/>'
r = random.Random(11)
for i in range(16):
    x = 40 + i * 46 + r.uniform(-6, 6); y = 230 + abs(400 - x) * 0.12 + r.uniform(-10, 10)
    c = r.choice(['#5a6070', '#7a6a5a', '#6a7a80', '#8a7a60'])
    body += f'<rect x="{x}" y="{y}" width="34" height="26" fill="{c}"/><polygon points="{x-3},{y} {x+17},{y-12} {x+37},{y}" fill="#8a8f99"/>'
    if r.random() < .5: body += f'<rect x="{x+12}" y="{y+8}" width="8" height="8" fill="{GOLD}"/>'
body += '<rect x="0" y="360" width="800" height="90" fill="#1c1a16"/>'
body += '<rect x="0" y="345" width="800" height="5" fill="#3a4160"/><rect x="0" y="356" width="800" height="3" fill="#3a4160"/>'
for i in range(7):
    x = 60 + i * 100
    body += f'<rect x="{x}" y="300" width="94" height="44" rx="4" fill="#3a2e28"/>'
    for j in range(4):
        body += f'<rect x="{x+6+j*22}" y="308" width="16" height="12" fill="{GOLD}" opacity=".9"/>'
        body += person(x + 14 + j * 22, 344, 0.3, '#100c0a')
    body += person(x + 92, 344, 0.38, '#100c0a')
body += '<g transform="translate(120,430)"><ellipse cx="0" cy="-14" rx="20" ry="11" fill="#d8d0c0"/><rect x="-14" y="-6" width="3" height="10" fill="#d8d0c0"/><rect x="10" y="-6" width="3" height="10" fill="#d8d0c0"/><circle cx="22" cy="-22" r="7" fill="#d8d0c0"/></g>'
body += '<g transform="translate(650,436)"><ellipse cx="0" cy="-8" rx="9" ry="7" fill="#e8e2d4"/><circle cx="8" cy="-14" r="4" fill="#e8e2d4"/></g>'
write('cap7-suburbio.svg', svg(body, 'Morro de barracos, bichos na rua e trem lotado'))

# ---------------- CAP7: Leonardo Flores discursando
body = '<rect width="800" height="450" fill="#1e1b26"/>' + '<rect x="0" y="360" width="800" height="90" fill="#2a2420"/>'
body += '<rect x="520" y="70" width="140" height="170" fill="#3a2e22"/><rect x="532" y="82" width="116" height="146" fill="#5a4636"/><ellipse cx="590" cy="140" rx="30" ry="38" fill="#2a1e16"/><rect x="560" y="170" width="60" height="58" fill="#2a1e16"/>'
body += '<rect x="60" y="120" width="120" height="240" fill="#2a2f3a"/>'
for k in range(5):
    body += f'<rect x="70" y="{130+k*45}" width="100" height="6" fill="#4a5060"/>'
    for b in range(6):
        body += f'<rect x="{74+b*16}" y="{110+k*45}" width="10" height="20" fill="#7a6a5a"/>'
body += '<circle cx="380" cy="90" r="150" fill="url(#luzfraca)"/>'
# Flores braços abertos
body += '<g transform="translate(360,400) scale(1.6)"><rect x="-11" y="-40" width="8" height="40" rx="3" fill="#0e0c12"/><rect x="3" y="-40" width="8" height="40" rx="3" fill="#0e0c12"/><path d="M-13,-38 L-12,-70 Q0,-78 12,-70 L13,-38 Z" fill="#0e0c12"/><line x1="-12" y1="-68" x2="-42" y2="-96" stroke="#0e0c12" stroke-width="7" stroke-linecap="round"/><line x1="12" y1="-68" x2="42" y2="-96" stroke="#0e0c12" stroke-width="7" stroke-linecap="round"/><circle cx="0" cy="-90" r="11" fill="#0e0c12"/><path d="M-6,-82 L0,-66 L6,-82Z" fill="#0e0c12"/></g>'
# Meneses sentado
body += '<g transform="translate(600,400) scale(1.4)"><rect x="-20" y="-40" width="40" height="8" fill="#3a2e22"/><rect x="-18" y="-32" width="4" height="32" fill="#3a2e22"/><rect x="14" y="-32" width="4" height="32" fill="#3a2e22"/><path d="M-12,-40 L-10,-76 Q0,-84 10,-76 L12,-40Z" fill="#0e0c12"/><circle cx="0" cy="-92" r="11" fill="#0e0c12"/><path d="M-10,-88 Q0,-62 10,-88 Z" fill="#e6e0d0"/></g>'
body += '<text x="250" y="70" font-family="Georgia,serif" font-style="italic" font-size="24" fill="#f3d59a">"Pois eu não vendo"</text>'
write('cap7-flores.svg', svg(body, 'Leonardo Flores discursando de braços abertos diante de Meneses'))

# ---------------- CAP8: cartas
body = '<rect width="800" height="450" fill="#232030"/>' + '<rect x="0" y="360" width="800" height="90" fill="#33281f"/>'
body += '<rect x="560" y="60" width="160" height="200" fill="#151a2c"/>' + '<rect x="560" y="60" width="160" height="200" fill="none" stroke="#3a4060" stroke-width="10"/>'
body += '<circle cx="400" cy="160" r="170" fill="url(#luzfraca)"/>'
body += person(300, 410, 1.6, '#0f0d14', cane=False)
body += '<path d="M294,268 q-6,10 -4,22 q8,10 12,0 q2,-12 -8,-22z" fill="#e6e0d0"/>'  # barba
body += '<rect x="220" y="360" width="50" height="34" rx="4" fill="#4a2e1c"/><rect x="236" y="354" width="18" height="8" rx="3" fill="#4a2e1c"/>'
body += person(470, 410, 1.55, '#d9c6b0', dress=True, hair='#1a110a')
body += '<g transform="translate(385,300) rotate(-10)"><rect x="-26" y="-17" width="52" height="34" fill="#f3ead2"/><polyline points="-26,-17 0,4 26,-17" fill="none" stroke="#b8a678" stroke-width="2"/><circle cx="0" cy="4" r="5" fill="#b23a3a"/></g>'
body += '<line x1="330" y1="290" x2="362" y2="298" stroke="#0f0d14" stroke-width="9" stroke-linecap="round"/><line x1="448" y1="290" x2="408" y2="300" stroke="#d9c6b0" stroke-width="9" stroke-linecap="round"/>'
write('cap8-cartas.svg', svg(body, 'Meneses entregando uma carta escondida a Clara'))

# ---------------- CAP8: ladeira, chuva, crime
rain = ''.join(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x-8:.0f}" y2="{y+24:.0f}" stroke="#9fb3d6" stroke-width="1.2" opacity=".35"/>' for x, y in
               [(random.Random(i).uniform(0, 820), random.Random(i * 7).uniform(-20, 440)) for i in range(70)])
body = '<rect width="800" height="450" fill="#070a12"/>' + mountains(200, '#0b1020', 12, amp=60)
body += '<path d="M0,450 L0,380 L800,250 L800,450Z" fill="#141722"/>'
body += tree(120, 400, 1.7, '#0a120f') + tree(700, 270, 1.8, '#0a120f') + tree(560, 300, 1.4, '#0b1411')
body += '<circle cx="330" cy="200" r="70" fill="url(#luzfraca)" opacity=".7"/>' + lamp(330, 330, 130).replace('fill="url(#luzfraca)"', 'fill="none"')
body += person(260, 350, 1.15, '#2b3040', cane=True)
body += person(560, 300, 1.15, '#000') + person(600, 296, 1.15, '#000')
body += '<line x1="572" y1="230" x2="545" y2="200" stroke="#000" stroke-width="5" stroke-linecap="round"/><line x1="612" y1="226" x2="640" y2="196" stroke="#000" stroke-width="5" stroke-linecap="round"/>'
body += rain
write('cap8-ladeira.svg', svg(body, 'Ladeira escura à noite sob chuva; um homem de bengala e duas sombras à espera', sky=('#05070d', '#0e1426')))

# ---------------- CAP9: beco com Inês
body = '<rect width="800" height="450" fill="#15131a"/>'
body += '<polygon points="0,0 260,60 260,450 0,450" fill="#26222c"/><polygon points="800,0 540,60 540,450 800,450" fill="#2a2530"/>'
for y in [100, 190, 280]:
    body += f'<rect x="60" y="{y}" width="60" height="70" fill="#3a3040"/><rect x="170" y="{y+10}" width="50" height="60" fill="#3a3040"/>'
    body += f'<rect x="590" y="{y+10}" width="50" height="60" fill="#3a3040"/><rect x="680" y="{y}" width="60" height="70" fill="#3a3040"/>'
body += '<line x1="120" y1="150" x2="680" y2="140" stroke="#5a5060" stroke-width="2"/>'
for i, c in enumerate(['#b84a4a', '#d8d0c0', '#4a6aa0', '#c9a74a', '#d8d0c0']):
    x = 200 + i * 90
    body += f'<rect x="{x}" y="146" width="30" height="40" fill="{c}" opacity=".8"/>'
body += '<rect x="260" y="60" width="280" height="390" fill="#0f0e14"/><circle cx="400" cy="250" r="140" fill="url(#luzfraca)" opacity=".5"/>'
body += person(330, 430, 1.4, '#3a2a22', dress=True)
body += '<line x1="342" y1="330" x2="392" y2="305" stroke="#3a2a22" stroke-width="7" stroke-linecap="round"/>'
body += person(450, 430, 1.45, '#1c2236', hat=False)
for x in [270, 520, 560, 240]:
    body += person(x, 440, 1.1, '#0a090d')
write('cap9-beco.svg', svg(body, 'Beco escuro; uma mulher aponta para um homem de terno cercado de curiosos'))

# ---------------- CAP10: céu com Cruzeiro e mancha negra
body = stars(170, 13, 330)
body += '<path d="M0,0 L800,0 L800,330 Q400,250 0,330Z" fill="#c9d4ff" opacity=".04"/>'
cruz = [(470, 70, 5), (470, 190, 6), (420, 128, 4.5), (520, 122, 4.5), (492, 152, 2.6)]
for cx, cy, r in cruz:
    body += f'<circle cx="{cx}" cy="{cy}" r="{r*3}" fill="#fff" opacity=".08"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>'
body += '<path d="M540,170 Q560,140 610,150 Q660,160 650,205 Q640,240 590,232 Q545,226 540,170Z" fill="#020309"/>'
body += '<text x="600" y="262" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" fill="#aab3d8">a mancha "como carvão"</text>'
body += '<rect x="0" y="330" width="800" height="120" fill="#0b0f1a"/>' + tree(90, 360, 1.6, '#070b0a') + tree(720, 380, 1.5, '#070b0a')
body += '<rect x="250" y="300" width="300" height="150" fill="#1b2236"/>'
body += '<rect x="330" y="330" width="140" height="120" fill="#e6b85c" opacity=".25"/><rect x="330" y="330" width="140" height="120" fill="none" stroke="#0e1322" stroke-width="8"/>'
body += person(400, 452, 1.2, '#06080f', dress=True)
write('cap10-ceu.svg', svg(body, 'Céu estrelado com o Cruzeiro do Sul e uma mancha negra; Clara na janela', sky=('#04060e', '#141c38')))

# ---------------- CAP11: bonde
body = '<rect width="800" height="450" fill="#1a1e2a"/>'
body += '<rect x="0" y="40" width="800" height="200" fill="#2a3450"/>'
for i in range(5):
    x = 20 + i * 160
    body += f'<rect x="{x}" y="60" width="140" height="150" fill="#0f1424"/>'
    body += f'<rect x="{x}" y="60" width="140" height="150" fill="url(#ceu)" opacity=".9"/>'
    body += mountains(200, '#16203a', 20 + i, w=800).replace('points="0,450', f'clip="x" points="0,450') if False else ''
body += '<rect x="0" y="40" width="800" height="200" fill="none" stroke="#4a3a28" stroke-width="16"/>'
for i in range(1, 5):
    body += f'<rect x="{i*160}" y="40" width="20" height="200" fill="#4a3a28"/>'
body += '<rect x="0" y="240" width="800" height="210" fill="#2b2118"/>'
for i in range(6):
    body += f'<rect x="{20+i*135}" y="300" width="110" height="20" rx="4" fill="#5a4030"/>'
body += person(120, 430, 1.25, '#0d0f16', hat=True) + person(230, 430, 1.25, '#0d0f16') + person(690, 430, 1.25, '#0d0f16', hat=True)
body += person(420, 440, 1.45, '#c99a74', dress=True, hair='#1a110a')
body += person(520, 440, 1.6, '#3a3550', dress=True, hair='#c9a074')
body += '<path d="M380,180 q20,-30 80,-40" stroke="#f3d59a" stroke-width="2" fill="none" stroke-dasharray="3 6" opacity=".7"/>'
for x in [80, 260, 420, 600, 740]:
    body += f'<line x1="{x}" y1="20" x2="{x}" y2="44" stroke="#4a3a28" stroke-width="3"/><circle cx="{x}" cy="48" r="5" fill="#4a3a28"/>'
body += stars(30, 21, 200)
write('cap11-bonde.svg', svg(body, 'Interior de bonde; Clara olha pela janela ao lado de Dona Margarida'))

# ---------------- PERSONAGENS galeria
body = '<rect width="800" height="450" fill="#141826"/>' + '<rect x="0" y="360" width="800" height="90" fill="#0e1220"/>'
cast = [(80, dict(dress=True, hair='#1a110a'), 'Clara', '#c99a74'), (175, dict(hat=True), 'Joaquim', '#7a6a5a'),
        (270, dict(guitar=True), 'Cassi', '#e8c8a6'), (370, dict(cane=True), 'Marramaque', '#9a8a7a'),
        (470, dict(dress=True, hair='#c9a074'), 'D. Margarida', '#d8c0a0'), (570, dict(cane=True), 'Meneses', '#cfc6b4'),
        (670, dict(), 'L. Flores', '#9a7a5a'), (750, dict(dress=True), 'Salustiana', '#e0c8b0')]
for x, kw, nome, c in cast:
    body += f'<circle cx="{x}" cy="230" r="70" fill="url(#luzfraca)" opacity=".5"/>'
    body += person(x, 360, 1.5, '#06080f', **kw)
    body += f'<text x="{x}" y="395" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="{GOLD2}">{nome}</text>'
write('personagens.svg', svg(body, 'Galeria de silhuetas dos personagens principais'))

# ---------------- TEMAS balança
body = '<rect width="800" height="450" fill="#151827"/>' + stars(40, 31, 120)
body += '<rect x="396" y="100" width="8" height="260" fill="#c9a74a"/><rect x="350" y="355" width="100" height="16" rx="6" fill="#c9a74a"/>'
body += '<g transform="rotate(-14 400 110)"><rect x="180" y="106" width="440" height="8" rx="4" fill="#c9a74a"/>'
body += '<line x1="200" y1="110" x2="170" y2="200" stroke="#c9a74a" stroke-width="2"/><line x1="200" y1="110" x2="230" y2="200" stroke="#c9a74a" stroke-width="2"/><path d="M160,200 Q200,230 240,200Z" fill="#c9a74a"/>'
body += '<line x1="600" y1="110" x2="570" y2="200" stroke="#c9a74a" stroke-width="2"/><line x1="600" y1="110" x2="630" y2="200" stroke="#c9a74a" stroke-width="2"/><path d="M560,200 Q600,230 640,200Z" fill="#c9a74a"/></g>'
# lado esquerdo (pesado: cartola+bengala) — fica embaixo à esquerda após rotação negativa? rotação -14 sobe a direita
body += '<g transform="translate(180,250)"><rect x="-22" y="-40" width="44" height="34" fill="#0b0c12"/><rect x="-34" y="-8" width="68" height="8" rx="3" fill="#0b0c12"/><line x1="40" y1="-60" x2="20" y2="0" stroke="#d6c8a0" stroke-width="4"/></g>'
body += person(620, 150, 0.9, '#c99a74', dress=True, hair='#1a110a')
body += '<text x="120" y="320" font-family="Georgia,serif" font-size="18" fill="#e9e4d8">"família", cor branca, dinheiro</text>'
body += '<text x="620" y="40" text-anchor="middle" font-family="Georgia,serif" font-size="18" fill="#e9e4d8">mulher, pobre, negra</text>'
write('temas.svg', svg(body, 'Balança desequilibrada entre privilégio e a moça pobre'))

# ---------------- favicon
write('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0d1018"/><circle cx="32" cy="14" r="3" fill="#fff"/><circle cx="32" cy="46" r="3.5" fill="#fff"/><circle cx="18" cy="30" r="2.6" fill="#fff"/><circle cx="46" cy="28" r="2.6" fill="#fff"/><ellipse cx="50" cy="48" rx="7" ry="5" fill="#000" stroke="#e6b85c" stroke-width="1"/></svg>')
print('ok', len(os.listdir(OUT)))
