#!/usr/bin/env python3
"""Membuat semua aset gambar (SVG vektor = tajam di resolusi berapa pun, termasuk 4K/Retina).
Jalankan: python3 tools/generate_assets.py"""
import random, math, os
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "images")

def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'preserveAspectRatio="xMidYMid slice"><defs>{DEFS}{defs}</defs>{body}</svg>')

DEFS = '''
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a3418"/><stop offset="1" stop-color="#2b170b"/></linearGradient>
<linearGradient id="wood2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7a4a24"/><stop offset="1" stop-color="#3d2210"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#ffb347" stop-opacity=".55"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>
<radialGradient id="broth" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#ffe27a"/><stop offset=".6" stop-color="#f2b81c"/><stop offset="1" stop-color="#c98a0a"/></radialGradient>
<linearGradient id="ceramic" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fffaf0"/><stop offset="1" stop-color="#d9c9a8"/></linearGradient>
<linearGradient id="tea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9831f"/><stop offset="1" stop-color="#8a3f0a"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="blur2"><feGaussianBlur stdDeviation="40"/></filter>
<filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="18"/></filter>
'''

def planks(w, h, seed=1, tone="wood"):
    r = random.Random(seed); s = ""; n = 7; ph = h / n
    for i in range(n):
        s += f'<rect x="0" y="{i*ph:.0f}" width="{w}" height="{ph+2:.0f}" fill="url(#{tone})" opacity="{0.8+r.random()*.2:.2f}"/>'
        s += f'<rect x="0" y="{i*ph:.0f}" width="{w}" height="3" fill="#000" opacity=".45"/>'
        for _ in range(9):
            y = i*ph + r.random()*ph; x = r.random()*w; l = 200 + r.random()*600
            s += f'<path d="M{x:.0f} {y:.0f} q{l/2:.0f} {r.uniform(-10,10):.0f} {l:.0f} {r.uniform(-6,6):.0f}" stroke="#1c0f07" stroke-opacity=".35" stroke-width="{r.uniform(1,3):.1f}" fill="none"/>'
    return s

def bokeh(w, h, seed=2, n=18, y0=0, y1=.5):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.random()*w:.0f}" cy="{(y0+r.random()*(y1-y0))*h:.0f}" r="{r.uniform(18,70):.0f}" fill="#ffc861" opacity="{r.uniform(.12,.4):.2f}" filter="url(#blur)"/>' for _ in range(n))

def steam(cx, cy, s=1):
    return "".join(f'<path d="M{cx+dx*s} {cy} c{-30*s} {-50*s} {30*s} {-90*s} 0 {-150*s} c{-25*s} {-40*s} {25*s} {-70*s} 0 {-110*s}" stroke="#fff" stroke-opacity=".22" stroke-width="{16*s}" stroke-linecap="round" fill="none" filter="url(#blur)"/>' for dx in (-70, 0, 70))

def bowl(cx, cy, R, seed=3):
    r = random.Random(seed); H = R*.62
    b = f'<ellipse cx="{cx}" cy="{cy+H*.95}" rx="{R*1.05}" ry="{R*.2}" fill="#000" opacity=".55" filter="url(#shadow)"/>'
    b += f'<ellipse cx="{cx}" cy="{cy+H*.78}" rx="{R*.38}" ry="{R*.07}" fill="#a88f64"/>'
    b += f'<path d="M{cx-R} {cy} Q{cx-R*.95} {cy+H*1.05} {cx} {cy+H*.95} Q{cx+R*.95} {cy+H*1.05} {cx+R} {cy} Z" fill="url(#ceramic)"/>'
    b += f'<path d="M{cx-R*.9} {cy+H*.38} Q{cx} {cy+H*.62} {cx+R*.9} {cy+H*.38}" stroke="#b8231c" stroke-width="{R*.045}" fill="none" opacity=".85"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="{R*.3}" fill="#f5ead2" stroke="#c9b48a" stroke-width="3"/>'
    b += f'<ellipse cx="{cx}" cy="{cy+R*.01}" rx="{R*.92}" ry="{R*.255}" fill="url(#broth)"/>'
    for _ in range(26):  # suwiran ayam
        a = r.random()*6.28; d = r.random()*.7
        x = cx+math.cos(a)*R*.8*d; y = cy+math.sin(a)*R*.2*d
        b += f'<path d="M{x:.0f} {y:.0f} q{R*.08:.0f} {-R*.04:.0f} {R*.17:.0f} {r.uniform(-8,8):.0f}" stroke="#f3dca5" stroke-width="{R*.035:.0f}" stroke-linecap="round" fill="none"/>'
    for ex in (-.3, .22):  # telur
        b += f'<ellipse cx="{cx+R*ex}" cy="{cy-R*.02}" rx="{R*.15}" ry="{R*.075}" fill="#fff8e6"/><ellipse cx="{cx+R*ex}" cy="{cy-R*.02}" rx="{R*.06}" ry="{R*.03}" fill="#f2a900"/>'
    for _ in range(40):  # bawang goreng & seledri
        a = r.random()*6.28; d = r.random()
        x = cx+math.cos(a)*R*.85*d; y = cy+math.sin(a)*R*.22*d
        col = r.choice(["#8a4a12", "#b9701c", "#3f9a45", "#2c7a38"])
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R*r.uniform(.012,.03):.1f}" fill="{col}"/>'
    b += f'<ellipse cx="{cx-R*.35}" cy="{cy-R*.06}" rx="{R*.2}" ry="{R*.03}" fill="#fff" opacity=".35"/>'
    return b + steam(cx, cy-R*.15, R/330)

