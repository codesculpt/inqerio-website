"""Inqerio launch posters for social media: square, portrait, story and wide. Pillow only, brand fonts from the app."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

ROOT = os.path.expanduser('~/mnt/PROJECTS')
APP = f'{ROOT}/inqerio-team'
FONTS = f'{APP}/node_modules/@fontsource-variable'
MANROPE = f'{FONTS}/manrope/files/manrope-latin-wght-normal.woff2'
INTER = f'{FONTS}/inter/files/inter-latin-wght-normal.woff2'
LOCKUP = f'{APP}/src/renderer/assets/brand/lockup-white.png'
SHOT = f'{ROOT}/inqerio-website/media/app-view-2400.webp'

BG0, BG1 = (9, 24, 31), (14, 40, 49)
ACCENT, ACCENT2 = (21, 166, 158), (52, 189, 180)
WHITE, MUTED, FAINT = (245, 250, 250), (172, 196, 202), (120, 150, 158)

def font(path, size, weight):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f

def gradient(w, h):
    im = Image.new('RGB', (w, h), BG0)
    px = im.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(round(BG0[i] + (BG1[i] - BG0[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return im

def glow(im, cx, cy, r, colour, alpha):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=colour + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.55))
    im.alpha_composite(layer)

def dots(im, step=36, alpha=22):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w, h = im.size
    for y in range(step, h, step):
        for x in range(step, w, step):
            d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(255, 255, 255, alpha))
    im.alpha_composite(layer)

def rounded(size, radius, fill, outline=None, width=1):
    im = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=fill, outline=outline, width=width)
    return im

def shadow(im, box, radius, blur, alpha=150, offset=(0, 26)):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]), radius=radius, fill=(0, 0, 0, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    im.alpha_composite(layer)

def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def screenshot_card(im, x, y, w, fade=0.32, radius=22):
    shot = Image.open(SHOT).convert('RGBA')
    sw, sh = shot.size
    h = round(w * sh / sw)
    shot = shot.resize((w, h), Image.LANCZOS)
    # Rounded corners and a soft fade into the background at the bottom: the interface is shown in part, as on the website.
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    grad = Image.new('L', (w, h), 255)
    gp = grad.load()
    start = int(h * (1 - fade))
    for yy in range(start, h):
        v = int(255 * (1 - (yy - start) / (h - start)) ** 1.4)
        for xx in range(w):
            gp[xx, yy] = v
    from PIL import ImageChops
    mask = ImageChops.multiply(mask, grad)
    shadow(im, (x, y, x + w, y + h), radius, 34, alpha=170)
    frame = rounded((w + 2, h + 2), radius + 1, (255, 255, 255, 0), outline=(255, 255, 255, 46), width=1)
    im.alpha_composite(frame, (x - 1, y - 1))
    im.paste(shot, (x, y), mask)
    return h

def chips(im, draw, items, x, y, max_w, f, gap=12, pad=(22, 12)):
    cx, cy = x, y
    line_h = f.size + pad[1] * 2
    for t in items:
        tw = draw.textlength(t, font=f)
        cw = int(tw + pad[0] * 2)
        if cx + cw > x + max_w:
            cx, cy = x, cy + line_h + gap
        chip = rounded((cw, line_h), line_h // 2, (255, 255, 255, 18), outline=(255, 255, 255, 40))
        im.alpha_composite(chip, (cx, cy))
        draw.text((cx + pad[0], cy + pad[1] - 1), t, font=f, fill=WHITE)
        cx += cw + gap
    return cy + line_h

def poster(w, h, out, story=False):
    """One column, laid out top to bottom with a fixed budget so nothing can overlap."""
    im = gradient(w, h).convert('RGBA')
    glow(im, int(w * 0.9), int(h * 0.1), int(w * 0.45), ACCENT, 70)
    glow(im, int(w * 0.05), int(h * 0.97), int(w * 0.4), ACCENT, 34)
    dots(im, step=40, alpha=16)
    d = ImageDraw.Draw(im)
    m = 72

    # 1. Brand row
    top = 56
    lock = Image.open(LOCKUP).convert('RGBA')
    lw = 230
    lock = lock.resize((lw, round(lw * lock.size[1] / lock.size[0])), Image.LANCZOS)
    im.alpha_composite(lock, (m, top))
    f_pill = font(INTER, 21, 'SemiBold')
    pill = 'FREE BETA  ·  WINDOWS'
    pw, ph = int(d.textlength(pill, font=f_pill) + 44), 42
    py = top + (lock.size[1] - ph) // 2
    im.alpha_composite(rounded((pw, ph), ph // 2, ACCENT + (46,), outline=ACCENT2 + (140,)), (w - m - pw, py))
    d.text((w - m - pw + 22, py + 9), pill, font=f_pill, fill=ACCENT2)
    y = top + lock.size[1] + (64 if not story else 190)

    # 2. Headline
    hs = 80 if not story else 86
    f_h = font(MANROPE, hs, 'ExtraBold')
    d.text((m, y), 'Your whole study,', font=f_h, fill=WHITE)
    y += int(hs * 1.12)
    d.text((m, y), 'in one workspace.', font=f_h, fill=ACCENT2)
    y += int(hs * 1.12) + 26

    # 3. One short line
    f_sub = font(INTER, 31, 'Regular')
    for line in wrap(d, 'Write, review the literature, analyse data and work with your team, all in one desktop app.', f_sub, w - 2 * m):
        d.text((m, y), line, font=f_sub, fill=MUTED)
        y += 44
    y += 34

    # 4. Reserve the bottom first: chips, then footer. The screenshot takes whatever room is left.
    f_chip = font(INTER, 24, 'Medium')
    items = ['Live citations', 'Reviews to PRISMA', 'R · Python · Stata · SAS · SPSS', 'Qualitative coding', 'Ethics consultant', 'Team projects']
    cols, gap, ch = 2, 14, 58
    cw = (w - 2 * m - gap) // cols
    rows = (len(items) + cols - 1) // cols
    chips_h = rows * ch + (rows - 1) * gap
    footer_h = 150
    chips_top = h - 56 - footer_h - 40 - chips_h
    shot_h = chips_top - 30 - y
    assert shot_h > 300, shot_h

    shot = Image.open(SHOT).convert('RGBA')
    sw = w - 2 * m
    full_h = round(sw * shot.size[1] / shot.size[0])
    shot = shot.resize((sw, full_h), Image.LANCZOS).crop((0, 0, sw, min(full_h, shot_h)))
    sh = shot.size[1]
    mask = Image.new('L', (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, sh - 1), radius=22, fill=255)
    from PIL import ImageChops
    grad = Image.new('L', (sw, sh), 255)
    gp = grad.load()
    start = int(sh * 0.78)
    for yy in range(start, sh):
        v = int(255 * (1 - (yy - start) / (sh - start)))
        for xx in range(sw):
            gp[xx, yy] = v
    mask = ImageChops.multiply(mask, grad)
    shadow(im, (m, y, m + sw, y + sh), 22, 30, alpha=150)
    im.paste(shot, (m, y), mask)
    d = ImageDraw.Draw(im)

    # 5. Chips, two columns, text centred
    for i, t in enumerate(items):
        cx = m + (i % cols) * (cw + gap)
        cy = chips_top + (i // cols) * (ch + gap)
        im.alpha_composite(rounded((cw, ch), ch // 2, (255, 255, 255, 20), outline=(255, 255, 255, 46)), (cx, cy))
        tw = d.textlength(t, font=f_chip)
        assert tw < cw - 24, (t, tw, cw)
        d.text((cx + (cw - tw) / 2, cy + (ch - f_chip.size) / 2 - 2), t, font=f_chip, fill=WHITE)

    # 6. Footer
    fy = chips_top + chips_h + 40
    f_url = font(MANROPE, 60, 'ExtraBold')
    f_small = font(INTER, 24, 'Regular')
    f_tiny = font(INTER, 19, 'Medium')
    d.text((m, fy), 'inqerio.com', font=f_url, fill=WHITE)
    d.text((m, fy + 78), 'No account needed  ·  Your files stay on your computer', font=f_small, fill=MUTED)
    made = 'Made by CodeSculpt  ·  codesculpt.ca'
    d.text((m, fy + 116), made, font=f_tiny, fill=FAINT)
    assert fy + 116 + f_tiny.size < h - 30, 'footer off the page'
    im.convert('RGB').save(out, quality=90, optimize=True)
    print('wrote', out, im.size, 'screenshot height', sh, 'footer bottom', fy + 116 + f_tiny.size)

poster(1080, 1350, 'inqerio-poster-whatsapp.jpg')
poster(1080, 1920, 'inqerio-poster-status.jpg', story=True)
