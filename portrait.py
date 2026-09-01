#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline do retrato: recorte -> segmentacao -> dither Floyd-Steinberg 1-bit."""
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from scipy import ndimage as ndi

SRC = '/mnt/user-data/uploads/WhatsApp_Image_2026-08-28_at_21_37_23.jpeg'
GW, GH = 300, 340                      # grade do retrato


def segment(rgb):
    """Mascara do sujeito: distancia de cor ao fundo OU mais escuro que o fundo."""
    a = np.asarray(rgb, dtype=float)
    g = a.mean(2)
    bg = np.median(a[:40].reshape(-1, 3), 0)
    dist = np.linalg.norm(a - bg, axis=2)
    raw = (dist > 48) | (g < bg.mean() - 6)
    raw = ndi.binary_opening(raw, np.ones((3, 3)))
    lab, _ = ndi.label(~raw)                       # fundo = componentes que tocam a borda
    edge = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])
    edge.discard(0)
    subj = ~np.isin(lab, list(edge))
    subj = ndi.binary_closing(subj, np.ones((9, 9)))
    subj = ndi.binary_fill_holes(subj)
    lab2, n = ndi.label(subj)
    if n > 1:                                       # mantem o maior componente
        subj = lab2 == (1 + np.argmax(np.bincount(lab2.ravel())[1:]))
    return subj


def crop_box(subj, aspect=GW / GH):
    """Recorte cabeca+ombros na proporcao da grade, centrado no sujeito."""
    ys, xs = np.nonzero(subj)
    x0, x1 = xs.min(), xs.max()
    top = ys.min()
    H, W = subj.shape
    cx = (x0 + x1) / 2
    h = H - max(0, top - int(0.06 * H))             # do topo da cabeca ate a base
    y0 = H - h
    w = h * aspect
    if w > W:
        w = W
        h = w / aspect
        y0 = min(y0, H - h)
    l = int(np.clip(cx - w / 2, 0, W - w))
    return (l, int(y0), int(l + w), int(y0 + h))


def prepare():
    im = Image.open(SRC).convert('RGB')
    subj = segment(im)
    box = crop_box(subj)
    im_c = im.crop(box).resize((GW, GH), Image.LANCZOS)
    m_c = Image.fromarray((subj * 255).astype('uint8')).crop(box).resize((GW, GH), Image.LANCZOS)
    mask = np.asarray(m_c) > 140

    g = ImageOps.grayscale(im_c)
    g = ImageOps.autocontrast(g, cutoff=1)
    g = g.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    g = ImageEnhance.Contrast(g).enhance(1.3)       # 1.3x apenas - 2.4x fica caveira
    return np.asarray(g, dtype=float), mask, box


def dither(density, mask):
    """Floyd-Steinberg 1-bit, varredura serpentina. Retorna grade booleana de pontos."""
    v = density.astype(float).copy()
    v[~mask] = 0.0
    H, W = v.shape
    on = np.zeros((H, W), bool)
    for y in range(H):
        rng = range(W) if y % 2 == 0 else range(W - 1, -1, -1)
        nxt = 1 if y % 2 == 0 else -1
        for x in rng:
            old = v[y, x]
            new = 255.0 if old > 127.5 else 0.0
            on[y, x] = new > 0
            err = old - new
            if 0 <= x + nxt < W:
                v[y, x + nxt] += err * 7 / 16
            if y + 1 < H:
                if 0 <= x - nxt < W:
                    v[y + 1, x - nxt] += err * 3 / 16
                v[y + 1, x] += err * 5 / 16
                if 0 <= x + nxt < W:
                    v[y + 1, x + nxt] += err * 1 / 16
    hard = ndi.binary_erosion(mask, np.ones((3, 3)))   # limpa o sangramento na borda
    return on & hard


def rolloff(v, knee=190.0, slope=0.42):
    """Comprime os altos: evita que a camisa branca vire um bloco 100% solido."""
    return np.where(v > knee, knee + (v - knee) * slope, v)


def bottom_fade(v, rows=58, gamma=1.4):
    """Rarefaz os pontos nas ultimas linhas: dissolve a base da camisa no painel
    sem depender de <mask>, que nem todo renderizador aplica."""
    v = v.copy()
    H = v.shape[0]
    y = np.arange(rows)
    ramp = 1.0 - (y / rows) ** gamma
    v[H - rows:] *= ramp[:, None]
    return v


def portraits():
    """dark: pontos nas areas iluminadas. light: pontos nas areas escuras."""
    gray, mask, box = prepare()
    dark = dither(bottom_fade(rolloff(gray)), mask)
    light = dither(bottom_fade(rolloff(255.0 - gray)), mask)
    return dark, light, mask, box


if __name__ == '__main__':
    d, l, m, box = portraits()
    print('recorte', box, ' sujeito', f'{m.mean()*100:.1f}%')
    print('pontos dark ', d.sum(), '  light', l.sum())
    for name, arr, bg, fg in (('pv_dark.png', d, 10, 200), ('pv_light.png', l, 250, 40)):
        img = np.full(arr.shape, bg, 'uint8')
        img[arr] = fg
        Image.fromarray(img).resize((GW * 2, GH * 2), Image.NEAREST).save(name)
    def runs(a):
        n = 0
        for row in a:
            n += int(np.sum(row[1:] & ~row[:-1])) + int(row[0])
        return n
    print('runs dark', runs(d), ' light', runs(l))
    np.save('portrait_dark.npy', d)
    np.save('portrait_light.npy', l)
