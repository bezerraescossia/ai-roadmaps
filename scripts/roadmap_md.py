"""Parse and edit a spec-kit-format roadmap.md. Stdlib only.

Entries are `### NNN — Title  [status: x]` under `## Planned Specs`; fields are `- **Name:** value`
lines, optionally followed by indented continuation lines.
"""
import datetime
import re
from dataclasses import dataclass, field

ENTRY = re.compile(r"^### (\d{3}) [—-] (.+?)\s+\[status: ([\w-]+)\]\s*$")
FIELD = re.compile(r"^- \*\*([^:*]+):\*\*\s*(.*)$")
QUESTION = re.compile(r"^- (Q\d+) [—-] (.*)$")
FOOTER = re.compile(r"(\*\*Version\*\*: )(\d+)\.(\d+)\.(\d+)( \| \*\*Ratified\*\*: [^|]+\| \*\*Last Amended\*\*: )(\S+)")

DONE = {"implemented", "verified"}
SKIPPED = {"deferred", "abandoned"}
BLOCKED = {"undecided", "needs-info"}
RESUMABLE = {"specced", "in-progress"}
STATUSES = DONE | SKIPPED | BLOCKED | RESUMABLE | {"planned"}


@dataclass
class Entry:
    number: str
    title: str
    status: str
    start: int  # index of the heading line
    end: int  # index one past the last line of the entry
    fields: dict = field(default_factory=dict)

    def text(self, name: str) -> str:
        return "\n".join(self.fields.get(name, [])).strip()


def section_bounds(lines: list[str], title: str) -> tuple[int, int]:
    start = next((i + 1 for i, ln in enumerate(lines) if ln.strip() == f"## {title}"), len(lines))
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, end


def parse_entries(lines: list[str]) -> list[Entry]:
    start, end = section_bounds(lines, "Planned Specs")
    entries, current, name = [], None, None
    for i in range(start, end):
        heading = ENTRY.match(lines[i])
        if heading:
            if current:
                current.end = i
            current = Entry(heading[1], heading[2], heading[3], i, end)
            entries.append(current)
            name = None
        elif current is not None:
            match = FIELD.match(lines[i])
            if match:
                name = match[1].strip()
                current.fields[name] = [match[2]] if match[2] else []
            elif name and lines[i].strip():
                current.fields[name].append(lines[i].rstrip())
    return entries


def parse_questions(lines: list[str]) -> list[tuple[str, str]]:
    start, end = section_bounds(lines, "Open Questions")
    found = []
    for line in lines[start:end]:
        match = QUESTION.match(line)
        if match:
            found.append((match[1], match[2]))
        elif found and line.startswith("  ") and line.strip():
            found[-1] = (found[-1][0], found[-1][1] + " " + line.strip())
    return found


def expand_numbers(text: str) -> list[str]:
    """'001, 003' -> ['001','003']; '001–008' -> 001..008; 'none' -> []."""
    numbers = []
    for first, last in re.findall(r"(\d{3})(?:\s*[–-]\s*(\d{3}))?", text):
        numbers += [f"{n:03d}" for n in range(int(first), int(last or first) + 1)]
    return numbers


def next_action(text: str) -> dict:
    lines = text.splitlines()
    entries = parse_entries(lines)
    questions = parse_questions(lines)
    by_number = {e.number: e for e in entries}
    for entry in entries:
        if entry.status in DONE | SKIPPED:
            continue
        info = {"number": entry.number, "title": entry.title, "status": entry.status,
                "spec_dir": entry.text("Spec dir")}
        if entry.status in RESUMABLE:
            return {"action": "resume", **info}
        if entry.status in BLOCKED:
            return {"action": "blocked", "reason": f"status is {entry.status}", **info,
                    "open_questions": related_questions(questions, entry.number)}
        deps = expand_numbers(entry.text("Depends on"))
        missing = [d for d in deps if d not in by_number]
        pending = [d for d in deps if d in by_number and by_number[d].status not in DONE | SKIPPED]
        if missing or pending:
            return {"action": "blocked", "reason": f"depends on {', '.join(missing + pending)}",
                    **info, "open_questions": []}
        return {"action": "specify", **info, "warnings": [
                    f"depends on {d}, which is {by_number[d].status}" for d in deps
                    if by_number[d].status in SKIPPED],
                "description": entry.text("Description"), "outcome": entry.text("Outcome"),
                "scope_in": entry.text("Scope (in)"), "scope_out": entry.text("Scope (out)"),
                "depends_on": entry.text("Depends on"), "governed_by": entry.text("Governed by"),
                "notes": entry.text("Notes"),
                "open_questions": related_questions(questions, entry.number)}
    return {"action": "complete"}


