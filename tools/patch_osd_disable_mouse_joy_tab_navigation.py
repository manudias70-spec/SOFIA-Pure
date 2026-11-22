#!/usr/bin/env python3
"""Remove legacy mouse and shoulder-button OSD tab switching, preserving SOFIA sidebar controls."""
from pathlib import Path

target = Path("dosbox-pure/dosbox_pure_osd.h")
if not target.is_file():
    raise SystemExit(f"Expected upstream OSD source not found: {target}")

source = target.read_text(encoding="utf-8")

def replace_once(old, new, label):
    global source
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"OSD mouse/joy patch aborted at {label}: expected one match, found {count}")
    source = source.replace(old, new, 1)

# The two shoulder buttons were mapped to Grave/Tab, which switched OSD tabs.
replace_once(
    "\t\t\t{ 0, RETRO_DEVICE_JOYPAD, 0, RETRO_DEVICE_ID_JOYPAD_L, DBPET_KEYDOWN, KBD_grave },\n"
    "\t\t\t{ 0, RETRO_DEVICE_JOYPAD, 0, RETRO_DEVICE_ID_JOYPAD_R, DBPET_KEYDOWN, KBD_tab },\n",
    "\t\t\t// L1/R1 no longer switch OSD tabs; all other Mapper/gamepad bindings remain unchanged.\n",
    "L1/R1 OSD bindings",
)

# Remove the old native top-tab buttons in the standalone OSD. The SOFIA sideNav
# branch above them is deliberately retained as the sole interface navigation.
replace_once(
    "\t\t\telse\n"
    "\t\t\t{\n"
    "\t\t\t\tint osk = 3*(int)(first_shell && !DBP_FullscreenOSD), mpr = 3*(int)!!first_shell, n = 4+osk+mpr;\n"
    "\t\t\t\tif (       buf.DrawButton(btnblend, btny, lh,   0,   2, n, btnmrgn, mode == DBPOSD_MAIN,     mouse, \"START MENU\",                              txtblend) && mouse.click) SetMode(DBPOSD_MAIN);\n"
    "\t\t\t\tif (osk && buf.DrawButton(btnblend, btny, lh,   2,   5, n, btnmrgn, mode == DBPOSD_OSK,      mouse, \"ON-SCREEN KEYBOARD\",                      txtblend) && mouse.click) SetMode(DBPOSD_OSK);\n"
    "\t\t\t\tif (mpr && buf.DrawButton(btnblend, btny, lh, n-5, n-2, n, btnmrgn, mode == DBPOSD_MAPPER,   mouse, \"CONTROLLER MAPPER\",                       txtblend) && mouse.click) SetMode(DBPOSD_MAPPER);\n"
    "\t\t\t\tif (       buf.DrawButton(btnblend, btny, lh, n-2, n  , n, btnmrgn, mode == DBPOSD_SETTINGS, mouse, \"SETTINGS\",                                txtblend) && mouse.click) SetMode(DBPOSD_SETTINGS);\n"
    "\t\t\t}\n"
    "\t\t\t#endif",
    "\t\t\telse\n"
    "\t\t\t{\n"
    "\t\t\t\t// Legacy native OSD tab buttons removed; SOFIA side navigation remains active.\n"
    "\t\t\t}\n"
    "\t\t\t#endif",
    "legacy native OSD tab buttons",
)

# Remove the legacy L/R arrow shortcuts and wheel-to-tab event injection.
replace_once(
    "\t\t\tif (!sideNav && w >= 296 && buf.DrawButtonAt(btnblend, btny, lh, 4, 4, 8, 30, false,                 mouse, \"L\",                                           txtblend) && mouse.click) evnt(DBPET_KEYUP, KBD_grave, 0);\n",
    "",
    "legacy L button",
)
replace_once(
    "\t\t\tif (!sideNav && w >= 296 && buf.DrawButtonAt(btnblend, btny, lh, 4, 4, w-30, w-8, false,             mouse, \"R\",                                           txtblend) && mouse.click) evnt(DBPET_KEYUP, KBD_tab, 0);\n",
    "",
    "legacy R button",
)
replace_once(
    "\t\t\tif (!sideNav && mouse.y >= btny && (mouse.wheel_up || mouse.wheel_down)) evnt(DBPET_KEYUP, (mouse.wheel_down ? KBD_grave : KBD_tab), 0);\n",
    "",
    "mouse wheel tab switching",
)

# Remove direct tab-click navigation from the alternate non-standalone build path too.
for old, label in [
    ('\t\t\tif (       buf.DrawButton(btnblend, btny, lh,   0, 1, n, btnmrgn, mode == DBPOSD_MAIN,   mouse, (w < 500 ? "START"    : "START MENU"),         txtblend) && mouse.click) SetMode(DBPOSD_MAIN);\n', "alternate Start tab"),
    ('\t\t\tif (osk && buf.DrawButton(btnblend, btny, lh,   1, 2, n, btnmrgn, mode == DBPOSD_OSK,    mouse, (w < 500 ? "KEYBOARD" : "ON-SCREEN KEYBOARD"), txtblend) && mouse.click) SetMode(DBPOSD_OSK);\n', "alternate OSK tab"),
    ('\t\t\tif (mpr && buf.DrawButton(btnblend, btny, lh, n-1, n, n, btnmrgn, mode == DBPOSD_MAPPER, mouse, (w < 500 ? "CONTROLS" : "CONTROLLER MAPPER"),  txtblend) && mouse.click) SetMode(DBPOSD_MAPPER);\n', "alternate Mapper tab"),
]:
    if source.count(old) != 1:
        raise SystemExit(f"OSD mouse/joy patch aborted at {label}: expected one match, found {source.count(old)}")
    source = source.replace(old, "", 1)

target.write_text(source, encoding="utf-8", newline="\n")
print("Removed legacy OSD mouse tab controls and L1/R1 tab-switch bindings")
print("Preserved SOFIA sideNav, L2/R2, L3, D-pad, face buttons, Mapper internals and all other inputs")
