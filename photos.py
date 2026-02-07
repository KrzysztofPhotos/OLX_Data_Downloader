import os
import time
import re
import requests
import mimetypes
from pathlib import Path
from urllib.parse import urlparse

# New import for image conversion
try:
    from PIL import Image
except ImportError:
    print("CRITICAL ERROR: You need to install Pillow. Run: pip3 install pillow --break-system-packages")
    exit()

# CONFIGURATION
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
}

def clean_filename(title):
    # Remove dangerous characters but keep the dashes from the URL
    return re.sub(r'[^\w\s-]', '', title).strip()[:100]

def get_name_from_url(url):
    """
    Extracts the ad name directly from the URL link.
    Example: .../oferta/nice-laptop-CID99-ID123.html -> nice-laptop
    """
    try:
        parsed = urlparse(url)
        path = parsed.path # e.g. /d/oferta/piekny-laptop...html
        
        # Get the last part of the path (the filename)
        filename = path.split('/')[-1]
        
        # Remove .html if present
        if filename.endswith('.html'):
            filename = filename[:-5]
            
        # Remove the ID part (starts with -CID or -ID)
        # We split by '-CID' and take the first part
        if '-CID' in filename:
            filename = filename.split('-CID')[0]
        elif '-ID' in filename:
            filename = filename.split('-ID')[0]
            
        return clean_filename(filename)
    except:
        return "olx_download"

def convert_folder_to_jpg(folder_path):
    print("\n--- Converting images to JPG ---")
    files = os.listdir(folder_path)
    
    for filename in files:
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            continue # Already correct
            
        file_path = os.path.join(folder_path, filename)
        new_filename = os.path.splitext(filename)[0] + ".jpg"
        new_file_path = os.path.join(folder_path, new_filename)
        
        try:
            # Open image
            with Image.open(file_path) as img:
                # Convert to RGB (Required for JPG)
                rgb_im = img.convert('RGB')
                rgb_im.save(new_file_path, 'JPEG', quality=95)
            
            # Remove the old file to keep folder clean
            os.remove(file_path)
            print(f"Converted: {filename} -> {new_filename}")
            
        except Exception as e:
            print(f"Could not convert {filename}: {e}")

def extract_images_nuclear(html_text):
    clean_html = html_text.replace(r'\/', '/')
    pattern = r'(https?://[^\s"\'<>]+olxcdn\.com[^\s"\'<>]*)'
    matches = re.findall(pattern, clean_html)
    
    valid_images = []
    for url in matches:
        if '/v1/files/' not in url: continue
        if ';s=' in url: url = url.split(';s=')[0]
        if '?' in url: url = url.split('?')[0]
        if 'icon' in url or 'avatar' in url: continue
        valid_images.append(url)
            
    return list(set(valid_images))

def download_images(url):
    # Strip query params for clean processing
    original_url = url
    if '?' in url: url = url.split('?')[0]
    
    print(f"Connecting to: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error: {e}")
        return

    # 1. Setup Folder (FROM URL NOW)
    folder_name = get_name_from_url(original_url)
    
    # Fallback if URL parsing failed mostly
    if not folder_name or len(folder_name) < 3:
        folder_name = "olx_download"
        
    downloads_path = Path.home() / "Downloads"
    full_path = downloads_path / folder_name

    print(f"Target Folder: {full_path}")

    # 2. Extract Images
    image_urls = extract_images_nuclear(response.text)
    print(f"Found {len(image_urls)} potential images.")

    if not os.path.exists(full_path):
        os.makedirs(full_path)
    
    # 3. Download
    count = 0
    print("\nStarting Download...")
    
    for i, img_url in enumerate(image_urls):
        try:
            # Get content
            img_response = requests.get(img_url, headers=HEADERS, timeout=10)
            
            # Guess extension for temporary save
            content_type = img_response.headers.get('Content-Type', '').lower()
            ext = mimetypes.guess_extension(content_type) or ".jpg"
            if ext == '.jpe': ext = '.jpg'
            
            filename = f"image_{i+1}{ext}"
            file_path = full_path / filename

            with open(file_path, 'wb') as f:
                f.write(img_response.content)
            
            print(f"Saved: {filename}")
            count += 1
            time.sleep(0.2)

        except Exception as e:
            print(f"Failed: {e}")

    # 4. Convert all to JPG
    if count > 0:
        convert_folder_to_jpg(full_path)
        print(f"\nSUCCESS! Images saved to:\n{full_path}")

if __name__ == "__main__":
    ad_url = input("Paste OLX Ad URL: ").strip()
    if ad_url:
        download_images(ad_url)
