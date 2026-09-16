from pathlib import Path
import shutil
import re
import sys

ROOT = Path.cwd()
SOURCE = ROOT / "Amna_MAhmood_final_Thesis_Web.pdf"
DOCS = ROOT / "docs"
PAGES_PDF = DOCS / "Amna_MAhmood_final_Thesis_Web.pdf"
THESIS_HTML = DOCS / "thesis.html"
INDEX_HTML = DOCS / "index.html"
NOJEKYLL = DOCS / ".nojekyll"
README = ROOT / "README.md"

PAGES_BASE = "https://amna-pro.github.io/Integration-of-LLM-with-Conventional-Systems-for-Autonomous-Vehicles/"
THESIS_URL = PAGES_BASE + "thesis.html"

thesis_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Amna Mahmood | Full Thesis</title>
  <style>
    html, body { margin: 0; height: 100%; background: #f6f8fa; font-family: Arial, sans-serif; }
    .bar {
      box-sizing: border-box;
      min-height: 58px;
      padding: 14px 20px;
      background: #ffffff;
      border-bottom: 1px solid #d0d7de;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .title { font-size: 16px; font-weight: 700; color: #1f2328; }
    .repo {
      color: #0969da;
      text-decoration: none;
      font-size: 14px;
      white-space: nowrap;
    }
    .viewer { height: calc(100vh - 58px); }
    iframe { width: 100%; height: 100%; border: 0; background: white; }
    @media (max-width: 650px) {
      .bar { align-items: flex-start; flex-direction: column; }
      .viewer { height: calc(100vh - 90px); }
    }
  </style>
</head>
<body>
  <div class="bar">
    <div class="title">Integration of LLMs with Conventional Systems for Autonomous Vehicles</div>
    <a class="repo" href="https://github.com/Amna-pro/Integration-of-LLM-with-Conventional-Systems-for-Autonomous-Vehicles">View Repository</a>
  </div>
  <div class="viewer">
    <iframe src="Amna_MAhmood_final_Thesis_Web.pdf" title="Amna Mahmood Full Thesis"></iframe>
  </div>
</body>
</html>
"""

index_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=thesis.html">
  <title>Amna Mahmood Thesis</title>
</head>
<body>
  <p><a href="thesis.html">Open the thesis</a></p>
</body>
</html>
"""

def main():
    if not SOURCE.exists():
        print("ERROR: Amna_MAhmood_final_Thesis_Web.pdf was not found in the repository root.")
        sys.exit(1)
    if not README.exists():
        print("ERROR: README.md was not found.")
        sys.exit(1)

    DOCS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE, PAGES_PDF)
    THESIS_HTML.write_text(thesis_html, encoding="utf-8", newline="\n")
    INDEX_HTML.write_text(index_html, encoding="utf-8", newline="\n")
    NOJEKYLL.touch()

    text = README.read_text(encoding="utf-8", errors="replace")

    patterns = [
        r'href="Amna_MAhmood_final_Thesis_Web\.pdf"',
        r'href="https://raw\.githubusercontent\.com/[^"]*Amna_MAhmood_final_Thesis\.pdf"',
        r'href="Amna_MAhmood_final_Thesis\.pdf"',
    ]
    replaced = False
    for pattern in patterns:
        if re.search(pattern, text):
            text = re.sub(pattern, f'href="{THESIS_URL}"', text, count=1)
            replaced = True
            break

    if not replaced:
        print("WARNING: I could not locate the existing thesis href automatically.")
        print(f"Set the README thesis link to: {THESIS_URL}")
    else:
        README.write_text(text, encoding="utf-8", newline="\n")

    print("GitHub Pages thesis viewer prepared.")
    print(f"Created: {PAGES_PDF.relative_to(ROOT)}")
    print(f"Created: {THESIS_HTML.relative_to(ROOT)}")
    print(f"Created: {INDEX_HTML.relative_to(ROOT)}")
    print(f"Created: {NOJEKYLL.relative_to(ROOT)}")
    if replaced:
        print("README.md updated to point to the GitHub Pages thesis viewer.")
    print("\nNext commands:")
    print("  git add README.md docs")
    print('  git commit -m "Add GitHub Pages thesis viewer"')
    print("  git push")
    print("\nThen on GitHub:")
    print("  Settings > Pages")
    print("  Source: Deploy from a branch")
    print("  Branch: main")
    print("  Folder: /docs")
    print("  Save")
    print(f"\nExpected thesis URL:\n{THESIS_URL}")

if __name__ == "__main__":
    main()
