from pathlib import Path
import fitz
import re
import sys

ROOT = Path.cwd()
SOURCE = ROOT / "Amna_MAhmood_final_Thesis.pdf"
OUTPUT = ROOT / "Amna_MAhmood_final_Thesis_Web.pdf"
README = ROOT / "README.md"

TARGET_MB = 12.0
PROFILES = [
    (110, 55),
    (96, 50),
    (84, 46),
]

def size_mb(path):
    return path.stat().st_size / (1024 * 1024)

def build_web_pdf(dpi, quality):
    temp = ROOT / f".thesis_web_{dpi}_{quality}.pdf"
    if temp.exists():
        temp.unlink()

    src = fitz.open(SOURCE)
    dst = fitz.open()

    total = len(src)
    for i, page in enumerate(src):
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        jpg = pix.tobytes("jpeg", jpg_quality=quality)

        new_page = dst.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(new_page.rect, stream=jpg)

        if (i + 1) % 10 == 0 or i + 1 == total:
            print(f"Processed {i + 1}/{total} pages")

    dst.save(temp, garbage=4, deflate=True, clean=True)
    dst.close()
    src.close()
    return temp

def update_readme():
    text = README.read_text(encoding="utf-8", errors="replace")

    pattern = re.compile(
        r'<a href="[^"]*Amna_MAhmood_final_Thesis(?:_Web)?\.pdf"><b>[^<]*Read[^<]*Thesis[^<]*</b></a>',
        re.IGNORECASE,
    )

    replacement = '<a href="Amna_MAhmood_final_Thesis_Web.pdf"><b>Read the Full Thesis</b></a>'

    if pattern.search(text):
        text = pattern.sub(replacement, text, count=1)
    else:
        old_raw = re.compile(
            r'<a href="https://raw\.githubusercontent\.com/[^"]+Amna_MAhmood_final_Thesis\.pdf"><b>Read the Full Thesis</b></a>',
            re.IGNORECASE,
        )
        if old_raw.search(text):
            text = old_raw.sub(replacement, text, count=1)
        else:
            print("WARNING: Could not find the thesis link in README.md automatically.")
            return

    README.write_text(text, encoding="utf-8", newline="\n")
    print("README.md updated to use only the web PDF link.")

def main():
    if not SOURCE.exists():
        print(f"ERROR: {SOURCE.name} not found.")
        sys.exit(1)

    if not README.exists():
        print("ERROR: README.md not found.")
        sys.exit(1)

    print(f"Source PDF size: {size_mb(SOURCE):.2f} MB")

    chosen = None

    for dpi, quality in PROFILES:
        print(f"\nCreating web PDF at {dpi} DPI, quality {quality}...")
        temp = build_web_pdf(dpi, quality)
        mb = size_mb(temp)
        print(f"Result size: {mb:.2f} MB")

        if chosen and chosen.exists():
            chosen.unlink()

        chosen = temp

        if mb <= TARGET_MB:
            break

    if OUTPUT.exists():
        OUTPUT.unlink()

    chosen.replace(OUTPUT)

    print(f"\nCreated {OUTPUT.name}")
    print(f"Web PDF size: {size_mb(OUTPUT):.2f} MB")
    print("Original thesis PDF remains unchanged.")

    update_readme()

    print("\nNext commands:")
    print("git add README.md Amna_MAhmood_final_Thesis_Web.pdf")
    print('git commit -m "Add browser friendly thesis PDF"')
    print("git push")

if __name__ == "__main__":
    main()