def sate(x, y, L, ang=-12, col="#6a3411", n=5):
    c = f'<g transform="translate({x} {y}) rotate({ang})"><rect x="0" y="-4" width="{L}" height="8" rx="4" fill="#d8b36a"/>'
    for i in range(n):
        c += f'<rect x="{L*.1+i*L*.14:.0f}" y="-{L*.045:.0f}" width="{L*.12:.0f}" height="{L*.09:.0f}" rx="{L*.03:.0f}" fill="{col}"/><rect x="{L*.1+i*L*.14+6:.0f}" y="-{L*.035:.0f}" width="{L*.05:.0f}" height="{L*.02:.0f}" rx="4" fill="#fff" opacity=".18"/>'
    return c + '</g>'

def tempe(x, y, s):
    c = ""
    for i in range(3):
        c += f'<g transform="translate({x+i*s*.55:.0f} {y-i*s*.12:.0f}) rotate({-6+i*7})"><rect width="{s}" height="{s*.55}" rx="{s*.08}" fill="#e0a02b"/><rect y="{s*.06}" width="{s}" height="{s*.2}" rx="{s*.08}" fill="#fff" opacity=".18"/><circle cx="{s*.3}" cy="{s*.3}" r="{s*.03}" fill="#8a5a10"/><circle cx="{s*.65}" cy="{s*.2}" r="{s*.03}" fill="#8a5a10"/></g>'
    return c

def glass(x, y, w):
    h = w*1.7
    return (f'<ellipse cx="{x+w/2}" cy="{y+h}" rx="{w*.55}" ry="{w*.1}" fill="#000" opacity=".5" filter="url(#shadow)"/>'
            f'<path d="M{x} {y} L{x+w} {y} L{x+w*.86} {y+h} L{x+w*.14} {y+h} Z" fill="url(#tea)" opacity=".92"/>'
            + "".join(f'<rect x="{x+w*(.15+.3*i)}" y="{y+h*(.1+.18*(i%2))}" width="{w*.26}" height="{w*.26}" rx="8" fill="#fff" opacity=".45" transform="rotate({i*14} {x+w/2} {y+h/2})"/>' for i in range(3))
            + f'<path d="M{x+w*.12} {y+6} L{x+w*.2} {y+h-8}" stroke="#fff" stroke-opacity=".5" stroke-width="{w*.05}" stroke-linecap="round"/>'
            f'<path d="M{x+w*.6} {y+h*.1} L{x+w*.95} {y-h*.28}" stroke="#d9302a" stroke-width="{w*.06}" stroke-linecap="round"/>'
            f'<ellipse cx="{x+w/2}" cy="{y}" rx="{w/2}" ry="{w*.08}" fill="#f0a64a" stroke="#fff" stroke-opacity=".6" stroke-width="3"/>')

def scene(w, h, items, seed=1, light=(.5, .35), dark=1.0):
    return svg(w, h, planks(w, h, seed) + f'<rect width="{w}" height="{h}" fill="url(#glow)" transform="translate({(light[0]-.5)*w*.6} 0)"/>'
               + bokeh(w, h, seed+9, 16, 0, .45) + items + f'<rect width="{w}" height="{h}" fill="url(#vig)" opacity="{dark}"/>')

