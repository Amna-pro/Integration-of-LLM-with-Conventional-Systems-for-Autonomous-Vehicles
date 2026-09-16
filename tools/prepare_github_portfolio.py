from pathlib import Path
from urllib.parse import quote
import re
import sys

ROOT = Path.cwd()
IMAGES = ROOT / "Images"
PREVIEWS = ROOT / "docs" / "previews"
THESIS = ROOT / "Amna_MAhmood_final_Thesis.pdf"
README = ROOT / "README.md"
GITIGNORE = ROOT / ".gitignore"

RASTER_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
PDF_EXT = ".pdf"

def natural_key(text):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", str(text))]

def url_path(path):
    rel = path.relative_to(ROOT).as_posix()
    return quote(rel, safe="/")

def title_from_name(path):
    name = path.stem.replace("_", " ").strip()
    name = re.sub(r"\s+", " ", name)
    return name

def render_pdf_preview(pdf_path, out_path):
    try:
        import fitz
    except ImportError:
        print("\nERROR: PyMuPDF is not installed.")
        print("Run: py -m pip install pymupdf")
        sys.exit(1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    if len(doc) == 0:
        doc.close()
        return False

    page = doc[0]
    rect = page.rect
    max_dim = max(rect.width, rect.height)
    scale = min(2.0, 1400.0 / max_dim) if max_dim else 1.5
    matrix = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    pix.save(out_path)
    doc.close()
    return True

def collect_chapter_media():
    chapters = []
    for chapter_dir in sorted(
        [p for p in IMAGES.iterdir() if p.is_dir()],
        key=lambda p: natural_key(p.name)
    ):
        items = []
        for p in sorted(
            [x for x in chapter_dir.iterdir() if x.is_file()],
            key=lambda x: natural_key(x.name)
        ):
            ext = p.suffix.lower()
            if ext in RASTER_EXTS:
                items.append({
                    "source": p,
                    "preview": p,
                    "kind": "image",
                })
            elif ext == PDF_EXT:
                preview = PREVIEWS / chapter_dir.name / f"{p.stem}.png"
                if not preview.exists() or preview.stat().st_mtime < p.stat().st_mtime:
                    print(f"Rendering preview: {p.relative_to(ROOT)}")
                    render_pdf_preview(p, preview)
                items.append({
                    "source": p,
                    "preview": preview,
                    "kind": "pdf",
                })
        chapters.append((chapter_dir.name, items))
    return chapters

def make_gallery_table(items):
    if not items:
        return "_No figures found in this chapter._\n"

    cells = []
    for item in items:
        source = item["source"]
        preview = item["preview"]
        title = title_from_name(source)
        source_url = url_path(source)
        preview_url = url_path(preview)
        source_label = "Open original PDF" if item["kind"] == "pdf" else "Open full image"
        cell = (
            f'<td align="center" width="50%">'
            f'<a href="{source_url}">'
            f'<img src="{preview_url}" alt="{title}" width="100%"></a>'
            f'<br><sub><b>{title}</b></sub>'
            f'<br><sub><a href="{source_url}">{source_label}</a></sub>'
            f'</td>'
        )
        cells.append(cell)

    rows = []
    for i in range(0, len(cells), 2):
        row_cells = cells[i:i+2]
        if len(row_cells) == 1:
            row_cells.append('<td width="50%"></td>')
        rows.append("<tr>" + "".join(row_cells) + "</tr>")

    return "<table>\n" + "\n".join(rows) + "\n</table>\n"

def write_gitignore():
    content = r"""# LaTeX build artifacts
*.aux
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz
*.toc
*.lof
*.lot
*.nav
*.snm
*.vrb
*.xdv
*.bcf
*.run.xml

# Editor and OS files
.vscode/
.idea/
.DS_Store
Thumbs.db
desktop.ini

# Python cache
__pycache__/
*.pyc
"""
    GITIGNORE.write_text(content, encoding="utf-8")

def build_readme(chapters):
    all_items = [item for _, items in chapters for item in items]
    pdf_count = sum(1 for item in all_items if item["kind"] == "pdf")
    image_count = len(all_items) - pdf_count

    featured = []
    for preferred in ("CH_3", "CH_4", "CH_5", "CH_6"):
        chapter_items = next((items for name, items in chapters if name == preferred), [])
        if chapter_items:
            featured.append(chapter_items[0])
    featured = featured[:4]

    lines = []
    lines.append('<p align="center">')
    if (ROOT / "nust-logo.png").exists():
        lines.append('  <img src="nust-logo.png" alt="NUST Logo" width="115">')
    lines.append('</p>')
    lines.append("")
    lines.append('<h1 align="center">Integration of LLMs with Conventional Systems for Autonomous Vehicles</h1>')
    lines.append("")
    lines.append('<p align="center">')
    lines.append("  A thesis repository presenting the integration of Large Language Models with conventional control approaches for autonomous vehicle systems.")
    lines.append("</p>")
    lines.append("")
    lines.append('<p align="center">')
    lines.append('  <img src="https://img.shields.io/badge/Research-Thesis-6f42c1" alt="Research Thesis">')
    lines.append('  <img src="https://img.shields.io/badge/Domain-Autonomous%20Vehicles-0969da" alt="Autonomous Vehicles">')
    lines.append('  <img src="https://img.shields.io/badge/AI-Large%20Language%20Models-238636" alt="Large Language Models">')
    lines.append('  <img src="https://img.shields.io/badge/Source-LaTeX-b31b1b" alt="LaTeX">')
    lines.append("</p>")
    lines.append("")
    if THESIS.exists():
        lines.append('<p align="center">')
        lines.append('  <a href="Amna_MAhmood_final_Thesis.pdf"><b>Read the Full Thesis</b></a>')
        lines.append("</p>")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Project Overview")
    lines.append("")
    lines.append(
        "This repository contains the complete thesis source, references, figures, diagrams, experimental visualizations, "
        "and final thesis PDF for the project. The visual material is organized chapter by chapter so the work can be reviewed directly from GitHub."
    )
    lines.append("")
    lines.append("## Repository Contents")
    lines.append("")
    lines.append("| Item | Description |")
    lines.append("| --- | --- |")
    lines.append("| `main.tex` | Main LaTeX thesis source |")
    lines.append("| `first.tex` | Supporting LaTeX source |")
    lines.append("| `mybib.bib` | Bibliography database |")
    lines.append("| `Images/` | Original chapter figures and diagrams |")
    lines.append("| `docs/previews/` | GitHub friendly PNG previews generated from PDF figures |")
    lines.append("| `Amna_MAhmood_final_Thesis.pdf` | Final thesis document |")
    lines.append("")
    lines.append("## Visual Summary")
    lines.append("")
    lines.append(
        f"The repository currently contains **{len(all_items)} visual assets** across six chapters, "
        f"including **{image_count} raster images** and **{pdf_count} PDF figures**. "
        "PDF figures are preserved in their original form and also rendered as PNG previews for GitHub."
    )
    lines.append("")
    if featured:
        lines.append("### Selected Visuals")
        lines.append("")
        lines.append(make_gallery_table(featured))
    lines.append("## Complete Figure Gallery")
    lines.append("")
    lines.append(
        "Every chapter figure is available below. Click any preview to open the original image or PDF."
    )
    lines.append("")

    for chapter_name, items in chapters:
        display_name = chapter_name.replace("_", " ")
        lines.append("<details>")
        lines.append(f"<summary><b>{display_name}</b> &nbsp; • &nbsp; {len(items)} figures</summary>")
        lines.append("")
        lines.append(make_gallery_table(items))
        lines.append("</details>")
        lines.append("")

    lines.append("## Project Structure")
    lines.append("")
    lines.append("```text")
    lines.append("Integration-of-LLM-with-Conventional-Systems-for-Autonomous-Vehicles/")
    lines.append("├── README.md")
    lines.append("├── main.tex")
    lines.append("├── first.tex")
    lines.append("├── mybib.bib")
    lines.append("├── nust-logo.png")
    lines.append("├── Amna_MAhmood_final_Thesis.pdf")
    lines.append("├── Images/")
    lines.append("│   ├── CH_1/")
    lines.append("│   ├── CH_2/")
    lines.append("│   ├── CH_3/")
    lines.append("│   ├── CH_4/")
    lines.append("│   ├── CH_5/")
    lines.append("│   └── CH_6/")
    lines.append("└── docs/")
    lines.append("    └── previews/")
    lines.append("```")
    lines.append("")
    lines.append("## Working With the Thesis")
    lines.append("")
    lines.append(
        "The editable thesis is maintained in LaTeX. Original figures remain inside their chapter folders, "
        "while the generated preview directory exists only to make PDF based figures visible directly in the GitHub README."
    )
    lines.append("")
    lines.append("## Author")
    lines.append("")
    lines.append("**Amna Mahmood**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append('<p align="center"><sub>Research repository prepared for clear review, reproducibility, and portfolio presentation.</sub></p>')
    lines.append("")

    README.write_text("\n".join(lines), encoding="utf-8")

def main():
    if not IMAGES.exists():
        print("ERROR: Images folder was not found.")
        print("Run this script from the thesis project root.")
        sys.exit(1)

    if not (ROOT / ".git").exists():
        print("WARNING: This folder does not appear to be a Git repository.")

    print("Preparing GitHub portfolio...")
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    chapters = collect_chapter_media()
    write_gitignore()
    build_readme(chapters)

    total = sum(len(items) for _, items in chapters)
    print("\nDone.")
    print(f"README.md created with {total} visual assets.")
    print(".gitignore created.")
    print("PDF previews created under docs\\previews.")
    print("\nNext run:")
    print("  git status --short")
    print("  git add .")
    print('  git commit -m "Add thesis project and visual documentation"')
    print("  git push -u origin main")

if __name__ == "__main__":
    main()
