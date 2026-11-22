#!/usr/bin/env python3
"""Scale the native DOSBox Pure on-screen keyboard to 50% and right-anchor it."""
from pathlib import Path

target = Path("dosbox-pure/dosbox_pure_osd.h")
if not target.is_file():
    raise SystemExit(f"Expected upstream OSD source not found: {target}")

source = target.read_text(encoding="utf-8")

old = """\t\tfloat fy = fx * buf.ratio * buf.height / buf.width; if (fy < 1) fy = 1;

\t\tint oskx = (int)(buf.width / fx / 2) - (KWIDTH / 2);"""
new = """\t\tfloat fy = fx * buf.ratio * buf.height / buf.width; if (fy < 1) fy = 1;

\t\t// SOFIA: render the native on-screen keyboard at half scale.
\t\tfx *= 0.5f;
\t\tfy *= 0.5f;

\t\t// SOFIA: anchor the keyboard to the right edge with a small logical margin.
\t\tint oskx = (int)(buf.width / fx) - KWIDTH - 8;"""

count = source.count(old)
if count != 1:
    raise SystemExit(f"OSK size/position patch aborted: expected one exact anchor, found {count}")

target.write_text(source.replace(old, new, 1), encoding="utf-8", newline="\n")
print("Scaled native on-screen keyboard to 50% and right-aligned it")