def storefront(w, h, name, seed):
    r = random.Random(seed)
    s = f'<rect width="{w}" height="{h}" fill="#2a1a10"/><rect width="{w}" height="{h*.55}" fill="#1f2c3d"/>'
    s += "".join(f'<rect x="{r.randint(0,w-200)}" y="{r.randint(0,int(h*.3))}" width="{r.randint(120,260)}" height="{r.randint(200,400)}" fill="#2b3d52" opacity=".6"/>' for _ in range(6))
    s += f'<rect x="{w*.08}" y="{h*.22}" width="{w*.84}" height="{h*.62}" fill="#f2e0bd"/>'
    s += f'<rect x="{w*.08}" y="{h*.22}" width="{w*.84}" height="{h*.16}" fill="#b8231c"/>'
    s += f'<text x="{w/2}" y="{h*.335}" text-anchor="middle" font-family="Georgia,serif" font-weight="bold" font-style="italic" font-size="{w*.075}" fill="#ffd34d">{name}</text>'
    for i in range(12):
        s += f'<path d="M{w*.08+i*w*.07} {h*.38} h{w*.07} v{h*.04} q-{w*.035} {h*.05} -{w*.07} 0 z" fill="{"#f7b500" if i%2 else "#fff"}"/>'
    s += f'<rect x="{w*.14}" y="{h*.52}" width="{w*.72}" height="{h*.32}" fill="url(#wood2)"/><rect x="{w*.14}" y="{h*.5}" width="{w*.72}" height="{h*.03}" fill="#8b5a2b"/>'
    s += "".join(f'<ellipse cx="{w*(.25+.17*i)}" cy="{h*.62}" rx="{w*.055}" ry="{h*.02}" fill="#f5ead2"/><ellipse cx="{w*(.25+.17*i)}" cy="{h*.617}" rx="{w*.048}" ry="{h*.015}" fill="url(#broth)"/>' for i in range(4))
    s += f'<rect x="0" y="{h*.84}" width="{w}" height="{h*.16}" fill="#3b3b3b"/><rect x="0" y="{h*.84}" width="{w}" height="6" fill="#555"/>'
    s += bokeh(w, h, seed, 14, .1, .5) + f'<rect width="{w}" height="{h}" fill="url(#vig)" opacity=".5"/>'
    return svg(w, h, s)

def vintage(w, h):
    body = ('<g filter="url(#sepia)">' + planks(w, h, 5, "wood2") + f'<rect width="{w}" height="{h}" fill="url(#glow)"/>'
            + bowl(w*.5, h*.55, w*.3, 8) + sate(w*.12, h*.82, w*.28, -6) + '</g>'
            + f'<rect width="{w}" height="{h}" fill="url(#vig)"/><rect width="{w}" height="{h}" fill="#d8b98a" opacity=".22"/>')
    return svg(w, h, body, '<filter id="sepia"><feColorMatrix type="matrix" values=".4 .5 .1 0 0 .35 .45 .1 0 0 .25 .35 .08 0 0 0 0 0 1 0"/></filter>')

W, H = 2400, 1600
files = {}
# HERO: mangkuk besar + sate + es teh (sisi kanan, teks di kiri)
files["hero.svg"] = scene(2400, 1600, bowl(1500, 760, 560, 1) + sate(1330, 1330, 560, -6) + sate(1280, 1450, 560, -3, "#4a2208", 4) + glass(2000, 330, 170) + tempe(760, 1300, 230), 1, (.7, .4), .8)
files["tentang-1.svg"] = vintage(1600, 1200)
files["tentang-2.svg"] = scene(1600, 1200, bowl(800, 560, 420, 4) + glass(1230, 600, 150) + tempe(180, 960, 190), 2)
files["mengapa-bowl.svg"] = scene(1400, 1400, bowl(700, 640, 560, 6), 3, dark=.7)
files["menu-soto-ayam.svg"] = scene(1200, 1140, bowl(600, 520, 470, 11), 11, dark=.7)
files["menu-sate-ayam.svg"] = scene(1200, 1140, sate(130, 420, 940, -9) + sate(150, 620, 940, -4) + sate(110, 820, 940, 3), 12, dark=.7)
files["menu-sate-kerang.svg"] = scene(1200, 1140, sate(130, 430, 940, -8, "#3a1a08", 6) + sate(150, 640, 940, -3, "#4a2208", 6) + sate(110, 850, 940, 4, "#3a1a08", 6), 13, dark=.7)
files["menu-tempe.svg"] = scene(1200, 1140, tempe(70, 640, 480), 14, dark=.7)
files["menu-es-teh.svg"] = scene(1200, 1140, glass(430, 250, 340), 15, dark=.7)
files["lokasi-banyumanik.svg"] = storefront(1400, 1000, "Mas Boed", 21)
files["lokasi-semarang-barat.svg"] = storefront(1400, 1000, "Soto Mas Boed", 22)
files["galeri-1.svg"] = scene(1600, 1400, bowl(800, 640, 600, 31) + glass(1250, 760, 150), 31)
files["galeri-2.svg"] = scene(1600, 1400, sate(160, 520, 1200, -6) + sate(200, 760, 1200, 2) + tempe(300, 1100, 300), 32)
files["galeri-3.svg"] = scene(1600, 1400, bowl(560, 640, 440, 33) + bowl(1100, 860, 400, 34), 33)
files["galeri-4.svg"] = scene(1600, 1400, glass(640, 300, 300) + tempe(240, 1000, 280), 34)
files["galeri-5.svg"] = scene(1600, 1400, bowl(800, 560, 520, 35) + sate(260, 1130, 1000, -4, "#4a2208", 5), 35)
files["cta-bg.svg"] = scene(2400, 1200, bowl(1650, 560, 480, 41) + sate(1500, 1030, 640, -8) + glass(2100, 330, 150), 41, (.75, .4), .9)

os.makedirs(OUT, exist_ok=True)
for n, c in files.items():
    open(os.path.join(OUT, n), "w", encoding="utf-8").write(c)
print(f"{len(files)} gambar dibuat di {os.path.abspath(OUT)}")
