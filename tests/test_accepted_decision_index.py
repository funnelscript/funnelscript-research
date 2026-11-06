"""Fail closed when the research-owned accepted decision index drifts."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROW = re.compile(
    r"^\| \*\*(DEC-\d{3})\*\* \| \[[^\]]+\]\(#[^)]+\) "
    r"\| \d{4}-\d{2}-\d{2} \| \*\*Accepted\*\* \| [^|]+\|$"
)
DETAIL = re.compile(r"^### (DEC-\d{3}): .+$", re.MULTILINE)


def accepted_index_size(body: str) -> int:
    try:
        index = body.split("## Decision Index", 1)[1].split(
            "## Detailed Architecture Decision Records", 1
        )[0]
        details = body.split("## Detailed Architecture Decision Records", 1)[1]
    except IndexError as exc:
        raise ValueError("decision index or detail section missing") from exc

    rows = [line for line in index.splitlines() if line.startswith("| **DEC-")]
    if not rows:
        raise ValueError("accepted decision index is empty")

    indexed = []
    for row in rows:
        match = ROW.fullmatch(row)
        if match is None:
            raise ValueError(f"invalid accepted index row: {row}")
        indexed.append(match.group(1))

    detailed = DETAIL.findall(details)
    if len(indexed) != len(set(indexed)):
        raise ValueError("duplicate indexed decision")
    if len(detailed) != len(set(detailed)):
        raise ValueError("duplicate detailed decision")
    if set(indexed) != set(detailed):
        raise ValueError(
            f"unindexed details: {sorted(set(detailed) - set(indexed))}; "
            f"missing details: {sorted(set(indexed) - set(detailed))}"
        )
    return len(indexed)


class AcceptedDecisionIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = (ROOT / "DECISIONS.md").read_text(encoding="utf-8")
        cls.first_row = next(
            line for line in cls.body.splitlines() if line.startswith("| **DEC-")
        )

    def test_canonical_index_and_details_match(self):
        self.assertGreater(accepted_index_size(self.body), 0)

    def test_removed_index_row_is_rejected(self):
        mutated = self.body.replace(self.first_row + "\n", "", 1)
        with self.assertRaisesRegex(ValueError, "unindexed details"):
            accepted_index_size(mutated)

    def test_duplicate_index_row_is_rejected(self):
        mutated = self.body.replace(self.first_row, self.first_row + "\n" + self.first_row, 1)
        with self.assertRaisesRegex(ValueError, "duplicate indexed"):
            accepted_index_size(mutated)

    def test_proposed_entry_cannot_enter_accepted_index(self):
        mutated = self.body.replace(self.first_row, self.first_row.replace("**Accepted**", "**Proposed**"), 1)
        with self.assertRaisesRegex(ValueError, "invalid accepted index"):
            accepted_index_size(mutated)

    def test_duplicate_detail_is_rejected(self):
        first_detail = DETAIL.search(self.body)
        self.assertIsNotNone(first_detail)
        mutated = self.body + "\n" + first_detail.group(0) + "\n"
        with self.assertRaisesRegex(ValueError, "duplicate detailed"):
            accepted_index_size(mutated)


if __name__ == "__main__":
    unittest.main()
