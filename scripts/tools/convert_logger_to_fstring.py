"""
Conservative converter: replace common `logger.info("...%s...", var)` and
`logger.info("text", var)` patterns with f-strings.

Backs up each modified file to `<file>.bak`.

Note: This script avoids touching calls with >1 non-literal args or multiple %s
in a single format string. It prints a summary of modified files.
"""

from pathlib import Path
import re
import sys

EXCLUDE_DIRS = {".venv", "env", "__pycache__", "node_modules"}

# Pattern A: single %s in a string literal followed by a single arg
pattern_percent_s = re.compile(
    r"(logger\.info\(\s*)([uUrR]?[\'\"](?:[^\\\n\\\"]|\\.)*%s(?:[^\\\n\\\"]|\\.)*[\'\"])\s*,\s*([^,)]+)\s*\)"
)

# Pattern B: string literal followed by a single arg (no %s in literal)
pattern_literal_comma_arg = re.compile(
    r"(logger\.info\(\s*)([uUrR]?[\'\"](?:[^\\\n\\\"]|\\.)*[\'\"])\s*,\s*([^,)\n]+)\s*\)"
)

changed_files = []


def should_skip(path: Path):
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def convert_content(content: str):
    changed = False

    def repl_percent(match):
        prefix, literal, var = match.groups()
        # Count %s occurrences in literal
        cnt = literal.count("%s")
        if cnt != 1:
            return match.group(0)  # skip
        # remove surrounding quotes from literal
        quote = literal[0]
        inner = literal[1:-1]
        # Escape braces if any exist in the inner string
        inner = inner.replace("{", "{{").replace("}", "}}")
        # replace %s with {var}
        new_inner = inner.replace("%s", "{" + var.strip() + "}")
        new = f"{prefix}f{quote}{new_inner}{quote})"
        return new

    def repl_literal_comma(match):
        prefix, literal, var = match.groups()
        inner = literal[1:-1]
        # If literal already contains formatting placeholders like {} or %s, skip
        if "%s" in inner or "{" in inner or "}" in inner:
            return match.group(0)
        # Escape braces
        inner = inner.replace("{", "{{").replace("}", "}}")
        new_inner = inner + "{" + var.strip() + "}"
        quote = literal[0]
        new = f"{prefix}f{quote}{new_inner}{quote})"
        return new

    # First convert %s cases
    new_content, n1 = pattern_percent_s.subn(repl_percent, content)
    content = new_content
    # Then convert literal, arg cases (but avoid those we already changed)
    new_content, n2 = pattern_literal_comma_arg.subn(
        repl_literal_comma, content
    )
    content = new_content

    changed = (n1 + n2) > 0
    return content, changed, n1 + n2


if __name__ == "__main__":
    root = Path(".").resolve()
    py_files = list(root.rglob("*.py"))
    total_changes = 0
    for p in py_files:
        if should_skip(p):
            continue
        # skip this converter script
        if p.name == Path(__file__).name:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        new_text, changed, count = convert_content(text)
        if changed:
            bak = p.with_suffix(p.suffix + ".bak")
            # ensure unique backup filename if one already exists
            i = 0
            candidate = bak
            while candidate.exists():
                i += 1
                candidate = p.with_suffix(p.suffix + f".bak{i}")
            bak = candidate
            p.rename(bak)  # move original to unique .bak
            p.write_text(new_text, encoding="utf-8")
            changed_files.append((str(p), count))
            total_changes += count
            print(f"Modified {p} ({count} replacements) -> backup at {bak}")

    print("\nSummary:")
    print(f"Modified files: {len(changed_files)}")
    print(f"Total replacements: {total_changes}")
    for fn, c in changed_files:
        print(f" - {fn}: {c}")
    if not changed_files:
        print("No changes made.")
    # exit code 0
    sys.exit(0)
