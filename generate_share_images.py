#!/usr/bin/env -S uv run
"""
Generate OpenGraph share images for Hugo site
Creates 1200x630 images matching msherman.xyz aesthetic

Run this script whenever you:
- Add new blog posts or pages
- Update titles/descriptions of existing content
- Want to refresh the share images

Usage: uv run generate_share_images.py
"""

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Configuration
CONTENT_DIR = Path("hugo-site/content")
OUTPUT_DIR = Path("hugo-site/static/images/share")
IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 630

# Colors matching your site
BG_COLOR = (30, 30, 30)  # #1e1e1e
TEXT_COLOR = (224, 224, 224)  # #e0e0e0
DESC_COLOR = (160, 160, 160)  # #a0a0a0
ACCENT_COLOR = (255, 204, 0)  # #ffcc00 (your yellow)
GLOW_COLOR_1 = (79, 195, 247)  # #4fc3f7 (blue)
GLOW_COLOR_2 = (129, 199, 132)  # #81c784 (green)


def parse_frontmatter(file_path):
    """Extract title and description from Hugo frontmatter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]

            # Extract title - try double-quoted, then single-quoted, then unquoted
            title = None
            title_match = re.search(r'title:\s*"([^"]+)"', frontmatter)
            if title_match:
                title = title_match.group(1)
            else:
                title_match = re.search(r"title:\s*'([^']+)'", frontmatter)
                if title_match:
                    title = title_match.group(1)
                else:
                    title_match = re.search(r'title:\s*([^\n]+)', frontmatter)
                    if title_match:
                        title = title_match.group(1).strip()

            # Extract description - try double-quoted, then single-quoted, then unquoted
            description = None
            desc_match = re.search(r'description:\s*"([^"]+)"', frontmatter)
            if desc_match:
                description = desc_match.group(1)
            else:
                desc_match = re.search(r"description:\s*'([^']+)'", frontmatter)
                if desc_match:
                    description = desc_match.group(1)
                else:
                    desc_match = re.search(r'description:\s*([^\n]+)', frontmatter)
                    if desc_match:
                        description = desc_match.group(1).strip()

            return title, description

    return None, None


def create_gradient_background():
    """Create dark gradient background with subtle glow effects"""
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img, 'RGBA')

    # Create subtle gradient
    for y in range(IMAGE_HEIGHT):
        progress = y / IMAGE_HEIGHT
        # Darker at top and bottom, slightly lighter in middle
        if progress < 0.5:
            lightness = int(30 + progress * 20)
        else:
            lightness = int(40 - (progress - 0.5) * 20)

        color = (lightness, lightness, lightness)
        draw.rectangle([(0, y), (IMAGE_WIDTH, y + 1)], fill=color)

    # Add subtle glow orbs
    orb_layer = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
    orb_draw = ImageDraw.Draw(orb_layer)

    # Blue glow (top-right)
    orb_draw.ellipse(
        [(IMAGE_WIDTH - 200, -200), (IMAGE_WIDTH + 200, 200)],
        fill=(*GLOW_COLOR_1, 25)
    )

    # Green glow (bottom-left)
    orb_draw.ellipse(
        [(-150, IMAGE_HEIGHT - 150), (150, IMAGE_HEIGHT + 150)],
        fill=(*GLOW_COLOR_2, 25)
    )

    # Apply blur to orbs
    orb_layer = orb_layer.filter(ImageFilter.GaussianBlur(80))

    # Composite
    img = Image.alpha_composite(img.convert('RGBA'), orb_layer)

    return img.convert('RGB')


def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width"""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def generate_share_image(title, description, output_path):
    """Generate a share image with title and description"""

    # Create base image
    img = create_gradient_background()
    draw = ImageDraw.Draw(img)

    # Try to load Inter font, fall back to default
    try:
        # Adjust these paths based on where Inter font is located
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        desc_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        domain_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except OSError:
        print("Warning: Could not load custom fonts, using default")
        title_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
        domain_font = ImageFont.load_default()

    # Layout constants
    padding = 80
    max_text_width = IMAGE_WIDTH - (padding * 2)

    # Draw title (centered vertically, wrapped)
    y_position = 200

    if title:
        title_lines = wrap_text(title, title_font, max_text_width)

        for line in title_lines[:3]:  # Max 3 lines for title
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (IMAGE_WIDTH - text_width) // 2

            draw.text((x, y_position), line, font=title_font, fill=TEXT_COLOR)
            y_position += bbox[3] - bbox[1] + 10

    # Draw description
    y_position += 30

    if description and y_position < IMAGE_HEIGHT - 150:
        desc_lines = wrap_text(description, desc_font, max_text_width)

        for line in desc_lines[:3]:  # Max 3 lines for description
            bbox = draw.textbbox((0, 0), line, font=desc_font)
            text_width = bbox[2] - bbox[0]
            x = (IMAGE_WIDTH - text_width) // 2

            draw.text((x, y_position), line, font=desc_font, fill=DESC_COLOR)
            y_position += bbox[3] - bbox[1] + 10

    # Draw domain at bottom center
    domain_text = "msherman.xyz"
    bbox = draw.textbbox((0, 0), domain_text, font=domain_font)
    text_width = bbox[2] - bbox[0]
    x = (IMAGE_WIDTH - text_width) // 2
    draw.text((x, IMAGE_HEIGHT - 100), domain_text, font=domain_font, fill=ACCENT_COLOR)

    # Draw accent bar at bottom
    accent_height = 4
    for x in range(IMAGE_WIDTH):
        progress = x / IMAGE_WIDTH

        # Gradient: transparent -> blue -> green -> blue -> transparent
        if progress < 0.2:
            alpha = int(progress / 0.2 * 255)
            color = (*GLOW_COLOR_1, alpha)
        elif progress < 0.5:
            ratio = (progress - 0.2) / 0.3
            r = int(GLOW_COLOR_1[0] + (GLOW_COLOR_2[0] - GLOW_COLOR_1[0]) * ratio)
            g = int(GLOW_COLOR_1[1] + (GLOW_COLOR_2[1] - GLOW_COLOR_1[1]) * ratio)
            b = int(GLOW_COLOR_1[2] + (GLOW_COLOR_2[2] - GLOW_COLOR_1[2]) * ratio)
            color = (r, g, b, 255)
        elif progress < 0.8:
            ratio = (progress - 0.5) / 0.3
            r = int(GLOW_COLOR_2[0] + (GLOW_COLOR_1[0] - GLOW_COLOR_2[0]) * ratio)
            g = int(GLOW_COLOR_2[1] + (GLOW_COLOR_1[1] - GLOW_COLOR_2[1]) * ratio)
            b = int(GLOW_COLOR_2[2] + (GLOW_COLOR_1[2] - GLOW_COLOR_2[2]) * ratio)
            color = (r, g, b, 255)
        else:
            alpha = int((1 - (progress - 0.8) / 0.2) * 255)
            color = (*GLOW_COLOR_1, alpha)

        # Draw vertical line
        accent_img = Image.new('RGBA', (1, accent_height), color)
        img.paste(accent_img, (x, IMAGE_HEIGHT - accent_height), accent_img)

    # Save image
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, 'PNG', optimize=True)
    print(f"✓ Generated: {output_path}")


def main():
    """Generate share images for all content files"""

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate homepage image
    generate_share_image(
        "Maksym Sherman",
        "I believe in great work, ambition, and obsessiveness. I seek to understand the world through better explanations.",
        OUTPUT_DIR / "home.png"
    )

    # Generate images for all posts
    posts_dir = CONTENT_DIR / "posts"
    if posts_dir.exists():
        for post_file in posts_dir.glob("*.html"):
            title, description = parse_frontmatter(post_file)

            if title:
                # Use post filename as image name
                output_name = post_file.stem + ".png"
                output_path = OUTPUT_DIR / output_name

                generate_share_image(title, description, output_path)

    # Generate images for other pages
    for page_file in CONTENT_DIR.glob("*.html"):
        if page_file.name == "_index.html":
            continue

        title, description = parse_frontmatter(page_file)

        if title:
            output_name = page_file.stem + ".png"
            output_path = OUTPUT_DIR / output_name
            generate_share_image(title, description, output_path)

    print(f"\n✓ All share images generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
