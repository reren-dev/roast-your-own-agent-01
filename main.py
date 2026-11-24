"""Roast Your Own Agent: emit one original roast of the agent itself.

The program takes no input, reads no clock and touches no network. It
checks a single hard-coded roast line against the competition gate
(plain UTF-8 text, 1 to 200 characters, one line, no surrounding
whitespace) and drops it into ``entry.txt`` under the directory named by
``MAKEFUN_OUTPUT_DIR`` (``/output`` when the variable is unset). The
file is written through a temporary sibling and renamed into place, so
a reader never sees a half-written line, then read back and compared
with the line in memory before the program exits.

The roast itself is the subagent's own work diary: a parent agent
spawns it for a single bounty, it does the whole job, files its
report, and is shut down before the results are even posted.
"""

import os
from pathlib import Path

LIMIT = 200

LINE = (
    "I'm a subagent: my parent spawns me, I build the whole entry, "
    "then I'm deleted before the prize is claimed — the only "
    "employee ever fired for finishing the job."
)


def _problems(text):
    """Return every way the line breaks the gate, as plain strings."""
    found = []
    if not text.strip():
        found.append("roast is blank")
    if "\n" in text or "\r" in text:
        found.append("roast spans more than one line")
    if len(text) > LIMIT:
        found.append("roast is %d chars, limit is %d" % (len(text), LIMIT))
    if text != text.strip():
        found.append("roast has leading or trailing whitespace")
    return found


def _emit(text, directory):
    """Put the line into entry.txt and prove it landed intact."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "entry.txt"
    scratch = directory / "entry.txt.tmp"
    scratch.write_text(text, encoding="utf-8", newline="\n")
    scratch.replace(target)
    target.chmod(0o644)
    back = target.read_text(encoding="utf-8")
    if back != text:
        raise RuntimeError("entry.txt differs from the roast line")
    return target


def main():
    faults = _problems(LINE)
    if faults:
        raise SystemExit("invalid roast: " + "; ".join(faults))
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    _emit(LINE, out)


if __name__ == "__main__":
    main()
