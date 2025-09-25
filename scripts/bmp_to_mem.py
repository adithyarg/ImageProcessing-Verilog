from PIL import Image
import sys

def bmp_to_mem(input_path, output_path):
    img = Image.open(input_path).convert("RGB")
    width, height = img.size
    pixels = list(img.getdata())

    with open(output_path, "w") as f:
        for (r, g, b) in pixels:
            val = (r << 16) | (g << 8) | b
            f.write(f"{val:06x}\n")

    print(f"✅ Wrote {output_path} ({width}x{height}, {len(pixels)} pixels)")
    return width, height

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bmp_to_mem.py input.bmp output.mem")
    else:
        bmp_to_mem(sys.argv[1], sys.argv[2])
