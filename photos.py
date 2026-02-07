import os
import time
import re
import requests
import mimetypes
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Try to import Pillow for JPG conversion. 
try:
    from PIL import Image
except ImportError:
    print("Note: Pillow library not found. Images will be saved in original format.")

# CONFIGURATION
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

def clean_filename(title):
    return re.sub(r'[^\w\s-]', '', title).strip()[:100]

def get_name_from_url(url):
    """Extracts folder name from the URL string."""
    try:
        parsed = urlparse(url)
        path = parsed.path 
        filename = path.split('/')[-1]
        
        if filename.endswith('.html'):
            filename = filename[:-5]
            
        if '-CID' in filename:
            filename = filename.split('-CID')[0]
        elif '-ID' in filename:
            filename = filename.split('-ID')[0]
            
        return clean_filename(filename)
    except:
        return "olx_download"

def save_description(soup, folder_path):
    """Scrapes Title and Description using Meta Tags (More Reliable)"""
    try:
        # --- IMPROVED TITLE FINDER ---
        title_text = "No Title Found"
        
        # Method 1: Meta Tag (Best for OLX)
        meta_title = soup.find("meta", property="og:title")
        if meta_title:
            title_text = meta_title.get("content").strip()
            
        # Method 2: H1 Fallback
        if title_text == "No Title Found":
            h1_tag = soup.find('h1')
            if h1_tag:
                title_text = h1_tag.get_text(strip=True)
                
        # Method 3: <title> Tag Fallback
        if title_text == "No Title Found" and soup.title:
            title_text = soup.title.string.replace(" - OLX.pl", "").strip()

        # --- GET DESCRIPTION ---
        desc_div = soup.find('div', {'data-cy': 'ad_description'})
        if desc_div:
            desc_text = desc_div.get_text(separator='\n', strip=True)
        else:
            desc_text = "Description not found."

        # --- SAVE TO FILE ---
        file_path = os.path.join(folder_path, "data.txt")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("TITLE\n")
            f.write(title_text)
            f.write("\n\nDESCRIPTION\n")
            f.write(desc_text)
            
        print(f"Saved description to: data.txt")
        
    except Exception as e:
        print(f"Warning: Could not save description. {e}")

def convert_folder_to_jpg(folder_path):
    print("\n--- Converting images to JPG ---")
    files = os.listdir(folder_path)
    
    for filename in files:
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            continue 
            
        file_path = os.path.join(folder_path, filename)
        if filename == "data.txt": continue # Skip the text file

        new_filename = os.path.splitext(filename)[0] + ".jpg"
        new_file_path = os.path.join(folder_path, new_filename)
        
        try:
            with Image.open(file_path) as img:
                rgb_im = img.convert('RGB')
                rgb_im.save(new_file_path, 'JPEG', quality=95)
            
            os.remove(file_path)
            print(f"Converted: {filename} -> {new_filename}")
        except Exception as e:
            pass

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
    original_url = url
    if '?' in url: url = url.split('?')[0]
    
    print(f"Connecting to: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. Setup Folder
    folder_name = get_name_from_url(original_url)
    if not folder_name or len(folder_name) < 3:
        folder_name = "olx_download"
        
    downloads_path = Path.home() / "Downloads"
    full_path = downloads_path / folder_name

    print(f"Target Folder: {full_path}")

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    # 2. Save Title & Description (Improved)
    save_description(soup, full_path)

    # 3. Extract Images
    image_urls = extract_images_nuclear(response.text)
    print(f"Found {len(image_urls)} potential images.")
    
    # 4. Download
    count = 0
    print("\nStarting Download...")
    
    for i, img_url in enumerate(image_urls):
        try:
            img_response = requests.get(img_url, headers=HEADERS, timeout=10)
            
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

    # 5. Convert
    if count > 0:
        convert_folder_to_jpg(full_path)
        print(f"\nSUCCESS! Saved in:\n{full_path}")

if __name__ == "__main__":
    ad_url = input("Paste OLX Ad URL: ").strip()
    if ad_url:
        download_images(ad_url)
