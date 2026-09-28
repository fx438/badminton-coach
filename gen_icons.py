"""生成 PWA 图标（简单几何图形，不依赖外部图片/字体）。"""
from PIL import Image, ImageDraw
import math

PRIMARY = (14, 92, 74)      # 深羽毛球场馆绿
ACCENT = (226, 163, 61)     # 球托暖黄
BG = (246, 243, 236)        # 米白


def make_icon(size: int, path: str, padded: bool = False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if padded:
        # maskable icon: 留出安全边距，背景铺满
        draw.rectangle([0, 0, size, size], fill=PRIMARY)
        cx, cy = size / 2, size / 2
        r = size * 0.30
    else:
        draw.ellipse([0, 0, size, size], fill=PRIMARY)
        cx, cy = size / 2, size / 2
        r = size * 0.34

    # 球拍拍头（椭圆环）
    head_w, head_h = r * 1.3, r * 1.65
    bbox = [cx - head_w / 2, cy - head_h / 2 - r * 0.15, cx + head_w / 2, cy + head_h / 2 - r * 0.15]
    draw.ellipse(bbox, outline=BG, width=max(2, int(size * 0.045)))

    # 拍柄
    handle_top = (cx, cy + head_h / 2 - r * 0.15)
    handle_bottom = (cx, cy + head_h * 0.95)
    draw.line([handle_top, handle_bottom], fill=BG, width=max(3, int(size * 0.05)))

    # 羽毛球（小圆 + 三条羽毛线），放在拍头右上方
    ball_cx, ball_cy = cx + head_w * 0.55, cy - head_h * 0.55
    ball_r = size * 0.07
    draw.ellipse(
        [ball_cx - ball_r, ball_cy - ball_r, ball_cx + ball_r, ball_cy + ball_r],
        fill=ACCENT,
    )
    for ang in (-25, 0, 25):
        rad = math.radians(ang - 90)
        x2 = ball_cx + math.cos(rad) * ball_r * 3.0
        y2 = ball_cy + math.sin(rad) * ball_r * 3.0
        draw.line([(ball_cx, ball_cy), (x2, y2)], fill=ACCENT, width=max(2, int(size * 0.02)))

    img.save(path)


make_icon(192, "icons/icon-192.png", padded=False)
make_icon(512, "icons/icon-512.png", padded=False)
make_icon(512, "icons/icon-512-maskable.png", padded=True)
print("icons generated")
