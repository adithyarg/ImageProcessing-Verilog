# kernel_mem_generator.py
from PIL import Image
from pathlib import Path
import sys

def get_pixel(img, x, y):
    # clamp to image border (replicate)
    x = max(0, min(img.width - 1, x))
    y = max(0, min(img.height - 1, y))
    return img.getpixel((x, y))

def pack_neighborhood(img_path, out_mem_path):
    img = Image.open(img_path).convert("RGB")
    w, h = img.size

    lines = []
    for y in range(h):
        for x in range(w):
            # order p0..p8 top-left -> bottom-right
            coords = [(-1,-1),(0,-1),(1,-1), (-1,0),(0,0),(1,0), (-1,1),(0,1),(1,1)]
            hex_parts = []
            for dx, dy in coords:
                px = get_pixel(img, x+dx, y+dy)
                r,g,b = px
                hex_parts.append(f"{(r<<16)|(g<<8)|b:06x}")
            # concatenate p0..p8 (p0 = MSB)
            line = "".join(hex_parts)
            lines.append(line)

    Path(out_mem_path).write_text("\n".join(lines))
    print(f"Wrote {out_mem_path} ({w}x{h}, {len(lines)} entries)")
    return w, h

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python kernel_mem_generator.py input.bmp output_kernel_input.mem")
        sys.exit(1)
    pack_neighborhood(sys.argv[1], sys.argv[2])
