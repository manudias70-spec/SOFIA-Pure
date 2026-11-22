#!/usr/bin/env python3
"""Scale DOSBox Pure's native on-screen keyboard to 60% and center it."""
from pathlib import Path
import re

target = Path("dosbox-pure/dosbox_pure_osd.h")
if not target.is_file():
    raise SystemExit(f"Expected upstream OSD source not found: {target}")

source = target.read_text(encoding="utf-8")

# Patch the actual geometry block in DBP_OnScreenKeyboardState::GFX.
# Run this immediately after checking out the pinned Pure source, before
# the other OSD patchers edit the same header.
pattern = re.compile(
    r"\t\tint thickness = buf\.GetThickness\(\);\n"
    r"\t\tfloat fx = .*?;\n"
    r"\t\tfloat fy = .*?;\n"
    r"\t\tint thicknessy = .*?;\n"
    r"\n"
    r"\t\tint oskx = .*?;\n"
    r"\t\tint osky = .*?;",
    re.DOTALL,
)

replacement = """\t\tint baseThickness = buf.GetThickness();
\t\tfloat fx = (buf.width < KWIDTH ? (buf.width - 10) / (float)KWIDTH : (float)baseThickness);
\t\tfloat fy = fx * buf.ratio * buf.height / buf.width; if (fy < 1) fy = 1;

\t\t// SOFIA: increase native OSD keyboard geometry to 60% of original size.
\t\tfx *= 0.6f;
\t\tfy *= 0.6f;
\t\tint thickness = (int)(fx + .95f);
\t\tint thicknessy = (int)(fy + .95f);

\t\t// SOFIA: center the keyboard horizontally and vertically in the OSD.
\t\tint oskx = ((int)(buf.width / fx) - KWIDTH) / 2;
\t\tint osky = ((int)(buf.height / fy) - 85) / 2;"""

if "SOFIA: scale all native OSD keyboard geometry to half size." in source:
    raise SystemExit("OSK size patch already present; refusing to apply it twice")

source, count = pattern.subn(lambda _: replacement, source, count=1)
if count != 1:
    raise SystemExit(f"OSK size/position patch aborted: expected one GFX geometry block, found {count}")

if "SOFIA: anchor the keyboard to the right edge with a small margin." not in source:
    raise SystemExit("OSK size patch verification failed: centering marker missing")

target.write_text(source, encoding="utf-8", newline="\n")
print("Verified: native DOSBox Pure OSD keyboard scaled to 60% and centered")
