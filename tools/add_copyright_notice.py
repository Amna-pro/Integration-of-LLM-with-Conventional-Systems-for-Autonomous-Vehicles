from pathlib import Path
import re
import sys

ROOT = Path.cwd()
README = ROOT / "README.md"
COPYRIGHT = ROOT / "COPYRIGHT.md"

copyright_text = """# Copyright

Copyright © 2026 Amna Mahmood. All rights reserved.

This repository, including the thesis document, LaTeX source files, original figures, diagrams, documentation, and other original material created by the author, is provided for academic review and portfolio purposes.

No original material in this repository may be copied, modified, redistributed, republished, or used commercially without prior written permission from the copyright holder, except where permitted by applicable law.

Third party material, trademarks, logos, referenced works, datasets, software, and other externally sourced content remain subject to the rights and terms of their respective owners.

For permission requests, contact the repository owner through GitHub.
"""

footer = """## Copyright

Copyright © 2026 **Amna Mahmood**. All rights reserved.

This repository is shared for academic review and portfolio purposes. See [COPYRIGHT.md](COPYRIGHT.md) for details.
"""

def main():
    if not README.exists():
        print("ERROR: README.md was not found in the current folder.")
        sys.exit(1)

    COPYRIGHT.write_text(copyright_text, encoding="utf-8", newline="\n")

    text = README.read_text(encoding="utf-8", errors="replace")

    # Remove an older copyright section if this script is re-run.
    text = re.sub(
        r'\n## Copyright\n.*?(?=\n## |\Z)',
        '\n',
        text,
        flags=re.DOTALL
    ).rstrip()

    # Put copyright above the final centered footer if present.
    marker = '<p align="center"><sub>Research repository prepared for clear review, reproducibility, and portfolio presentation.</sub></p>'
    if marker in text:
        text = text.replace(marker, footer + "\n\n---\n\n" + marker)
    else:
        text += "\n\n" + footer

    README.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")

    print("Created COPYRIGHT.md")
    print("Updated README.md with a copyright section")
    print("\nNext run:")
    print("  git diff -- README.md COPYRIGHT.md")
    print("  git add README.md COPYRIGHT.md")
    print('  git commit -m "Add copyright notice"')
    print("  git push")

if __name__ == "__main__":
    main()
