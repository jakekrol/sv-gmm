#!/usr/bin/env bash

# combine files
mapfile -t files < <(ls ../../data/2026_01-variants-plotting-data/ | grep -v "README")
for f in "${files[@]}"; do
    cat "../../data/2026_01-variants-plotting-data/${f}" >> combined_variants.tsv
done
./download_bams.py

./plot.sh

python -c "
from PIL import Image, ImageDraw, ImageFont
import glob
import os

images = []
for f in sorted(glob.glob('*.png')):
    # Load image
    img = Image.open(f)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # Create new image with space for filename
    new_height = img.height + 80
    new_img = Image.new('RGB', (img.width, new_height), 'white')
    
    # Add filename text
    draw = ImageDraw.Draw(new_img)
    filename = os.path.basename(f)
    try:
        font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans.ttf', 36)
    except:
        font = ImageFont.load_default()
    
    # Center the text
    text_width = draw.textlength(filename, font=font)
    x = (new_img.width - text_width) // 2
    draw.text((x, 20), filename, fill='black', font=font)
    
    # Paste original image below text
    new_img.paste(img, (0, 80))
    images.append(new_img)

images[0].save('all.pdf', save_all=True, append_images=images[1:])
"
