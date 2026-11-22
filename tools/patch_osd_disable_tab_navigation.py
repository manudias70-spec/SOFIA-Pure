from pathlib import Path

def replace_once(path, old, new, label):
    source = path.read_text(encoding="utf-8")
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"{path}: {label}: expected one match, found {count}")
    path.write_text(source.replace(old, new), encoding="utf-8", newline="\n")

osd = Path("dosbox-pure/dosbox_pure_osd.h")
if not osd.is_file():
    raise SystemExit(f"Expected pinned DOSBox Pure OSD source not found: {osd}")

# Remove only the two joypad shortcuts that inject the OSD tab-switch keys.
replace_once(
    osd,
    "\t\t\t{ 0, RETRO_DEVICE_JOYPAD, 0, RETRO_DEVICE_ID_JOYPAD_L, DBPET_KEYDOWN, KBD_grave },\n",
    "",
    "L1 previous-tab shortcut",
)
replace_once(
    osd,
    "\t\t\t{ 0, RETRO_DEVICE_JOYPAD, 0, RETRO_DEVICE_ID_JOYPAD_R, DBPET_KEYDOWN, KBD_tab },\n",
    "",
    "R1 next-tab shortcut",
)

# Remove the legacy left/right footer shortcuts and mouse-wheel tab switching.
replace_once(
    osd,
    "\t\t\tif (!sideNav && w >= 296 && buf.DrawButtonAt(btnblend, btny, lh, 4, 4, 8, 30, false,                 mouse, \"L\",                                           txtblend) && mouse.click) evnt(DBPET_KEYUP, KBD_grave, 0);\n",
    "",
    "legacy left footer shortcut",
)
replace_once(
    osd,
    "\t\t\tif (!sideNav && w >= 296 && buf.DrawButtonAt(btnblend, btny, lh, 4, 4, w-30, w-8, false,             mouse, \"R\",                                           txtblend) && mouse.click) evnt(DBPET_KEYUP, KBD_tab, 0);\n",
    "",
    "legacy right footer shortcut",
)
replace_once(
    osd,
    "\t\t\tif (!sideNav && mouse.y >= btny && (mouse.wheel_up || mouse.wheel_down)) evnt(DBPET_KEYUP, (mouse.wheel_down ? KBD_grave : KBD_tab), 0);\n",
    "",
    "legacy footer wheel shortcut",
)

# Remove the legacy top-tab buttons from the non-standalone OSD.
replace_once(
    osd,
    """\t\t\tint osk = (int)(first_shell && !DBP_FullscreenOSD), mpr = (int)!!first_shell, n = 1+osk+mpr;
\t\t\tif (       buf.DrawButton(btnblend, btny, lh,   0, 1, n, btnmrgn, mode == DBPOSD_MAIN,   mouse, (w < 500 ? "START"    : "START MENU"),         txtblend) && mouse.click) SetMode(DBPOSD_MAIN);
\t\t\tif (osk && buf.DrawButton(btnblend, btny, lh,   1, 2, n, btnmrgn, mode == DBPOSD_OSK,    mouse, (w < 500 ? "KEYBOARD" : "ON-SCREEN KEYBOARD"), txtblend) && mouse.click) SetMode(DBPOSD_OSK);
\t\t\tif (mpr && buf.DrawButton(btnblend, btny, lh, n-1, n, n, btnmrgn, mode == DBPOSD_MAPPER, mouse, (w < 500 ? "CONTROLS" : "CONTROLLER MAPPER"),  txtblend) && mouse.click) SetMode(DBPOSD_MAPPER);
""",
    "",
    "legacy non-standalone OSD tabs",
)

# Remove only the legacy standalone tab strip. The SOFIA sideNav branch remains.
replace_once(
    osd,
    """\t\t\telse
\t\t\t{
\t\t\t\tint osk = 3*(int)(first_shell && !DBP_FullscreenOSD), mpr = 3*(int)!!first_shell, n = 4+osk+mpr;
\t\t\t\tif (       buf.DrawButton(btnblend, btny, lh,   0,   2, n, btnmrgn, mode == DBPOSD_MAIN,     mouse, "START MENU",                              txtblend) && mouse.click) SetMode(DBPOSD_MAIN);
\t\t\t\tif (osk && buf.DrawButton(btnblend, btny, lh,   2,   5, n, btnmrgn, mode == DBPOSD_OSK,      mouse, "ON-SCREEN KEYBOARD",                      txtblend) && mouse.click) SetMode(DBPOSD_OSK);
\t\t\t\tif (mpr && buf.DrawButton(btnblend, btny, lh, n-5, n-2, n, btnmrgn, mode == DBPOSD_MAPPER,   mouse, "CONTROLLER MAPPER",                       txtblend) && mouse.click) SetMode(DBPOSD_MAPPER);
\t\t\t\tif (       buf.DrawButton(btnblend, btny, lh, n-2, n  , n, btnmrgn, mode == DBPOSD_SETTINGS, mouse, "SETTINGS",                                txtblend) && mouse.click) SetMode(DBPOSD_SETTINGS);
\t\t\t}
""",
    "",
    "legacy standalone OSD tabs",
)

# Remove the obsolete spacing variable used only by the legacy tab strip.
replace_once(
    osd,
    "\\t\\t\\tint btny = h - 13 - lh, btnmrgn = (w >= 296 ? 34 : 8), ydist = (isOSK ? (int)(127 - (btny - mouse.y) / (h*0.001f)) : 0xFF);\\n",
    "\\t\\t\\tint btny = h - 13 - lh, ydist = (isOSK ? (int)(127 - (btny - mouse.y) / (h*0.001f)) : 0xFF);\\n",
    "legacy tab-strip spacing",
)

# Remove the global Tab / Shift+Tab / Grave handler, leaving each menu's own
# Input() processing untouched (Mapper confirm, cancel, back and directions).
replace_once(
    osd,
    """\t\tif (type == DBPET_KEYUP && ((KBD_KEYS)val == KBD_tab || (KBD_KEYS)val == KBD_grave))
\t\t{
\t\t\tint add = (((KBD_KEYS)val == KBD_tab && !DBP_IsKeyDown(KBD_leftshift) && !DBP_IsKeyDown(KBD_rightshift)) ? 1 : -1), next = (int)mode;
\t\t\tint skip1 = ((first_shell && !DBP_FullscreenOSD) ? -1 : DBPOSD_OSK), skip2 = (first_shell ? -1 : DBPOSD_MAPPER);
\t\t\tdo { next = (next + (int)_DBPOSD_COUNT + add) % _DBPOSD_COUNT; } while (next == skip1 || next == skip2);
\t\t\tSetMode((DBP_OSDMode)next);
\t\t}
""",
    "",
    "OSD keyboard tab-switch handler",
)

print("Removed only legacy OSD tab navigation. Preserved SOFIA sideNav, L3 Mapper opening and all menu-internal controls.")
