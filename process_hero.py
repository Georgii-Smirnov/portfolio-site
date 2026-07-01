"""Process the Windows XP-style hero image into portrait versions."""
from PIL import Image
import os

SRC = r"C:\Users\EGOR\Downloads\214f851a-cccc-44fd-9aa2-d645bd42fc6a.png"
OUT_DIR = "images"

SIZES = {
    "portrait.png": (800, 1042),
    "portrait-2x.png": (1228, 1600),
}

img = Image.open(SRC).convert("RGB")
W, H = img.size
print(f"Source: {W}x{H}")

# Crop to focus on the actual photo within the Windows XP photo viewer window
# Skip title bar (top ~3%) and bottom status bar (~3%)
# Keep the full photo + menu (it's part of the meme look)
left = int(W * 0.08)
right = int(W * 0.95)
top = int(H * 0.06)
bottom = int(H * 0.96)

face = img.crop((left, top, right, bottom))
fw, fh = face.size
print(f"After crop: {fw}x{fh}")

# Now center-crop to portrait ratio 800:1042
target_ratio = 800 / 1042
src_ratio = fw / fh

if src_ratio > target_ratio:
    new_w = int(fh * target_ratio)
    off = (fw - new_w) // 2
    face = face.crop((off, 0, off + new_w, fh))
else:
    new_h = int(fw / target_ratio)
    off = (fh - new_h) // 2
    face = face.crop((0, off, fw, off + new_h))

print(f"After ratio crop: {face.size}")

for filename, (w, h) in SIZES.items():
    out = face.resize((w, h), Image.LANCZOS)
    png_path = os.path.join(OUT_DIR, filename)
    avif_path = os.path.join(OUT_DIR, filename.replace(".png", ".avif"))
    out.save(png_path, "PNG", optimize=True)
    print(f"Saved {png_path} ({w}x{h})")
    try:
        out.save(avif_path, "AVIF", quality=70)
        print(f"Saved {avif_path}")
    except Exception as e:
        print(f"AVIF failed: {e}")

print("Done")