def related_questions(questions: list[tuple[str, str]], number: str) -> list[str]:
    return [f"{qid} — {body}" for qid, body in questions if re.search(rf"\b{number}\b", body)]


def find_by_spec_dir(lines: list[str], spec_dir: str) -> Entry | None:
    wanted = spec_dir.strip().strip("/")
    for entry in parse_entries(lines):
        if entry.text("Spec dir").strip().strip("/") == wanted:
            return entry
    return None


def bump_patch(lines: list[str], old_status: str, new_status: str, number: str, today: str) -> list[str]:
    """Bump the footer PATCH version and rewrite the Sync Impact Report."""
    footer_i = next((i for i in range(len(lines) - 1, -1, -1) if FOOTER.search(lines[i])), None)
    if footer_i is None:
        raise ValueError("roadmap footer (**Version**: ... | **Ratified** ... | **Last Amended** ...) not found")
    m = FOOTER.search(lines[footer_i])
    old = f"{m[2]}.{m[3]}.{m[4]}"
    new = f"{m[2]}.{m[3]}.{int(m[4]) + 1}"
    lines[footer_i] = FOOTER.sub(lambda g: f"{g[1]}{new}{g[5]}{today}", lines[footer_i])
    rationale = f"PATCH — status transition on spec {number}: {old_status} → {new_status}"

    if lines and lines[0].strip() == "<!--":
        close = next((i for i, ln in enumerate(lines) if ln.strip() == "-->"), None)
        if close is not None:
            body = lines[1:close]
            first_previous = next((i for i, ln in enumerate(body) if ln.startswith("Previous")), len(body))
            previous = body[first_previous:]
            rationale_at = next((i for i, ln in enumerate(body) if ln.startswith("Bump rationale:")), None)
            if rationale_at is not None:
                block = [body[rationale_at].split(":", 1)[1].strip()]
                for ln in body[rationale_at + 1:]:
                    if not ln.strip():
                        break
                    block.append(ln)
                previous = [f"Previous ({old}): " + block[0]] + block[1:] + previous
            report = ["<!--", "SYNC IMPACT REPORT", "==================",
                      f"Version change: {old} → {new}", f"Bump rationale: {rationale}", "",
                      "Changes this revision:", f"  - Spec {number}: {old_status} → {new_status}", "",
                      f"Specs affected: {number}", "Open questions added/resolved: none", ""]
            return report + previous + ["-->"] + lines[close + 1:]
    return lines


def set_status(text: str, number: str, status: str, spec_dir: str | None = None,
               today: str | None = None) -> str:
    if status not in STATUSES:
        raise ValueError(f"unknown status {status!r}")
    today = today or datetime.date.today().isoformat()
    lines = text.splitlines()
    entry = next((e for e in parse_entries(lines) if e.number == number), None)
    if entry is None:
        raise ValueError(f"no entry {number} in Planned Specs")
    changed_dir = bool(spec_dir) and entry.text("Spec dir").strip() != spec_dir.strip()
    if entry.status == status and not changed_dir:
        return text  # idempotent
    lines[entry.start] = re.sub(r"\[status: [\w-]+\]", f"[status: {status}]", lines[entry.start])
    if spec_dir:
        pointer = f"- **Spec dir:** {spec_dir}"
        existing = next((i for i in range(entry.start + 1, entry.end)
                         if lines[i].startswith("- **Spec dir:**")), None)
        if existing is not None:
            lines[existing] = pointer
        else:
            last = max((i for i in range(entry.start + 1, entry.end) if lines[i].strip()),
                       default=entry.start)
            lines.insert(last + 1, pointer)
    lines = bump_patch(lines, entry.status, status, number, today)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
