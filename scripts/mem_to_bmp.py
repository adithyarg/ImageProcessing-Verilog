# mem_to_bmp.py (batch)
from PIL import Image
from pathlib import Path
import os

# update these to your image size
WIDTH = 128
HEIGHT = 128
IMG_DIR = r"your_path_dir"

# files produced by convolution testbench
file_map = {
    "blur.mem":        "blur.bmp",
    "motion_blur.mem": "motion_blur.bmp",
    "sharpen.mem":     "sharpen.bmp",
    "sobel_edge.mem":  "sobel_edge.bmp",
    "emboss.mem":      "emboss.bmp",
    "outline.mem":     "outline.bmp",
    # also include the simple filters produced earlier (if present)
    "1.Invert.mem":    "1.Invert.bmp",
    "2.Grayscale.mem": "2.Grayscale.bmp",
    "3.BrightnessInc.mem": "3.BrightnessInc.bmp",
    "4.BrightnessDec.mem": "4.BrightnessDec.bmp",
    "5.RedFilter.mem": "5.RedFilter.bmp",
    "6.GreenFilter.mem": "6.GreenFilter.bmp",
    "7.BlueFilter.mem": "7.BlueFilter.bmp",
    "8.Original.mem":  "8.Original.bmp",
}

def mem_to_bmp(mem_path, bmp_path):
    with open(mem_path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]
    if len(lines) < WIDTH * HEIGHT:
        print(f"Warning: {mem_path} has {len(lines)} pixels, expected {WIDTH*HEIGHT}")
    pixels = []
    for line in lines[:WIDTH*HEIGHT]:
        # each line can be long: we only need the lower 6 hex digits for pixel
        hex_pixel = line[-6:]
        val = int(hex_pixel, 16)
        r = (val >> 16) & 0xFF
        g = (val >> 8) & 0xFF
        b = val & 0xFF
        pixels.append((r,g,b))

    img = Image.new("RGB", (WIDTH, HEIGHT))
    img.putdata(pixels)
    img.save(bmp_path)
    print(f"Wrote {bmp_path}")

def main():
    Path(IMG_DIR).mkdir(parents=True, exist_ok=True)
    for mem_name, bmp_name in file_map.items():
        mem_path = os.path.join(IMG_DIR, mem_name)
        bmp_path = os.path.join(IMG_DIR, bmp_name)
        if os.path.exists(mem_path):
            mem_to_bmp(mem_path, bmp_path)
        else:
            print(f"Skipping {mem_name} (not found)")

if __name__ == "__main__":
    main()
