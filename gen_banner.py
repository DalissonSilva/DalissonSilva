#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Banner animado do perfil GitHub — Dalisson Silva.
Saida: dark.svg / light.svg  (1180x610)

Duas camadas independentes no painel VISUAL.MAP:
  1. RETRATO   ~31k pontos (dither Floyd-Steinberg), em 94 bandas de deriva.
               Na virada cada banda desliza ~42% rumo ao centroide e some.
  2. VIAJANTES ~900 pontos que morfam entre 3 formas, casados por transporte
               otimo. Invisiveis durante a fase do retrato.
"""
import math, random, os
import numpy as np
from PIL import Image, ImageDraw
from scipy.optimize import linear_sum_assignment
import portrait as PORT

SEED = 20260828
random.seed(SEED); np.random.seed(SEED)

W, H = 1180, 610
N_TRAV = 900
S = 400
N_BANDS, N_SUB = 94, 14

# ------------------------------------------------------------ formas geometricas
def shape_database():
    img = Image.new("L", (S, S), 0); d = ImageDraw.Draw(img)
    x0, x1 = 62, 338
    d.ellipse([x0, 82, x1, 138], outline=255, width=12)
    d.line([x0 + 6, 110, x0 + 6, 292], fill=255, width=12)
    d.line([x1 - 6, 110, x1 - 6, 292], fill=255, width=12)
    d.arc([x0, 264, x1, 320], start=0, end=180, fill=255, width=12)
    for yy in (170, 232):
        d.arc([x0, yy - 28, x1, yy + 28], start=0, end=180, fill=255, width=9)
    return img

def shape_dag():
    img = Image.new("L", (S, S), 0); d = ImageDraw.Draw(img)
    nodes = {"a": (62, 200), "b": (162, 112), "c": (162, 288),
             "d": (262, 200), "e": (352, 116), "f": (352, 284)}
    R = 33
    for u, v in [("a","b"),("a","c"),("b","d"),("c","d"),("d","e"),("d","f")]:
        (x1, y1), (x2, y2) = nodes[u], nodes[v]
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        d.line([(x1 + ux*R, y1 + uy*R), (x2 - ux*R, y2 - uy*R)], fill=255, width=8)
    for (cx, cy) in nodes.values():
        d.ellipse([cx-26, cy-26, cx+26, cy+26], outline=255, width=11)
    return img

def shape_chart():
    img = Image.new("L", (S, S), 0); d = ImageDraw.Draw(img)
    base, bw, gap, x = 322, 26, 22, 66
    pts = []
    for h in [92, 138, 112, 186, 158, 236]:
        d.rectangle([x, base-h, x+bw, base], fill=255)
        pts.append((x + bw/2, base - h - 26)); x += bw + gap
    d.line([56, base+12, 348, base+12], fill=255, width=9)
    d.line(pts, fill=255, width=8, joint="curve")
    for (px, py) in pts:
        d.ellipse([px-9, py-9, px+9, py+9], fill=255)
    return img

SHAPES = [shape_database, shape_dag, shape_chart]
CAPTIONS = ["portrait.dither", "oracle.storage", "airflow.dag", "qlik.analytics"]

def grid_points(mask, step):
    ys, xs = np.nonzero(mask)
    keep = {}
    gx = (xs / step).astype(int); gy = (ys / step).astype(int)
    for i in range(len(xs)):
        k = (gx[i], gy[i])
        if k not in keep:
            keep[k] = (xs[i], ys[i])
    p = np.array(list(keep.values()), dtype=float)
    return p + np.random.normal(0, step * 0.16, p.shape)

def sample(img, target):
    a = np.array(img) > 110
    lo, hi, best = 1.4, 16.0, None
    for _ in range(40):
        step = (lo + hi) / 2
        pts = grid_points(a, step)
        if best is None or abs(len(pts) - target) < abs(len(best) - target):
            best = pts
        lo, hi = (step, hi) if len(pts) > target else (lo, step)
    pts = best
    if len(pts) > target:
        pts = pts[np.random.choice(len(pts), target, replace=False)]
    elif len(pts) < target:
        k = target - len(pts)
        pts = np.vstack([pts, pts[np.random.choice(len(pts), k, True)] + np.random.normal(0, 1.6, (k, 2))])
    return pts

def match(src, dst):
    cost = ((src[:, None, :] - dst[None, :, :]) ** 2).sum(-1)
    return dst[linear_sum_assignment(cost)[1]]

# --------------------------------------------------------------- geometria
PAD = 20
WIN = (PAD, PAD, W - 2*PAD, H - 2*PAD)
BAR_H = 40
BODY_Y = PAD + BAR_H
LP = (44, 84, 418, 482)
RP = (492, 84, 644, 482)

PW, PH = PORT.GW, PORT.GH
PX = LP[0] + (LP[2] - PW) / 2
PY = LP[1] + 38
CENTRE = np.array([PX + PW/2, PY + PH/2])

print("gerando retrato (dither Floyd-Steinberg)...")
DOTS_DARK, DOTS_LIGHT, MASK, BOX = PORT.portraits()
print(f"  recorte {BOX}  pontos dark={DOTS_DARK.sum()} light={DOTS_LIGHT.sum()}")

def runs_of(grid):
    out = []
    for y in range(grid.shape[0]):
        row = grid[y]; x = 0
        while x < len(row):
            if row[x]:
                x0 = x
                while x < len(row) and row[x]:
                    x += 1
                out.append((x0, y, x - x0))
            else:
                x += 1
    return out

def bands_for(runs):
    """94 bandas. Ruido per-ponto (sigma 4) ANTES de agrupar: sem isso, quantizar
    uma funcao linear da posicao recria matematicamente uma grade quadrada."""
    pos = np.array([[PX + r[0] + r[2]/2, PY + r[1]] for r in runs])
    noisy = pos + np.random.normal(0, 4.0, pos.shape)
    drift = (CENTRE - noisy) * 0.42
    u = 0.62 * noisy[:, 0] + 0.78 * noisy[:, 1]
    edges = np.quantile(u, np.linspace(0, 1, N_BANDS + 1))
    idx = np.clip(np.searchsorted(edges, u, 'right') - 1, 0, N_BANDS - 1)
    reps = np.zeros((N_BANDS, 2))
    for b in range(N_BANDS):
        m = idx == b
        reps[b] = drift[m].mean(0) if m.any() else 0
    return idx, reps, pos

def blockiness(pos, idx, tile=8):
    tx = ((pos[:, 0] - PX) // tile).astype(int)
    ty = ((pos[:, 1] - PY) // tile).astype(int)
    d = {}
    for i in range(len(pos)):
        d.setdefault((tx[i], ty[i]), set()).add(idx[i])
    return sum(1 for v in d.values() if len(v) == 1) / max(len(d), 1)

print("casando trajetorias dos viajantes (transporte otimo)...")
clouds = [sample(f(), N_TRAV) for f in SHAPES]
chain = [clouds[0]]
for k in range(1, len(clouds)):
    chain.append(match(chain[-1], clouds[k]))

def fit(cloud, box=300.0):
    mn, mx = cloud.min(0), cloud.max(0)
    sc = min(box / max(mx[0]-mn[0], 1e-6), box / max(mx[1]-mn[1], 1e-6))
    return (cloud - (mn + mx) / 2) * sc + CENTRE

TRAV = [fit(c) for c in chain]
COLLAPSE = CENTRE + (TRAV[0] - CENTRE) * 0.12

T = [0.0, 3.4, 4.7, 6.7, 8.0, 10.0, 11.3, 13.3, 14.6]
CYCLE = T[-1]
KT = ";".join(f"{t/CYCLE:.4f}" for t in T)
STAGE = [0, 0, 1, 1, 2, 2, 3, 3, 0]

ROWS = [
    ("Subject",       "Dálisson Silva"),
    ("Role",          "Engenheiro de Dados"),
    ("Origin",        "Maceió, Alagoas — BR"),
    ("Company",       "Unimed Maceió"),
    ("Domain",        "Saúde Suplementar & Hospitalar"),
    ("Status",        "Full-Cycle Data Professional"),
    ("ToolChain",     "VS Code . Git . Linux . Airflow"),
    ("Core.Lang",     "Python . SQL . PL/SQL . Shell"),
    ("Core.Data",     "Oracle . Autonomous DB . Tasy"),
    ("Core.Pipeline", "Airflow . ETL . Parquet . Cron"),
    ("Core.Arch",     "Medallion . Bronze/Silver/Gold"),
    ("Core.BI",       "Qlik Sense . Power BI . Streamlit"),
    ("Core.Cloud",    "OCI . GCP . Databricks"),
    ("Core.Gov",      "Linhagem . LGPD . Data Owners"),
    ("Grid.Mail",     "dalissonmuniz@outlook.com"),
    ("Grid.Portfolio","DalissonSilva.github.io"),
    ("Grid.LinkedIn", "in/dalisson-silva"),
    ("Grid.GitHub",   "DalissonSilva"),
]

PALETTES = {
    "dark": dict(page="#0A0A0F", win="#0C0C13", bar="#12121B", edge="#1E293B",
                 panel="#0B0B12", dot="#A78BFA", chrome="#00E5FF", val="#CBD5E1",
                 lead="#2A3444", accent="#10B981", live="#F43F5E", dim="#475569",
                 pill="#7C3AED", pilltxt="#F8FAFC", lattice="#141B27", trav="#00E5FF"),
    "light": dict(page="#F1F5F9", win="#FFFFFF", bar="#F8FAFC", edge="#D8E0EA",
                  panel="#FBFCFE", dot="#4C1D95", chrome="#0891B2", val="#334155",
                  lead="#CBD5E1", accent="#059669", live="#E11D48", dim="#94A3B8",
                  pill="#7C3AED", pilltxt="#FFFFFF", lattice="#E8EEF6", trav="#0891B2"),
}
MONO = "ui-monospace,SFMono-Regular,'DejaVu Sans Mono',Menlo,Consolas,monospace"
esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build(theme, grid):
    P = PALETTES[theme]
    runs = runs_of(grid)
    idx, reps, pos = bands_for(runs)
    o = []; a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'role="img" aria-label="Dálisson Silva — Engenheiro de Dados">')
    a(f'<defs><pattern id="lat" width="7" height="7" patternUnits="userSpaceOnUse">'
      f'<rect width="1" height="1" fill="{P["lattice"]}"/></pattern>'
      f'<clipPath id="vp"><rect x="{LP[0]}" y="{LP[1]}" width="{LP[2]}" height="{LP[3]}" rx="8"/></clipPath>'
      f'</defs>')

    a(f'<rect width="{W}" height="{H}" fill="{P["page"]}"/>')
    a(f'<rect x="{WIN[0]}" y="{WIN[1]}" width="{WIN[2]}" height="{WIN[3]}" rx="12" '
      f'fill="{P["win"]}" stroke="{P["edge"]}" stroke-width="1"/>')
    a(f'<path d="M{PAD+12} {PAD} h{WIN[2]-24} a12 12 0 0 1 12 12 v{BAR_H-12} h{-WIN[2]} '
      f'v{-(BAR_H-12)} a12 12 0 0 1 12 -12 z" fill="{P["bar"]}"/>')
    a(f'<line x1="{PAD}" y1="{BODY_Y}" x2="{PAD+WIN[2]}" y2="{BODY_Y}" stroke="{P["edge"]}" stroke-width="1"/>')
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        a(f'<circle cx="{PAD+22+i*20}" cy="{PAD+BAR_H/2}" r="6" fill="{c}"/>')
    a(f'<text x="{W/2}" y="{PAD+BAR_H/2+4.5}" font-family="{MONO}" font-size="13" '
      f'fill="{P["dim"]}" text-anchor="middle">profile.sh --live</text>')

    a(f'<rect x="{LP[0]}" y="{LP[1]}" width="{LP[2]}" height="{LP[3]}" rx="8" fill="{P["panel"]}" '
      f'stroke="{P["edge"]}" stroke-width="1"/>')
    a(f'<rect x="{LP[0]}" y="{LP[1]}" width="{LP[2]}" height="{LP[3]}" rx="8" fill="url(#lat)" opacity="0.85"/>')
    for (cx, cy, sx, sy) in [(LP[0],LP[1],1,1),(LP[0]+LP[2],LP[1],-1,1),
                             (LP[0],LP[1]+LP[3],1,-1),(LP[0]+LP[2],LP[1]+LP[3],-1,-1)]:
        a(f'<path d="M{cx+sx*2} {cy+sy*20} V{cy+sy*10} A8 8 0 0 1 {cx+sx*10} {cy+sy*2} H{cx+sx*20}" '
          f'fill="none" stroke="{P["chrome"]}" stroke-width="2" opacity="0.75"/>')
    a(f'<text x="{LP[0]+14}" y="{LP[1]+20}" font-family="{MONO}" font-size="11" '
      f'letter-spacing="1.6" fill="{P["chrome"]}">VISUAL.MAP</text>')

    a('<g clip-path="url(#vp)">')

    op_p = "1;1;0;0;0;0;0;0;1"
    delays = np.random.permutation(N_BANDS * N_SUB) / (N_BANDS * N_SUB) * 1.95
    by_band = [[] for _ in range(N_BANDS)]
    for i, r in enumerate(runs):
        by_band[idx[i]].append(r)
    for b in range(N_BANDS):
        if not by_band[b]:
            continue
        dx, dy = reps[b]
        tv = ";".join(["0,0", "0,0"] + [f"{dx:.1f},{dy:.1f}"] * 6 + ["0,0"])
        a(f'<g><animateTransform attributeName="transform" type="translate" values="{tv}" '
          f'keyTimes="{KT}" dur="{CYCLE}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="{op_p}" keyTimes="{KT}" '
          f'dur="{CYCLE}s" repeatCount="indefinite"/>')
        subs = [[] for _ in range(N_SUB)]
        for r in by_band[b]:
            subs[random.randrange(N_SUB)].append(r)
        for k, sub in enumerate(subs):
            if not sub:
                continue
            d = "".join(f"M{PX+x:.0f} {PY+y+0.5:.1f}h{L}" for (x, y, L) in sub)
            a(f'<path d="{d}" stroke="{P["dot"]}" stroke-width="0.95" fill="none" '
              f'shape-rendering="crispEdges" opacity="0">'
              f'<animate attributeName="opacity" values="0;1" dur="0.8s" '
              f'begin="{delays[b*N_SUB+k]:.2f}s" fill="freeze"/></path>')
        a('</g>')

    op_t = "0;0;1;1;1;1;1;1;0"
    for i in range(N_TRAV):
        seq = [COLLAPSE[i], COLLAPSE[i], TRAV[0][i], TRAV[0][i], TRAV[1][i],
               TRAV[1][i], TRAV[2][i], TRAV[2][i], COLLAPSE[i]]
        x0, y0 = seq[0]
        v = ";".join(f"{p[0]-x0:.1f},{p[1]-y0:.1f}" for p in seq)
        a(f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="1.8" fill="{P["trav"]}" opacity="0">'
          f'<animateTransform attributeName="transform" type="translate" values="{v}" '
          f'keyTimes="{KT}" dur="{CYCLE}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="{op_t}" keyTimes="{KT}" '
          f'dur="{CYCLE}s" repeatCount="indefinite"/></circle>')
    a('</g>')

    cy = LP[1] + LP[3] - 42
    a(f'<line x1="{LP[0]+14}" y1="{cy-20}" x2="{LP[0]+LP[2]-14}" y2="{cy-20}" stroke="{P["edge"]}" stroke-width="1"/>')
    for k, cap in enumerate(CAPTIONS):
        vis = ";".join("1" if STAGE[j] == k else "0" for j in range(9))
        a(f'<text x="{LP[0]+LP[2]/2}" y="{cy}" font-family="{MONO}" font-size="12.5" '
          f'fill="{P["accent"]}" text-anchor="middle" opacity="0">'
          f'<animate attributeName="opacity" values="{vis}" keyTimes="{KT}" dur="{CYCLE}s" '
          f'repeatCount="indefinite"/>{cap}</text>')
    for k in range(4):
        px = LP[0] + LP[2]/2 - 27 + k*18
        vis = ";".join("1" if STAGE[j] == k else "0.22" for j in range(9))
        a(f'<rect x="{px}" y="{cy+14}" width="10" height="3" rx="1.5" fill="{P["chrome"]}" opacity="0.22">'
          f'<animate attributeName="opacity" values="{vis}" keyTimes="{KT}" dur="{CYCLE}s" '
          f'repeatCount="indefinite"/></rect>')

    a(f'<text x="{RP[0]}" y="{RP[1]+16}" font-family="{MONO}" font-size="13" '
      f'letter-spacing="1.6" fill="{P["chrome"]}">SYSTEM.INFO</text>')
    bx = RP[0] + RP[2] - 62
    a(f'<rect x="{bx}" y="{RP[1]+3}" width="62" height="18" rx="9" fill="none" stroke="{P["live"]}" stroke-width="1"/>')
    a(f'<circle cx="{bx+13}" cy="{RP[1]+12}" r="3.4" fill="{P["live"]}">'
      f'<animate attributeName="opacity" values="1;0.15;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    a(f'<text x="{bx+24}" y="{RP[1]+16}" font-family="{MONO}" font-size="10.5" '
      f'letter-spacing="1.2" fill="{P["live"]}">LIVE</text>')
    a(f'<line x1="{RP[0]}" y1="{RP[1]+30}" x2="{RP[0]+RP[2]}" y2="{RP[1]+30}" stroke="{P["edge"]}" stroke-width="1"/>')

    FS, CW, SP = 13.5, 8.1, 21.5
    y0 = RP[1] + 52
    x_l, x_r = RP[0], RP[0] + RP[2]
    for i, (label, value) in enumerate(ROWS):
        y = y0 + i*SP
        lw, vw = len(label)*CW, len(value)*CW
        a(f'<text x="{x_l}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{P["chrome"]}" '
          f'textLength="{lw:.1f}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text>')
        a(f'<text x="{x_r-vw:.1f}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{P["val"]}" '
          f'textLength="{vw:.1f}" lengthAdjust="spacingAndGlyphs">{esc(value)}</text>')
        gs, ge = x_l + lw + 8, x_r - vw - 8
        n = int((ge - gs) / 6)
        if n > 0:
            step = (ge - gs) / n
            d = "".join(f"M{gs+j*step:.1f} {y-4}h1.6" for j in range(n+1))
            a(f'<path d="{d}" stroke="{P["lead"]}" stroke-width="1.6" stroke-linecap="round" shape-rendering="crispEdges"/>')

    py = RP[1] + RP[3] - 32
    handle = "@DalissonSilva"
    pw = len(handle)*8.4 + 34
    a(f'<rect x="{RP[0]}" y="{py}" width="{pw:.1f}" height="30" rx="15" fill="{P["pill"]}"/>')
    a(f'<circle cx="{RP[0]+17}" cy="{py+15}" r="4" fill="{P["pilltxt"]}"/>')
    a(f'<text x="{RP[0]+28}" y="{py+20}" font-family="{MONO}" font-size="14" fill="{P["pilltxt"]}">{handle}</text>')
    a(f'<text x="{RP[0]+RP[2]}" y="{py+20}" font-family="{MONO}" font-size="12" fill="{P["dim"]}" '
      f'text-anchor="end">bronze -&gt; silver -&gt; gold</text>')
    a('</svg>')
    return "\n".join(o), (pos, idx)


os.makedirs("/mnt/user-data/outputs", exist_ok=True)
for theme, name, grid in (("dark", "dark.svg", DOTS_DARK), ("light", "light.svg", DOTS_LIGHT)):
    svg, (pos, idx) = build(theme, grid)
    open(f"/mnt/user-data/outputs/{name}", "w", encoding="utf-8").write(svg)
    print(f"{name:10s} {len(svg)/1024:7.1f} KB   corridas={len(pos):6d}   "
          f"blocagem={blockiness(pos, idx):.3f} (organico<0.20 / grade>0.60)")
