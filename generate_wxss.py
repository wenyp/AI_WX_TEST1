
import re
import urllib.parse

def px_to_rpx(match):
    px_val = float(match.group(1))
    return f"{px_val * 2}rpx"

def get_svg_data_uri(svg_content):
    # Clean up SVG
    svg_content = re.sub(r'\s+', ' ', svg_content).strip()
    encoded = urllib.parse.quote(svg_content)
    return f"url('data:image/svg+xml;utf8,{encoded}')"

with open('demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract Style
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if style_match:
    css_content = style_match.group(1)
    # Convert px to rpx
    wxss_content = re.sub(r'(\d+(\.\d+)?)px', px_to_rpx, css_content)
    
    # Fix body -> page
    wxss_content = wxss_content.replace('body {', 'page {')
    
    # Remove container fixed size and relative positioning if needed, 
    # but for now let's keep it as the design relies on absolute positioning.
    # However, page { height: 100% } might be needed.
    
else:
    wxss_content = ""

# Extract SVGs and map to classes
# This part requires manual mapping based on the order found in HTML
svgs = re.findall(r'<svg.*?>.*?</svg>', content, re.DOTALL)

# Defined classes order based on my analysis
icon_classes = [
    'icon-signal',       # 0
    'icon-battery',      # 1
    'icon-back',         # 2
    'icon-more',         # 3
    'icon-close',        # 4
    'ai-btn-icon',       # 5 (Note: this class existed in CSS but used as container, now we need to apply bg to inner div or the div itself if empty)
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

extra_css = ""

# Helper to get dimensions from svg tag
def get_dims(svg_str):
    w_match = re.search(r'width="(\d+)"', svg_str)
    h_match = re.search(r'height="(\d+)"', svg_str)
    w = int(w_match.group(1)) if w_match else 0
    h = int(h_match.group(1)) if h_match else 0
    return w, h

for i, svg in enumerate(svgs):
    if i < len(icon_classes):
        cls = icon_classes[i]
        uri = get_svg_data_uri(svg)
        w, h = get_dims(svg)
        
        # Special handling for existing classes vs new icon classes
        if cls == 'ai-btn-icon':
             # The CSS already has .ai-btn-icon, we just need to add background image and no-repeat
             extra_css += f"""
.{cls} {{
    background-image: {uri};
    background-repeat: no-repeat;
    background-size: 100% 100%;
    /* width/height already in CSS? Check later. If not, add them. */
}}
"""
        elif cls == 'card-service-icon':
             extra_css += f"""
.{cls} {{
    background-image: {uri};
    background-repeat: no-repeat;
    background-size: 100% 100%;
}}
"""
        else:
            # New classes
            extra_css += f"""
.{cls} {{
    width: {w*2}rpx;
    height: {h*2}rpx;
    background-image: {uri};
    background-repeat: no-repeat;
    background-size: 100% 100%;
}}
"""

# Append extra CSS
wxss_content += "\n/* Generated Icon Styles */\n" + extra_css

# Write to file
with open('pages/demo/demo.wxss', 'w', encoding='utf-8') as f:
    f.write(wxss_content)

print("WXSS generated successfully.")
