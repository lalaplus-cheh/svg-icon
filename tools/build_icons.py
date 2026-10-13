#!/usr/bin/env python3
"""Generate the SVG icon set for the CP3 web UI (video / audio / light).

Usage:  python3 tools/build_icons.py [output-root]

Every icon is drawn on a 64x64 grid with a 3.5 stroke and round caps/joins.
The viewBox carries 8 units of padding (-8 -8 80 80) so the artwork sits at
the same visual size as the original 160x160 PNGs. Icons are white by default
(color="#fff" + currentColor) so they work as a drop-in <img> replacement; when
inlined, override with CSS `color`.

Also writes preview.html (originals vs. new icons) into the output root.
"""
import math
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = 'fill="currentColor" stroke="none"'


def n(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def svg(*els):
    body = '\n'.join('  ' + e for e in els if e)
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" viewBox="-8 -8 80 80" '
            'color="#fff" fill="none" stroke="currentColor" stroke-width="3.5" '
            'stroke-linecap="round" stroke-linejoin="round">\n' + body + '\n</svg>\n')


def P(d, extra=''):
    return f'<path d="{d}"{(" " + extra) if extra else ""}/>'


def C(cx, cy, r, extra=''):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}"{(" " + extra) if extra else ""}/>'


def R(x, y, w, h, rx=0, extra=''):
    a = f' rx="{n(rx)}"' if rx else ''
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"{a}{(" " + extra) if extra else ""}/>'


