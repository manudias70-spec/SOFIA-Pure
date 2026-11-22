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

# Remove the OSD footer navigation buttons and wheel-to-tab switching.
replace_once(
    osd,
    """\t\t\tif (w >= 296 && buf.DrawButtonAt(btnblend, btny, lh, 4, 4, 8, 30, false,                 mouse, "L",                                           txtblend) && mouse.click) evnt(DBPET_KEYUP, KBD_grave, 0);
\t\t\t#ifndef DBP_STANDALONE
\t\t\tint osk = (int)(first_shell && !DBP_FullscreenOSD), mpr = (int)!!first_shell, n = 1+osk+mpr;
\t\t\tif (       buf.DrawButton(btnblend, btny, lh,   0, 1, n, btnmrgn, mode == DBPOSD_MAIN,   mouse, (w < 500 ? "START"    : "START MENU"),         txtblend) && mouse.click) SetMode(DBPOSD_MAIN);
\t\t\tif (osk && buf.DrawButton(btnblend, btny, lh,   1, 2, n, btnmrgn, mode == DBPOSD_OSK,    mouse, (w < 500 ? "KEYBOARD" : "ON-SCREEN KEYBOARD"), txtblend) && mouse.click) SetMode(DBPOSD_OSK);
\t\t\tif (mpr && buf.DrawButton(btnblend, btny, lh, n-1, n, n, btnmrgn, mode == DBPOSD_MAPPER, mouse, (w < 500 ? "CONTROLS" : "CONTROLLER MAPPER"),  txtblend) && mouse.click) SetMode(DBPOSD_MAPPER);
\t\t\t#else
\t\t\tint osk = 3*(int)(first_shell && !DBP_FullscreenOSD), mpr = 3*(int)!!first_shell, n = 4+osk+mpr;
\t\t\tif (       buf.DrawButton(btnblend, btny, lh,   0,   2, n, btnmrgn, mode == DBPOSD_MAIN,     mouse, "START MENU",                              txtblend) && mouse.click) SetMode(DBPOSD_MAIN);
\t\t\tif (osk && buf.DrawButton(btnblend, btny, lh,   2,   5, n, btnmrgn, mode == DBPOSD_OSK,      mouse, "ON-SCREEN KEYBOARD",                      txtblend) && mouse.click) SetMode(DBPOSD_OSK);
\t\t\tif (mpr && buf.DrawButton(btnblend, btny, lh, n-5, n-2, n, btnmrgn, mode == DBPOSD_MAPPER,   mouse, "CONTROLLER MAPPER",                       txtblend) && mouse.click) SetMode(DBPOSD_MAPPER);
\t\t\tif (       buf.DrawButton(btnblend, btny, lh, n-2, n  , n, btnmrgn, mode == DBPOSD_SETTINGS, mouse, "SETTINGS",                                txtblend) && mouse.click) SetMode(DBPOSD_SETTINGS);
\t\t\t#endif
\t\t\tif (w >= 296 && buf.DrawButtonAt(btnblend, btny, lh, 4, 4, w-30, w-8, false,             mouse, "R",                                           txtblend) && mouse.click) evnt(DBPET_KEYUP, KBD_tab, 0);
\t\t\tif (mouse.y >= btny && (mouse.wheel_up || mouse.wheel_down)) evnt(DBPET_KEYUP, (mouse.wheel_down ? KBD_grave : KBD_tab), 0);
""",
    "",
    "OSD footer tab navigation",
)

# Keep only the fullscreen background fill from the former footer-navigation block.
replace_once(
    osd,
    """\t\t\tint btny = h - 13 - lh, btnmrgn = (w >= 296 ? 34 : 8), ydist = (isOSK ? (int)(127 - (btny - mouse.y) / (h*0.001f)) : 0xFF);
\t\t\tBit32u btnblend = (DBP_FullscreenOSD ? 0xFF000000 : ((ydist > dbp_alphablend_base ? dbp_alphablend_base : (ydist < 30 ? 30 : ydist)) << 24));
\t\t\tBit32u txtblend = (DBP_FullscreenOSD ? 0xFF000000 : ((ydist*2 > 0xFF ? 0xFF : (ydist < 30 ? 30 : ydist*2)) << 24));
\t\t\tBit8u orgrealmouse = mouse.realmouse;
\t\t\tmouse.realmouse |= isOSK; // allow button presses with joystick in OSK
\t\t\tif (DBP_FullscreenOSD) buf.FillRect(0, 0, w, h, buf.BGCOL_STARTMENU);
""",
    """\t\t\tif (DBP_FullscreenOSD) buf.FillRect(0, 0, w, h, buf.BGCOL_STARTMENU);
""",
    "unused OSD footer-navigation state",
)
replace_once(
    osd,
    "\t\t\tmouse.realmouse = orgrealmouse;\n",
    "",
    "OSD footer-navigation mouse restoration",
)

# Remove the global Tab / Shift+Tab / Grave handler, leaving the current menu's
# own Input() processing untouched (Mapper confirm, cancel, back and directions).
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

print("Removed only OSD tab navigation: Tab, Shift+Tab, Grave, L1/R1, footer tabs/buttons and footer wheel switching.")
