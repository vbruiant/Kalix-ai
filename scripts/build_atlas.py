import os
import json
from PIL import Image
from math import ceil, sqrt


def build_atlas(input_dir, output_image, output_metadata, tile_size=None):
    """Create a sprite atlas from all PNGs in input_dir."""
    files = [f for f in os.listdir(input_dir) if f.lower().endswith('.png')]
    if not files:
        raise ValueError(f"No PNG files found in {input_dir}")

    images = [Image.open(os.path.join(input_dir, f)) for f in files]

    # Optionally resize images to a consistent tile size
    if tile_size:
        try:
            resampling = Image.Resampling.LANCZOS
        except AttributeError:  # Pillow < 10
            resampling = Image.ANTIALIAS
        images = [img.resize(tile_size, resample=resampling) for img in images]

    width, height = images[0].size
    columns = ceil(sqrt(len(images)))
    rows = ceil(len(images) / columns)
    atlas = Image.new('RGBA', (columns * width, rows * height))

    metadata = {}
    for index, img in enumerate(images):
        x = (index % columns) * width
        y = (index // columns) * height
        atlas.paste(img, (x, y))
        metadata[files[index]] = {'x': x, 'y': y, 'width': width, 'height': height}

    atlas.save(output_image)
    with open(output_metadata, 'w') as f:
        json.dump(metadata, f, indent=2)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Build sprite atlas from PNG images.')
    parser.add_argument('input_dir', help='Directory containing PNG images')
    parser.add_argument('output_image', help='Path for the output atlas PNG')
    parser.add_argument('output_metadata', help='Path for the output metadata JSON')
    parser.add_argument('--tile-size', type=int, nargs=2, metavar=('W', 'H'),
                        help='Resize images to this size before packing')

    args = parser.parse_args()
    build_atlas(args.input_dir, args.output_image, args.output_metadata, args.tile_size)


if __name__ == '__main__':
    main()
