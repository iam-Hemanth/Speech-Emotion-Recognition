#!/usr/bin/env python3
"""
Script to convert the SVG logo to PNG format.
Requires cairosvg: pip install cairosvg
"""

import sys
from pathlib import Path

def convert_svg_to_png():
    """Convert SVG logo to PNG format."""
    try:
        # Try to import cairosvg
        import cairosvg
        
        svg_path = Path(__file__).parent.parent / "src" / "ser" / "assets" / "logo.svg"
        png_path = Path(__file__).parent.parent / "src" / "ser" / "assets" / "logo.png"
        
        if not svg_path.exists():
            print(f"❌ SVG logo not found at: {svg_path}")
            return False
        
        # Convert SVG to PNG
        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(png_path),
            output_width=100,
            output_height=100
        )
        
        print(f"✅ Logo converted successfully: {png_path}")
        return True
        
    except ImportError:
        print("❌ cairosvg not installed. Install with: pip install cairosvg")
        print("💡 The SVG logo will still work in the web app.")
        return False
    except Exception as e:
        print(f"❌ Error converting logo: {e}")
        return False

if __name__ == "__main__":
    convert_svg_to_png()
