# 📸 OLX Ad Downloader

A robust Python tool that automatically downloads high-resolution images and the description from an OLX advertisement.

It organizes files into a clean folder in your `Downloads` directory, named directly from the ad's URL, and optionally converts images to JPG format.

## 🚀 Features

* **Smart Folder Naming:** Extracts the exact item name from the URL (e.g., creates `macbook-air-2020` instead of random characters).
* **Description Scraping:** Saves the ad title and full description into a `data.txt` file within the folder.
* **Full Resolution:** Automatically strips resizing parameters to download the highest quality images available.
* **Auto-Conversion to JPG:** If the `Pillow` library is installed, it converts WebP/PNG files to standard JPG automatically.
* **Deep Scan:** Uses a "nuclear" regex method to find images even if OLX tries to hide them or uses lazy loading.

## 🛠️ Prerequisites & Installation

You need **Python 3** installed.

### 1. Save the script
Save the code as `photos.py`.

### 2. Install dependencies
Open your terminal and run the following command:

**For macOS (if you see "externally-managed-environment" error):**
```bash
pip3 install requests beautifulsoup4 pillow --break-system-packages
```

For Windows / Linux:

```bash
pip install requests beautifulsoup4 pillow
```
(Note: The `pillow` library is optional. If you don't install it, the script will still work but won't convert images to JPG).

▶️ Usage
Open your terminal in the folder where `photos.py` is saved.

Run the script:
```bash
python3 photos.py
```
Paste the OLX Ad URL when prompted and press Enter.

Example
Input:

```Plaintext
Paste OLX Ad URL: [https://www.olx.pl/d/oferta/piekny-rower-szosowy-CID767-IDMn3.html](https://www.olx.pl/d/oferta/piekny-rower-szosowy-CID767-IDMn3.html)
```

Output:
```Plaintext
Plaintext

Connecting to: [https://www.olx.pl/d/oferta/](https://www.olx.pl/d/oferta/)...
Target Folder: /Users/YourName/Downloads/piekny-rower-szosowy
Found 8 potential images.
Saved description to: data.txt

Starting Download...
Saved: image_1.webp
Saved: image_2.webp
...

--- Converting images to JPG ---
Converted: image_1.webp -> image_1.jpg
SUCCESS! Saved in: /Users/YourName/Downloads/piekny-rower-szosowy
```

📂 Output Structure
Inside your Downloads folder, you will find:

```Plaintext

📁 piekny-rower-szosowy/
├── 📄 data.txt        <-- Ad Title and Description
├── 🖼️ image_1.jpg     <-- Photo 1
├── 🖼️ image_2.jpg     <-- Photo 2
└── ...
```
❓ Troubleshooting
`ModuleNotFoundError`: You haven't installed the required libraries. See the Installation section.

Images look like blank icons: The script downloaded them, but couldn't convert them to JPG (missing Pillow). They are still valid files; you can open them in a browser or install Pillow to fix the icons.

Folder named `olx_download`: The script couldn't parse a clean name from the URL (e.g., the link format was unusual). This is the default fallback.
