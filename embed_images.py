"""
Embeds the images referenced in index.html directly into the file (base64),
so the page no longer depends on the Lovable site for its pictures.

Usage (needs internet access, Python 3):
    python embed_images.py                 # images only
    python embed_images.py --video         # images + clinic video (makes the file large)

Put this next to index.html. Output: index-embedded.html
"""
import base64, re, sys, urllib.request

SRC, OUT = "index.html", "index-embedded.html"
include_video = "--video" in sys.argv

html = open(SRC, encoding="utf-8").read()

pattern = r"https://happy-mouth-intro\.lovable\.app/__l5e/assets-v1/[^\s\"')]+"
urls = sorted(set(re.findall(pattern, html)))

mime_by_ext = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".mp4": "video/mp4",
}

for url in urls:
    ext = "." + url.rsplit(".", 1)[-1].lower()
    if ext == ".mp4" and not include_video:
        print("skipped (video):", url)
        continue
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=60).read()
    b64 = base64.b64encode(data).decode()
    html = html.replace(url, f"data:{mime_by_ext.get(ext, 'application/octet-stream')};base64,{b64}")
    print(f"embedded {len(data)//1024} KB:", url)

open(OUT, "w", encoding="utf-8").write(html)
print("Done ->", OUT)
