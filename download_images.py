
import re
import os
import urllib.request
import hashlib

# Configuration
ASSETS_DIR = 'pages/demo/assets'
FILES_TO_PROCESS = [
    'pages/demo/demo.wxml',
    'pages/demo/demo.wxss'
]

def download_image(url):
    try:
        # Generate filename from content hash or url hash to avoid duplicates
        path_parts = os.path.splitext(url)
        if len(path_parts) > 1:
            ext = path_parts[1]
        else:
            ext = '.png'
            
        # Clean extension (remove query params)
        ext = ext.split('?')[0]
        if not ext:
            ext = '.png'
            
        filename = hashlib.md5(url.encode('utf-8')).hexdigest() + ext
        filepath = os.path.join(ASSETS_DIR, filename)
        
        # Use urllib instead of requests
        with urllib.request.urlopen(url) as response:
             data = response.read()
             with open(filepath, 'wb') as f:
                 f.write(data)
        
        return filename
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None
    return None

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find URLs (simple version for http/https)
    # Looking for https://image-resource.mastergo.com...
    urls = re.findall(r'(https?://image-resource\.mastergo\.com/[^"\'\)\s]+)', content)
    
    # Deduplicate
    urls = list(set(urls))
    
    new_content = content
    for url in urls:
        print(f"Processing {url}...")
        filename = download_image(url)
        if filename:
            # Replace with local path
            # Using absolute path from project root for WX consistency
            local_path = f"/pages/demo/assets/{filename}"
            new_content = new_content.replace(url, local_path)
            print(f"  -> Saved to {local_path}")
        else:
            print("  -> Download failed")
            
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"No changes for {filepath}")

if __name__ == '__main__':
    for f in FILES_TO_PROCESS:
        if os.path.exists(f):
            process_file(f)
        else:
            print(f"File not found: {f}")
