"""Check navigation integrity of user-facing research documentation."""

from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOC_DIRS = ("docs", "spec", "evals", "paper")
LINKS = re.compile(r"\]\(([^)]+)\)")


def documentation_files():
    roots = (ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "DECISIONS.md",
             ROOT / "DEBATES.md", ROOT / "OUT_OF_THE_BOX.md")
    return (*roots, *(path for name in DOC_DIRS for path in sorted((ROOT / name).glob("*.md"))))


class DocumentationLinksTest(unittest.TestCase):
    def test_local_links_resolve_within_repository(self):
        examined = 0
        for document in documentation_files():
            for line_number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), 1):
                for raw_target in LINKS.findall(line):
                    target = raw_target.split(" ", 1)[0]
                    parsed = urlsplit(target)
                    if parsed.scheme or target.startswith("#"):
                        continue
                    examined += 1
                    destination = (document.parent / unquote(parsed.path)).resolve()
                    with self.subTest(document=document.relative_to(ROOT), line=line_number, link=target):
                        self.assertTrue(destination.is_relative_to(ROOT), "Link escapes research repository")
                        self.assertTrue(destination.is_file(), f"Missing target: {destination}")
        self.assertGreaterEqual(examined, 20, "Link extractor found too few local references")


if __name__ == "__main__":
    unittest.main()
