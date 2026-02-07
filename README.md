# OLX Image Downloader

A simple, robust Python tool that downloads all high-resolution images from an OLX advertisement. It automatically organizes files into a folder named after the ad and converts everything to JPG format.

## 🚀 Features

* **Smart Folder Naming:** Extracts the ad title directly from the URL to name your download folder (e.g., `piekny-laptop-macbook-air`).
* **Full Resolution:** Automatically removes resizing parameters to download the highest quality images available.
* **Format Conversion:** specific `WebP` or `PNG` images are automatically converted to standard `.jpg`.
* **Deep Scan:** Uses a "nuclear" regex method to find images even if OLX tries to hide them or uses lazy loading.
* **Duplicate Prevention:** Checks for duplicates and skips tiny icons/avatars.

## 📋 Prerequisites

* Python 3.x installed.
* An active internet connection.

## 🛠️ Installation

1.  **Download the script:**
    Save the code as `photos.py`.

2.  **Install dependencies:**
    Open your terminal/command prompt and run:

    ```bash
    pip3 install requests pillow
    ```

    **⚠️ Mac User Note:**
    If you see an error saying "externally-managed-environment", use this command instead:
    ```bash
    pip3 install requests pillow --break-system-packages
    ```

## 🏃 Usage

1.  Open your terminal and navigate to the folder where `photos.py` is saved.
2.  Run the script:
    ```bash
    python3 photos.py
    ```
3.  **Paste the OLX Ad URL** when prompted and press Enter.

### Example
**Input:**
```text
Paste OLX Ad URL: [https://www.olx.pl/d/oferta/piekny-laptop-macbook-air-2020-CID99-ID1893gF.html](https://www.olx.pl/d/oferta/piekny-laptop-macbook-air-2020-CID99-ID1893gF.html)
Output:

Plaintext

Connecting to: [https://www.olx.pl/d/oferta/](https://www.olx.pl/d/oferta/)...
Target Folder: /Users/krzys/Downloads/piekny-laptop-macbook-air-2020
Found 8 potential images.

Starting Download...
Saved: image_1.webp
Saved: image_2.webp
...

--- Converting images to JPG ---
Converted: image_1.webp -> image_1.jpg
Converted: image_2.webp -> image_2.jpg

SUCCESS! Images saved to:
/Users/krzys/Downloads/piekny-laptop-macbook-air-2020
❓ Troubleshooting
"ModuleNotFoundError: No module named 'PIL'": You are missing the Pillow library. Run the installation command above again.

"No images found": The ad might be expired, or OLX might be presenting a CAPTCHA. Open the link in a normal browser to verify it works, then try again.

Images are small: The script automatically tries to find the biggest version, but if the original upload was small, it cannot enhance it.
```
📝 Disclaimer
This tool is for educational purposes and personal use only. Please respect OLX's terms of service and robots.txt.