def G(transform, *els):
    inner = ''.join(els)
    return f'<g transform="{transform}">{inner}</g>'


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def arc(cx, cy, r, a0, a1):
    """Arc from math-angle a0 to a1 (degrees, y up). a1 > a0 => counter-clockwise on screen."""
    x0, y0 = pt(cx, cy, r, a0)
    x1, y1 = pt(cx, cy, r, a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 0 if a1 > a0 else 1
    return f'M{n(x0)} {n(y0)}A{n(r)} {n(r)} 0 {large} {sweep} {n(x1)} {n(y1)}'


# ---------------------------------------------------------------- stroke font
def glyph(ch, x, y, h):
    """Return (path, advance-width) for a single-stroke glyph with cap height h."""
    if ch == 'H':
        w = 0.72 * h
        return f'M{n(x)} {n(y)}v{n(h)}M{n(x + w)} {n(y)}v{n(h)}M{n(x)} {n(y + h / 2)}h{n(w)}', w
    if ch == 'D':
        r = h / 2
        a = 0.26 * h
        return f'M{n(x)} {n(y)}h{n(a)}a{n(r)} {n(r)} 0 0 1 0 {n(h)}H{n(x)}z', a + r
    if ch == 'M':
        w = 0.92 * h
        return f'M{n(x)} {n(y + h)}V{n(y)}l{n(w / 2)} {n(0.62 * h)}l{n(w / 2)} {n(-0.62 * h)}v{n(h)}', w
    if ch == 'I':
        return f'M{n(x)} {n(y)}v{n(h)}', 0
    if ch == 'V':
        w = 0.8 * h
        return f'M{n(x)} {n(y)}l{n(w / 2)} {n(h)}l{n(w / 2)} {n(-h)}', w
    if ch == 'A':
        w = 0.8 * h
        t = 0.66
        return (f'M{n(x)} {n(y + h)}l{n(w / 2)} {n(-h)}l{n(w / 2)} {n(h)}'
                f'M{n(x + w / 2 * (1 - t))} {n(y + t * h)}H{n(x + w - w / 2 * (1 - t))}'), w
    if ch == 'G':
        rx, ry = 0.46 * h, 0.5 * h
        cx, cy = x + rx, y + ry
        x0, y0 = cx + rx * math.cos(math.radians(48)), cy - ry * math.sin(math.radians(48))
        return (f'M{n(x0)} {n(y0)}A{n(rx)} {n(ry)} 0 1 0 {n(cx + rx)} {n(cy)}H{n(cx + 0.1 * rx)}'), 2 * rx
    if ch == 'L':
        w = 0.56 * h
        return f'M{n(x)} {n(y)}V{n(y + h)}H{n(x + w)}', w
    if ch == 'E':
        w = 0.56 * h
        return (f'M{n(x + w)} {n(y)}H{n(x)}V{n(y + h)}H{n(x + w)}M{n(x)} {n(y + h / 2)}H{n(x + 0.85 * w)}'), w
    if ch == 'T':
        w = 0.76 * h
        return f'M{n(x)} {n(y)}h{n(w)}M{n(x + w / 2)} {n(y)}v{n(h)}', w
    if ch == '3':
        r = 0.3 * h
        cx, cy = x + 0.3 * h, y + 0.7 * h
        ex, ey = cx + r * math.cos(math.radians(210)), cy - r * math.sin(math.radians(210))
        return (f'M{n(x + 0.02 * h)} {n(y)}H{n(x + 0.58 * h)}L{n(cx)} {n(cy - r)}'
                f'A{n(r)} {n(r)} 0 1 1 {n(ex)} {n(ey)}'), 0.6 * h
    if ch == '5':
        r = 0.3 * h
        cx, cy = x + 0.3 * h, y + 0.7 * h
        sx, sy = cx + r * math.cos(math.radians(135)), cy - r * math.sin(math.radians(135))
        ex, ey = cx + r * math.cos(math.radians(210)), cy - r * math.sin(math.radians(210))
        return (f'M{n(x + 0.56 * h)} {n(y)}H{n(x + 0.06 * h)}L{n(sx)} {n(sy)}'
                f'A{n(r)} {n(r)} 0 1 1 {n(ex)} {n(ey)}'), 0.6 * h
    if ch == '6':
        r = 0.3 * h
        cx, cy = x + 0.3 * h, y + 0.7 * h
        return (f'M{n(x + 0.5 * h)} {n(y)}Q{n(x)} {n(y + 0.28 * h)} {n(x)} {n(cy)}'
                f'M{n(cx - r)} {n(cy)}a{n(r)} {n(r)} 0 1 0 {n(2 * r)} 0a{n(r)} {n(r)} 0 1 0 {n(-2 * r)} 0'), 0.6 * h
    if ch == '.':
        return f'M{n(x)} {n(y + h)}h0', 0
    raise KeyError(ch)


def text(s, cx, y, h, gap):
    """Centred single-stroke text; returns a path d string."""
    widths = [glyph(c, 0, 0, h)[1] for c in s]
    total = sum(widths) + gap * (len(s) - 1)
    x = cx - total / 2
    out = []
    for c, w in zip(s, widths):
        out.append(glyph(c, x, y, h)[0])
        x += w + gap
    return ''.join(out)


# ---------------------------------------------------------------- shared icons
def pc():
    return svg(
        R(6, 10, 17, 44, 3),
        P('M11 19h7M11 26h7'),
        C(14.5, 45, 2.2, F),
        R(28, 14, 30, 24, 3),
        P('M43 38v13M35 52h16'),
    )


def laptop():
    return svg(
        R(11, 13, 42, 29, 3),
        P('M4 49h56'),
    )


def hdmi_plug(y=34):
    # HDMI type-A face: wide top, chamfered bottom corners.
    return [P(f'M8 {y}h48v9l-6 8H14l-6-8z'), P(f'M17 {y + 7}h30')]


def hdmi():
    return svg(P(text('HDMI', 32, 9, 14, 4.6)), *hdmi_plug(35))


def vga():
    dots = [C(x, 41, 1.9, F) for x in (20, 26, 32, 38, 44)]
    dots += [C(x, 47.5, 1.9, F) for x in (23, 29, 35, 41)]
    return svg(P(text('VGA', 32, 9, 14, 4.6)), P('M8 35h48l-5 19H13z'), *dots)


def dvi():
    dots = [C(x, y, 1.7, F) for y in (40, 46) for x in (27, 31.5, 36, 40.5, 45)]
    return svg(
        P(text('DVI', 32, 9, 14, 4.6)),
        R(13, 34, 38, 18, 3),
        C(6.5, 43, 2.5),
        C(57.5, 43, 2.5),
        P('M18 43h4M20 41v4', 'stroke-width="2.5"'),
        *dots,
    )


def combo_jack():
    return svg(
        R(10, 7, 44, 50, 7),
        P('M22 17h20l-2.5 9h-15z'),
        C(27, 21.5, 1.2, F), C(32, 21.5, 1.2, F), C(37, 21.5, 1.2, F),
        C(17.5, 21.5, 1.8, F), C(46.5, 21.5, 1.8, F),
        P('M22 37h20v4l-4 5H26l-4-5z'),
    )


def hdbt():
    return svg(
        R(7, 7, 50, 50, 9),
        P('M17 19h30v19h-7v6H24v-6h-7z'),
        P('M24 24v4M28 24v4M32 24v4M36 24v4M40 24v4', 'stroke-width="2"'),
    )


def podium():
    return svg(
        P('M8 24h48l-4 8H12z'),
        P('M19 32l2.5 20h21L45 32'),
        P('M15 55h34'),
        P('M45 24c0-6-1-10-6-13'),
        C(37, 9.5, 3, F),
    )


def wireless_router():
    cx, cy = 32, 30
    return svg(
        R(7, 37, 50, 15, 4),
        C(39, 44.5, 2, F), C(45, 44.5, 2, F), C(51, 44.5, 2, F),
        P('M14 37l-4-14M50 37l4-14'),
        C(cx, cy, 2.4, F),
        P(arc(cx, cy, 7.5, 45, 135)),
        P(arc(cx, cy, 14, 45, 135)),
        P(arc(cx, cy, 20.5, 48, 132)),
    )


def stream_box():
    # Generic set-top streaming box (no brand logo).
    return svg(
        R(7, 21, 50, 24, 8),
        P('M15 51h34'),
        P(text('TV', 32, 28.5, 9, 2.4), 'stroke-width="3"'),
    )


def usb_media():
    return svg(
        R(22, 6, 20, 16, 2),
        R(26.5, 11, 4, 4, 0.5, F), R(33.5, 11, 4, 4, 0.5, F),
        R(14, 22, 36, 36, 5),
        P('M32 52V30M28.5 33.5 32 30l3.5 3.5M32 47l-7-4.5V39M32 43.5l7-4.5v-3.5', 'stroke-width="2.6"'),
        C(25, 38, 2.4, F),
        R(36.6, 32.6, 4.8, 4.8, 0.6, F),
    )


def film():
    return svg(
        R(6, 12, 52, 40, 6),
        P('M6 21h52M6 43h52'),
        P('M17 12v9M27 12v9M37 12v9M47 12v9M17 43v9M27 43v9M37 43v9M47 43v9', 'stroke-width="2.5"'),
        P('M28 27v10l9-5z', 'fill="currentColor"'),
    )


def recorder():
    return svg(
        R(8, 8, 48, 48, 13),
        C(32, 32, 10, F),
    )


def livestream():
    cx, cy = 32, 20
    return svg(
        C(cx, cy, 3.6, F),
        P(arc(cx, cy, 9, 140, 220) + arc(cx, cy, 9, -40, 40)),
        P(arc(cx, cy, 16.5, 145, 215) + arc(cx, cy, 16.5, -35, 35)),
        P(text('LIVE', 32, 41, 13, 4.2)),
    )


def matrix():
    els = [R(5, 16, 54, 32, 5)]
    xs = (12.5, 23.5, 34.5, 45.5)
    ys = (22.5, 34.5)
    lit = {(0, 1), (1, 2)}
    for r, y in enumerate(ys):
        for c, x in enumerate(xs):
            if (r, c) in lit:
                els.append(R(x + 1, y + 1, 5, 5, 1, 'stroke-width="2.5"'))
            else:
                els.append(R(x, y, 7, 7, 1.6, F))
    return svg(*els)


def switcher():
    els = [R(5, 12, 54, 40, 5), P('M5 44h54')]
    for y in (18, 26, 34):
        for x in (11, 18.5, 26, 33.5):
            els.append(R(x, y, 5, 5, 1.2, F))
    els.append(P('M49 18v20', 'stroke-width="2"'))
    els.append(R(44.5, 24, 9, 6, 2, F))
    return svg(*els)


def multiview():
    return svg(
        R(6, 9, 52, 38, 4),
        P('M32 9v38M6 28h52'),
        R(10.5, 13.5, 17, 10, 1.5, F),
        P('M32 47v7M22 55h20'),
    )


def videoconf():
    return svg(
        C(32, 14, 6),
        P('M20 38v-2a12 12 0 0 1 24 0v2'),
        C(12.5, 24, 4.6),
        P('M3.5 41a9 9 0 0 1 18 0'),
        C(51.5, 24, 4.6),
        P('M42.5 41a9 9 0 0 1 18 0'),
        P('M5 47h54'),
        P('M14 47v8M50 47v8'),
    )


def projector():
    return svg(
        R(4, 20, 56, 26, 5),
        C(32, 33, 8.5),
        C(32, 33, 3, F),
        P('M10 28h8M10 33h8M10 38h8M46 28h8M46 33h8M46 38h8'),
        P('M14 46v4M50 46v4'),
    )


def led_wall():
    # 4x3 tile wall with the top-right tile being lifted into place.
    return svg(
        P('M6 23h36v10h12v20H6z'),
        P('M18 23v30M30 23v30M42 33v20M6 33h36M6 43h48', 'stroke-width="2.5"'),
        R(46, 11, 12, 10, 1),
    )


def tv():
    return svg(
        R(4, 11, 56, 35, 3),
        P('M16 46l-3 7M48 46l3 7'),
    )


def monitor():
    return svg(
        R(6, 8, 52, 36, 4),
        P('M6 37h52'),
        P('M32 44v10M22 55h20'),
    )


def camera_ptz():
    return svg(
        C(32, 25, 13),
        C(32, 25, 6),
        C(32, 25, 2, F),
        P('M13 23v13a7 7 0 0 0 7 7h24a7 7 0 0 0 7-7V23'),
        P('M26 43l-2 8h16l-2-8'),
        P('M17 54h30'),
    )


def camcorder():
    return svg(
        C(15, 15, 6.5),
        C(31, 15, 6.5),
        R(6, 25, 36, 27, 4),
        P('M42 33l15-7.5v25L42 43'),
    )


def tablet():
    return svg(
        P('M50 48h4a5 5 0 0 0 5-5V13a5 5 0 0 0-5-5H10a5 5 0 0 0-5 5v30a5 5 0 0 0 5 5h7.5'),
        C(54, 28, 1.8, F),
        P('M27 44V28.5a3.5 3.5 0 0 1 7 0V40a3 3 0 0 1 6 0v1.5a3 3 0 0 1 6 0V49c0 5-3 9-7 9h-7'
          'c-3 0-5-2-7-5l-4-6a2.6 2.6 0 0 1 4-3z'),
        P(arc(30.5, 28.5, 8.5, 40, 140), 'stroke-width="2.5"'),
        P(arc(30.5, 28.5, 14.5, 50, 130), 'stroke-width="2.5"'),
    )


def cast():
    ox, oy = 7, 53
    return svg(
        P('M7 25v-9a4 4 0 0 1 4-4h42a4 4 0 0 1 4 4v33a4 4 0 0 1-4 4H37'),
        C(ox + 1.2, oy - 1.2, 2.6, F),
        P(f'M{ox} {oy - 9}a9 9 0 0 1 9 9'),
        P(f'M{ox} {oy - 18}a18 18 0 0 1 18 18'),
    )


def handheld(head_r=9):
    """Hand-held microphone in local coords: head centred at (0,-13), handle down to y=20."""
    return (C(0, -13, head_r) +
            P(f'M{-head_r + 1.5} -13h{2 * head_r - 3}', 'stroke-width="2.5"') +
            P('M-6.5 -1h13l-3 21h-7z'))


def mixer():
    return svg(
        P('M16 8v48M32 8v48M48 8v48'),
        R(9, 35, 14, 8, 2.5, F),
        R(25, 15, 14, 8, 2.5, F),
        R(41, 27, 14, 8, 2.5, F),
    )


def music_note(dx=0):
    return [
        P(f'M{36 + dx} 44V10c0 8 13 9 13 21'),
        f'<ellipse cx="{n(28.5 + dx)}" cy="{n(45)}" rx="8.5" ry="6.5" transform="rotate(-20 {n(28.5 + dx)} 45)" {F}/>',
    ]


# ---------------------------------------------------------------- audio inputs
def wireless_mic():
    cx, cy = 40.5, 19.5
    return svg(
        G('translate(38 30) rotate(35)', handheld()),
        P(arc(cx, cy, 14, 150, 200)),
        P(arc(cx, cy, 20.5, 152, 198)),
    )


def wired_mic():
    return svg(
        G('translate(37 27) rotate(35)', handheld()),
        P('M23.5 46c-4 6-1 11 6 11h14c5 0 7-3 7-7'),
    )


def headset_mic():
    return svg(
        P('M11 36v-5a21 21 0 0 1 42 0v5'),
        R(6, 33, 11, 17, 4, F),
        R(47, 33, 11, 17, 4, F),
        P('M11.5 50c0 5 4 7 10 7h3'),
        R(24, 53.5, 10, 7, 3.5, F),
    )


def desk_mic():
    return svg(
        G('translate(38 24) rotate(30)', handheld()),
        P('M28 43v11'),
        P('M17 56h22'),
    )


def lavalier_mic():
    return svg(
        R(11, 6, 20, 19, 8, F),
        R(15.5, 27, 11, 9, 2),
        P('M9 42l24-5'),
        P('M21 36v4c0 10 5 17 14 17s14-6 14-14V22'),
        R(45, 8, 8, 12, 2, F),
    )


def shotgun_mic():
    return svg(
        R(5, 22, 54, 11, 5.5),
        P('M37 27.5h4M45 27.5h4', 'stroke-width="2.5"'),
        '<ellipse cx="16" cy="27.5" rx="3.5" ry="10" stroke-width="3"/>',
        '<ellipse cx="29" cy="27.5" rx="3.5" ry="10" stroke-width="3"/>',
        P('M16 37.5h13'),
        R(18.5, 40, 8, 17, 3, F + ' transform="rotate(12 22.5 48.5)"'),
    )


def pro_mic():
    return svg(
        R(23, 6, 18, 30, 9),
        P('M23 16h7M23 22h7M23 28h7', 'stroke-width="2.5"'),
        P('M16 27a16 16 0 0 0 32 0'),
        P('M32 43v10M24 55h16'),
        P('M9 14v18M3 19v8M55 14v18M61 19v8'),
    )


def conf_mic():
    return svg(
        P('M6 50h52l-9-16H17z'),
        P('M22 43h18', 'stroke-width="3"'),
        C(46, 43, 2, F),
    )


def xlr():
    return svg(
        C(32, 32, 25),
        C(32, 32, 17.5, 'stroke-width="2.5"'),
        R(29, 9.5, 6, 6, 1, F),
        C(24, 30, 3.4, F),
        C(40, 30, 3.4, F),
        C(32, 41, 3.4, F),
    )


def trs_plug(label, w):
    # Plug drawn tip-up in local coords, then rotated -45deg.
    hw = w / 2
    local = (
        R(-hw, -31, w, 7, hw, F) +          # tip
        R(-hw, -22.5, w, 4, 0, F) +         # ring
        R(-hw, -17, w, 8, 0, F) +           # sleeve
        R(-6, -7.5, 12, 20, 3) +            # handle
        P('M-3.5 12.5l1 5h5l1-5', 'fill="currentColor"')
    )
    # Cable leaves the plug end at local (0,17.5) -> (42.4,39.4) after the transform.
    return svg(
        G('translate(30 27) rotate(-45)', local),
        P('M42.5 39.5c4 4 6 9 3 13s-8 3-11 0'),
        P(text(label, 15, 43, 12, 2.8), 'stroke-width="3"'),
    )


def disc():
    return svg(
        C(32, 32, 25),
        C(32, 32, 8),
        C(32, 32, 2.4, F),
        P(arc(32, 32, 17, 105, 160), 'stroke-width="2.5"'),
    )


def music():
    return svg(*music_note(-1))


# ---------------------------------------------------------------- audio outputs
def main_speaker():
    return svg(
        P('M6 25h10l15-13v40L16 39H6z'),
        P('M40 24a11 11 0 0 1 0 16'),
        P('M47 17a20 20 0 0 1 0 30'),
    )


def stage_speaker():
    return svg(
        P('M5 52h54V16H25L5 34z'),
        C(41, 34, 10),
        C(41, 34, 3, F),
    )


def subwoofer():
    return svg(
        R(8, 8, 48, 46, 5),
        C(32, 29, 14),
        C(32, 29, 5),
        P('M25 48h14'),
    )


def headphones():
    return svg(
        P('M10 40v-8a22 22 0 0 1 44 0v8'),
        R(6, 36, 12, 19, 4, F),
        R(46, 36, 12, 19, 4, F),
    )


def fx():
    return svg(P('M8 28v8M16 21v22M24 11v42M32 19v26M40 14v36M48 23v18M56 28.5v7'))


def echo():
    cx, cy = 12, 32
    return svg(
        C(cx, cy, 4.5, F),
        P(arc(cx, cy, 13, -48, 48)),
        P(arc(cx, cy, 25, -42, 42), 'opacity=".6"'),
        P(arc(cx, cy, 37, -36, 36), 'opacity=".3"'),
    )


def recorder_audio():
    return svg(*music_note(-6), C(50, 46, 7, F), C(50, 46, 10.5, 'stroke-width="2.5"'))


# ---------------------------------------------------------------- lighting
SUN_C = (32, 32)


def rays(r0, r1, count=8, offset=0):
    out = []
    for i in range(count):
        a = offset + i * 360 / count
        x0, y0 = pt(*SUN_C, r0, a)
        x1, y1 = pt(*SUN_C, r1, a)
        out.append(f'M{n(x0)} {n(y0)}L{n(x1)} {n(y1)}')
    return P(''.join(out))


def cube():
    return svg(
        P('M32 6l23 12v28L32 58 9 46V18z'),
        P('M9 18l23 12 23-12M32 30v28'),
    )


def all_off():
    return svg(C(32, 32, 13))


def all_on():
    return svg(C(32, 32, 11, F), rays(18, 26))


def dim():
    return svg(
        C(32, 32, 12),
        P('M32 20a12 12 0 0 0 0 24z', F),
        rays(19, 22.5),
    )


def color_wheel():
    els = []
    r_out, r_in, gap = 26, 9, 1.6
    for i in range(12):
        hue = i * 30
        a0, a1 = 90 - i * 30, 90 - (i + 1) * 30
        # angular padding so wedges have even gaps
        po, pi = math.degrees(gap / 2 / r_out), math.degrees(gap / 2 / r_in)
        o0, o1 = pt(32, 32, r_out, a0 - po), pt(32, 32, r_out, a1 + po)
        i0, i1 = pt(32, 32, r_in, a1 + pi), pt(32, 32, r_in, a0 - pi)
        d = (f'M{n(o0[0])} {n(o0[1])}A{r_out} {r_out} 0 0 1 {n(o1[0])} {n(o1[1])}'
             f'L{n(i0[0])} {n(i0[1])}A{r_in} {r_in} 0 0 0 {n(i1[0])} {n(i1[1])}z')
        els.append(P(d, f'fill="hsl({hue} 85% 55%)" stroke="none"'))
    return svg(*els)


def presentation():
    return svg(
        R(24, 8, 34, 26, 2.5),
        P('M31 17h18M31 24h11'),
        C(13, 24, 6),
        P('M4 56V46a9 9 0 0 1 9-9h3l11-7'),
    )


def speech():
    return svg(
        C(32, 12, 6),
        P('M21 31a11 11 0 0 1 22 0'),
        P('M8 31h48l-4 7H12z'),
        P('M19 38l2.5 15h21L45 38'),
        P('M15 56h34'),
        P('M15 31c0-5 0-8-3-11'),
        C(11, 18, 2.6, F),
    )


def dimmer():
    return svg(
        P('M8 16h48M8 32h48M8 48h48'),
        C(18, 16, 6, F),
        C(40, 32, 6, F),
        C(28, 48, 6, F),
    )


def performance():
    return svg(
        C(15, 12, 5, F),
        P('M17 19l3 15M18 24l-10-5M18.5 25.5l12 3M20 34l-7 9 3 11M20 34l7 9-2 11'),
        C(48, 11, 5, F),
        P('M46 18l-3 15M45 22l12-6M44.5 24.5l-11 3M43 33l8 9 4 10M43 33l-6 10 2 11'),
    )


def spotlight():
    # Angled stage fixture on a ceiling bar, beam landing on a floor pool.
    return svg(
        P('M6 6h22M17 6v6'),
        R(7, 10, 20, 13, 3, F + ' transform="rotate(38 17 16.5)"'),
        P('M19 26L28 52h28L28 17z', 'fill="currentColor" stroke="none" opacity=".3"'),
        P('M19 26l9 25M28 17l27 31', 'stroke-width="2.5"'),
        '<ellipse cx="43" cy="51.5" rx="16" ry="4.5"/>',
    )


# ---------------------------------------------------------------- manifest
ICONS = {
    # video / in
    'video/in/11_pc': pc,
    'video/in/12_laptop': laptop,
    'video/in/13_dvi': dvi,
    'video/in/13_podium': podium,
    'video/in/21_hdmi': hdmi,
    'video/in/22_vga': vga,
    'video/in/23_combo_jack': combo_jack,
    'video/in/24_hdbt': hdbt,
    'video/in/31_player': film,
    'video/in/32_media': usb_media,
    'video/in/33_appletv': stream_box,
    'video/in/34_google_cast': cast,
    'video/in/41_wireless': wireless_router,
    'video/in/42_tablet': tablet,
    'video/in/51_camera': camera_ptz,
    'video/in/51_fixed_cam': camcorder,
    'video/in/52_maxtix': matrix,
    'video/in/53_switcher': switcher,
    'video/in/54_multiview': multiview,
    'video/in/55_recorder': recorder,
    'video/in/61_livestream': livestream,
    'video/in/62_videoconf': videoconf,
    # video / out
    'video/out/11_projector': projector,
    'video/out/12_led': led_wall,
    'video/out/13_tv': tv,
    'video/out/14_monitor': monitor,
    'video/out/21_switcher': switcher,
    'video/out/22_recorder': recorder,
    'video/out/23_livestream': livestream,
    'video/out/31_maxtix': matrix,
    'video/out/32_hdmi': hdmi,
    'video/out/33_vga': vga,
    # audio / in
    'audio/in/0_default': mixer,
    'audio/in/12_wireless_mic': wireless_mic,
    'audio/in/13_wired_mic': wired_mic,
    'audio/in/14_headset_mic': headset_mic,
    'audio/in/15_desk_mic': desk_mic,
    'audio/in/15_lavalier_mic': lavalier_mic,
    'audio/in/16_condenser_mic': shotgun_mic,
    'audio/in/16_desk_mic': desk_mic,
    'audio/in/17_condenser_mic': shotgun_mic,
    'audio/in/17_pro_mic': pro_mic,
    'audio/in/18_podium_mic': podium,
    'audio/in/18_pro_mic': pro_mic,
    'audio/in/19_conf_mic': conf_mic,
    'audio/in/1a_podium_mic': podium,
    'audio/in/21_xlr': xlr,
    'audio/in/22_6.3mm': lambda: trs_plug('6.3', 6),
    'audio/in/23_3.5mm': lambda: trs_plug('3.5', 4.5),
    'audio/in/24_hdmi': hdmi,
    'audio/in/31_pc': pc,
    'audio/in/32_laptop': laptop,
    'audio/in/33_wireless': wireless_router,
    'audio/in/34_recorder': recorder,
    'audio/in/41_music': music,
    'audio/in/42_video': disc,
    'audio/in/43_appletv': stream_box,
    'audio/in/44_media': usb_media,
    # audio / out
    'audio/out/0_default': mixer,
    'audio/out/11_main_speaker': main_speaker,
    'audio/out/12_stage_speaker': stage_speaker,
    'audio/out/13_subwoofer': subwoofer,
    'audio/out/14_monitor': headphones,
    'audio/out/21_fx': fx,
    'audio/out/22_echo': echo,
    'audio/out/81_recorder_audio': recorder_audio,
    'audio/out/82_recorder_video': recorder,
    'audio/out/91_projector': projector,
    'audio/out/92_led_display': led_wall,
    # light
    'light/0_default': cube,
    'light/basic_all_off': all_off,
    'light/basic_all_on': all_on,
    'light/basic_dim': dim,
    'light/color_stage': color_wheel,
    'light/scene_movie': film,
    'light/scene_presentation': presentation,
    'light/scene_projection': projector,
    'light/scene_speech': speech,
    'light/scene_video_wall': led_wall,
    'light/stage_dimmer': dimmer,
    'light/stage_performance': performance,
    'light/stage_spotlight': spotlight,
}


PREVIEW = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CP3 Icon Preview</title>
<style>
  body {{ margin: 0; padding: 16px; background: #1f2329; color: #d6dae0; font: 14px/1.4 system-ui, sans-serif; }}
  h1 {{ font-size: 20px; margin: 0 0 4px; }}
  h2 {{ font-size: 16px; margin: 28px 0 10px; color: #fff; }}
  .note {{ color: #8f98a3; margin: 0 0 8px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; }}
  figure {{ margin: 0; padding: 10px; background: #2b3038; border-radius: 8px; }}
  .icons {{ display: flex; align-items: flex-end; gap: 8px; }}
  .new {{ width: 96px; height: 96px; background: #3a404a; border-radius: 6px; }}
  .old {{ width: 40px; height: 40px; background: #3a404a; border-radius: 4px; opacity: .85; }}
  figcaption {{ margin-top: 6px; font-size: 12px; word-break: break-all; }}
  body.light {{ background: #f2f3f5; color: #333; }}
  body.light h2 {{ color: #111; }}
  body.light figure {{ background: #fff; }}
  body.light .new, body.light .old {{ background: #e4e6ea; }}
</style>
</head>
<body>
<h1>CP3 Icon Preview</h1>
<p class="note">大圖：新 SVG（以 &lt;img&gt; 載入）；右下小圖：原始 PNG。
<label><input type="checkbox" onchange="document.body.classList.toggle('light', this.checked)"> 淺色背景</label></p>
{sections}
</body>
</html>
"""


def preview():
    groups = {}
    for rel in ICONS:
        groups.setdefault(os.path.dirname(rel), []).append(rel)
    sections = []
    for group, rels in groups.items():
        cards = []
        for rel in rels:
            old = rel + '.png'
            old_img = f'<img class="old" src="{old}" alt="">' if os.path.exists(os.path.join(ROOT, old)) else ''
            cards.append(f'<figure><div class="icons"><img class="new" src="{rel}.svg" alt="">{old_img}</div>'
                         f'<figcaption>{os.path.basename(rel)}</figcaption></figure>')
        sections.append(f'<h2>{group}</h2>\n<div class="grid">\n' + '\n'.join(cards) + '\n</div>')
    return PREVIEW.format(sections='\n'.join(sections))


if __name__ == '__main__':
    for rel, fn in ICONS.items():
        path = os.path.join(ROOT, rel + '.svg')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', newline='\n') as f:
            f.write(fn())
    with open(os.path.join(ROOT, 'preview.html'), 'w', newline='\n') as f:
        f.write(preview())
    print(len(ICONS), 'icons written')
