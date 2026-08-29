#!/usr/bin/python3
"""Runs before every Write, Edit and Bash command.

If something is about to be written that a person reads LATER — a how-to page, a runbook,
a skill, a README — this tells the agent to load the writing-runbooks skill first.

Why it is a hook and not a rule: the skill gets skipped when the page is the tail end of a
coding job, because it feels like part of the code rather than a thing anyone reads cold.
Noticing is the part that fails, so this does not rely on noticing.

**It asks two questions, and either one is enough.**

1. *Is it in a place where pages live?* A name like `SKILL.md`, or a folder like `/docs/`
   or `/skills/`.
2. *Does the writing itself read like instructions?* Rules, warnings, numbered steps,
   telling a reader what to do. A page can be called anything, and the ones that slip
   through are the ones with an ordinary name — a second page inside a skill folder, a
   recipe an agent follows. Only the name was ever checked, so those were silent.

**Bash counts.** Watching only the Write and Edit tools leaves a file changed with `sed`
or a heredoc invisible, and that is a normal way to edit. A command is read for the paths
it would WRITE to; reading, searching and git are ignored. The path-reading is borrowed
from `worktree-reminder.py` so there is one copy of it, not two.

Speaks once per file per session; a second edit to the same file stays quiet.

**After changing this, run `./writing-runbooks-reminder.test.sh`.** A hook that is too
noisy gets switched off, and a hook that is too quiet is not there at all — and both look
exactly like success.

Uses the Mac's own python3 and nothing else. `jq` is not installed on this machine — a
hook that reaches for it fails silently and does nothing, which looks exactly like a hook
that is working.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile

# Folders whose pages are written to be read later.
WATCHED_DIRS = ("/docs/", "/runbooks/", "/plans/", "/skills/", "/scheduled-tasks/")

# Files that are a page whatever folder they sit in.
WATCHED_NAMES = ("SKILL.md", "README.md", "RECIPE.md", "project.md", "AGENTS.md")

# Endings that can hold a page. Anything else is code or data.
PAGE_SUFFIXES = (".md", ".mdx", ".markdown", ".rst", ".txt")

MESSAGE = (
    "STOP before writing {path}. Somebody reads this later with none of today's "
    "context. Load the writing-runbooks skill and follow it. Cut the date, the story of "
    "how it was worked out, and any snapshot of how things stand today; keep what to do "
    "and what goes wrong if you do not."
)

# ---------------------------------------------------------------------------
# Does the writing itself read like instructions somebody follows?
#
# Each of these is a way instructions talk. One on its own proves nothing — ordinary
# writing says "never" too — so several have to appear together before this speaks. The
# bar is deliberately high: a hook nobody can ignore is one that is right nearly always.
# ---------------------------------------------------------------------------
SIGNALS = (
    # A flat rule, or a warning about getting it wrong.
    re.compile(r"(?im)^[\s>*_-]*(?:\*\*)?(?:never|always|do not|don't|⛔|⚠|must not"
               r"|careful)\b"),
    # The same, said mid-sentence with weight on it.
    re.compile(r"(?i)\b(?:you must|it must|never|always) (?:say|be|use|write|read|run|do|"
               r"click|open|check|leave|send|call)\b"),
    # A numbered step, the shape of a procedure.
    re.compile(r"(?m)^#{1,6}\s*(?:step\s*)?\d+[.)]\s+\S"),
    # Telling the reader to go and read something first.
    re.compile(r"(?i)\bread (?:this|it|that|the)\b[^.\n]{0,40}\b(?:first|before|"
               r"whole|exactly)\b"),
    # What to do when each thing happens — the branch list a procedure ends with.
    re.compile(r"(?m)^[\s>*_-]*(?:\*\*)?(?:if|when|otherwise)\b[^\n]{0,80}→"),
    # Naming what goes wrong, which is the half people leave out.
    re.compile(r"(?i)\b(?:otherwise|or else|which is why|the trap|goes wrong|"
               r"silently|quietly) \b"),
    # Speaking to whoever comes next.
    re.compile(r"(?i)\b(?:before you|after you|whoever (?:reads|edits|comes)|"
               r"the next (?:agent|person|run))\b"),
)

# Enough signals to be sure. Two is a coincidence; three is a page of instructions.
SIGNALS_NEEDED = 3

# A heading makes it a document rather than a stray paragraph, and counts as one signal.
HEADING = re.compile(r"(?m)^#{1,6}\s+\S")

# Below this it is a fragment — a one-line tweak, not a page being written. Kept low on
# purpose: a real page of rules can be a few short lines, and the signal count is what
# keeps ordinary writing out, not the length.
MIN_CHARS = 200


def reads_like_instructions(text: str) -> bool:
    """True when this writing tells a reader what to do and what goes wrong."""
    if not text or len(text) < MIN_CHARS:
        return False
    hits = sum(1 for pattern in SIGNALS if pattern.search(text))
    if HEADING.search(text):
        hits += 1
    return hits >= SIGNALS_NEEDED


def could_be_a_page(path: str) -> bool:
    """A file that could hold prose at all. Keeps the content check off source code."""
    return path.lower().endswith(PAGE_SUFFIXES)


def in_a_watched_place(path: str) -> bool:
    """The name or the folder alone is enough, whatever the writing says."""
    if os.path.basename(path) in WATCHED_NAMES:
        return True
    return could_be_a_page(path) and any(d in path for d in WATCHED_DIRS)


def bash_targets(command: str) -> list:
    """Paths a bash command would write to, using worktree-reminder's own reader.

    Borrowed rather than copied: two copies of these patterns drift, and the day they
    disagree is the day one of the hooks goes quiet for reasons nobody can see. If that
    file is gone, this simply stops watching Bash rather than failing the edit.
    """
    other = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "worktree-reminder.py")
    try:
        spec = importlib.util.spec_from_file_location("_worktree_reminder", other)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        found = module.targets(command)
        folders = [module._first(m) for m in module.CD.finditer(command)]
    except Exception:
        return []

    # `cd <folder> && sed -i '' page.md` writes a bare name with no folder in it, so the
    # folder is the only thing that says where it lands. Put the two back together, or a
    # page edited this way is invisible — which is exactly how it is normally edited.
    out = list(found)
    for path in found:
        if not os.path.isabs(path):
            out += [os.path.join(folder, path) for folder in folders]
    return out


def spoken_already(session: str, path: str) -> bool:
    """One reminder per file per session. Sets the mark as it checks."""
    key = hashlib.sha256(f"{session}|{path}".encode()).hexdigest()[:20]
    stamp = os.path.join(tempfile.gettempdir(), f"claude-runbook-reminder-{key}")
    if os.path.exists(stamp):
        return True
    try:
        open(stamp, "w").close()
    except OSError:
        pass
    return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool = payload.get("tool_name") or ""
    tool_input = payload.get("tool_input") or {}

    if tool == "Bash":
        # No content to read — a heredoc's text is buried in the command — so a Bash write
        # is judged on where it lands.
        paths = [p for p in bash_targets(tool_input.get("command") or "")
                 if in_a_watched_place(p)]
        path, text = (paths[0] if paths else ""), ""
    else:
        path = tool_input.get("file_path") or ""
        # Write carries the whole page; Edit carries only the part being put in.
        text = tool_input.get("content") or tool_input.get("new_string") or ""

    if not path:
        return 0
    if not (in_a_watched_place(path)
            or (could_be_a_page(path) and reads_like_instructions(text))):
        return 0
    if spoken_already(payload.get("session_id", ""), path):
        return 0

    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": MESSAGE.format(path=path),
    }}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
