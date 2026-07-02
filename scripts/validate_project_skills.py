#!/usr/bin/env python3

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
NAME_RE = re.compile(r"^[a-z0-9-]{1,63}$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("unterminated YAML frontmatter")
    meta: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        if not raw.strip():
            continue
        if ":" not in raw:
            raise ValueError(f"bad frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    skill_file = path / "SKILL.md"
    if not skill_file.exists():
        return ["missing SKILL.md"]
    try:
        text = skill_file.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
    except Exception as exc:  # noqa: BLE001 - script reports all validation errors
        return [str(exc)]
    name = meta.get("name", "")
    desc = meta.get("description", "")
    if name != path.name:
        errors.append(f"name {name!r} does not match folder {path.name!r}")
    if not NAME_RE.match(name):
        errors.append(f"invalid name {name!r}")
    if len(desc) < 30:
        errors.append("description too short")
    if "TODO" in text:
        errors.append("contains TODO placeholder")
    return errors


def main() -> int:
    if not SKILLS.exists():
        print(f"missing {SKILLS.relative_to(ROOT)}", file=sys.stderr)
        return 1
    failed = False
    for path in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        errors = validate_skill(path)
        if errors:
            failed = True
            print(f"[skill] FAIL {path.name}: {'; '.join(errors)}")
        else:
            print(f"[skill] OK {path.name}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
