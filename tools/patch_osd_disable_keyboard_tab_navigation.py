#!/usr/bin/env python3
"""Disable only keyboard shortcuts that switch tabs inside DOSBox Pure's OSD."""
from pathlib import Path

target = Path("dosbox-pure/dosbox_pure_osd.h")
if not target.is_file():
    raise SystemExit(f"Expected upstream OSD source not found: {target}")

source = target.read_text(encoding="utf-8")
old = """\t\tif (type == DBPET_KEYUP && ((KBD_KEYS)val == KBD_tab || (KBD_KEYS)val == KBD_grave))
\t\t{
\t\t\tint add = (((KBD_KEYS)val == KBD_tab && !DBP_IsKeyDown(KBD_leftshift) && !DBP_IsKeyDown(KBD_rightshift)) ? 1 : -1), next = (int)mode;
\t\t\tint skip1 = ((first_shell && !DBP_FullscreenOSD) ? -1 : DBPOSD_OSK), skip2 = (first_shell ? -1 : DBPOSD_MAPPER);
\t\t\tdo { next = (next + (int)_DBPOSD_COUNT + add) % _DBPOSD_COUNT; } while (next == skip1 || next == skip2);
\t\t\tSetMode((DBP_OSDMode)next);
\t\t}
"""
if source.count(old) != 1:
    raise SystemExit(
        "OSD keyboard-navigation patch aborted: expected exactly one tab-switch handler"
    )

source = source.replace(
    old,
    "\t\t// Keyboard tab switching (Tab, Shift+Tab and Grave) is disabled in the OSD.\n",
)
target.write_text(source, encoding="utf-8", newline="\n")
print("Disabled only Tab/Shift+Tab/Grave OSD tab navigation")
