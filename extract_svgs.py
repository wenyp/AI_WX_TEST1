
import re
import os

# Configuration
ASSETS_DIR = 'pages/demo/assets'
HTML_FILE = 'demo.html'
WXML_FILE = 'pages/demo/demo.wxml'
WXSS_FILE = 'pages/demo/demo.wxss'

# Defined classes order based on HTML structure analysis (Same as before)
icon_classes = [
    'icon-signal',       # 0
    'icon-battery',      # 1
    'icon-back',         # 2
    'icon-more',         # 3
    'icon-close',        # 4
    'ai-btn-icon',       # 5
    'icon-solution',     # 6
    'icon-dynamic',      # 7
    'icon-product',      # 8
    'icon-customer',     # 9
    'icon-checkin',      # 10
    'icon-buy',          # 11
    'card-service-icon', # 12
    'icon-tab-home',     # 13
    'icon-tab-college',  # 14
    'icon-tab-contact',  # 15
    'icon-tab-mine'      # 16
]

def extract_svgs():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    svgs = re.findall(r'<svg.*?>.*?</svg>', content, re.DOTALL)
    
    saved_files = {}
    
    for i, svg in enumerate(svgs):
        if i < len(icon_classes):
            cls = icon_classes[i]
            # Clean up SVG
            svg_content = re.sub(r'\s+', ' ', svg).strip()
            
            # Save as .svg file (Python environment lacks SVG->PNG libs like cairosvg)
            # We will use .svg extension but user asked for png. 
            # WX supports SVG in image src. We will explain this limitation.
            filename = f"{cls}.svg"
            filepath = os.path.join(ASSETS_DIR, filename)
            
            # Ensure SVG has xmlns if missing
            if 'xmlns=' not in svg_content:
                svg_content = svg_content.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(svg_content)
                
            saved_files[cls] = f"/pages/demo/assets/{filename}"
            print(f"Saved {filepath}")
            
    return saved_files

def update_wxml(mapping):
    with open(WXML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = content
    
    # Iterate over mapping and replace view with image
    # Pattern: <view class="icon-class"></view>  -> <image class="icon-class" src="/path/to/icon.svg"></image>
    # Note: Regex needs to be careful about attributes order, but here we generated the WXML so it's consistent.
    # The generated WXML is like: <view class="icon-signal"></view>
    
    for cls, path in mapping.items():
        # Handle cases where class might be combined or have spaces
        # Simple replacement for exact match of the tag we generated
        
        # Search for <view class="... cls ..."></view> or just <view class="cls"></view>
        # Our previous generation was strict: <view class="cls"></view>
        
        # Regex to match the view tag with this class
        # We need to capture the indentation or surrounding context to be safe? 
        # Or just global replace specific strings.
        
        old_tag = f'<view class="{cls}"></view>'
        new_tag = f'<image class="{cls}" src="{path}" mode="aspectFit"></image>'
        
        if old_tag in new_content:
            new_content = new_content.replace(old_tag, new_tag)
        else:
            # Try searching with potential extra spaces or inside other classes?
            # In our case, they are mostly standalone.
            # But let's try a regex for robustness
            pattern = f'<view class="{cls}"></view>' 
            new_content = re.sub(pattern, new_tag, new_content)

    with open(WXML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated WXML")

def update_wxss(mapping):
    with open(WXSS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove the Base64 background images
    # We generated them at the end of the file in a block.
    # We can just clear the background-image properties for these classes.
    
    new_content = content
    
    # Remove "/* Generated Icon Styles (Base64) */" and everything after if it exists
    if "/* Generated Icon Styles (Base64) */" in new_content:
         parts = new_content.split("/* Generated Icon Styles (Base64) */")
         base_css = parts[0]
         # We still need the width/height for these classes!
         # The previous script generated width/height AND background-image.
         # We need to keep width/height but remove background-image.
         
         # Let's regenerate the CSS part for icons, but without background-image.
         # Or we can just parse the file.
         pass
    
    # Simpler approach: Rewrite the icon CSS block
    # We need to know the width/height again.
    
    # Re-read HTML to get dims (reusing logic is better)
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    svgs = re.findall(r'<svg.*?>.*?</svg>', html_content, re.DOTALL)
    
    extra_css = "\n/* Icon Dimensions */\n"
    
    for i, svg in enumerate(svgs):
        if i < len(icon_classes):
            cls = icon_classes[i]
            # Get dims
            w_match = re.search(r'width="(\d+)"', svg)
            h_match = re.search(r'height="(\d+)"', svg)
            w = int(w_match.group(1)) if w_match else 0
            h = int(h_match.group(1)) if h_match else 0
            
            # Write CSS rule
            # Only width and height needed, image tag handles display
            # But we might need display: block? Image is inline-block by default.
            
            if cls == 'ai-btn-icon' or cls == 'card-service-icon':
                # These might already have styles in the original CSS part?
                # Check if we need to override or append.
                # In previous run, we appended.
                pass
            
            extra_css += f"""
.{cls} {{
    width: {w*2}rpx;
    height: {h*2}rpx;
}}
"""
    
    # If we split by "/* Generated Icon Styles (Base64) */", we can replace the second part with new CSS
    if "/* Generated Icon Styles (Base64) */" in content:
        parts = content.split("/* Generated Icon Styles (Base64) */")
        new_content = parts[0] + extra_css
    elif "/* Generated Icon Styles */" in content: # Fallback for first version
        parts = content.split("/* Generated Icon Styles */")
        new_content = parts[0] + extra_css
    else:
        new_content += extra_css
        
    with open(WXSS_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated WXSS")

if __name__ == '__main__':
    mapping = extract_svgs()
    update_wxml(mapping)
    update_wxss(mapping)
