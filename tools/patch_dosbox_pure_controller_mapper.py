from pathlib import Path

def replace_once(path, old, new):
    source = path.read_text(encoding="utf-8")
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one match, found {count}")
    path.write_text(source.replace(old, new), encoding="utf-8", newline="\n")

root = Path("dosbox-pure")
replace_once(
    root / "dosbox_pure_sta.h",
    "bool DBPS_IsShowingOSD();\n",
    "bool DBPS_IsShowingOSD();\nvoid DBPS_OpenControllerMapper();\nvoid DBPS_OpenOnScreenKeyboard();\nvoid DBPS_ToggleControllerMapper();\nvoid DBPS_ToggleOnScreenKeyboard();\n",
)
replace_once(
    root / "dosbox_pure_osd.h",
    "if (dbp_map_osd == 'o' && dbp_game_running) { mode = DBPOSD_OSK; } // only osk",
    "if (dbp_map_osd == 'o' && dbp_game_running && in_mode != DBPOSD_MAPPER) { mode = DBPOSD_OSK; } // only osk unless explicitly opening Controller Mapper",
)
replace_once(
    root / "dosbox_pure_osd.h",
    "static void DBP_CloseOSD()\n{\n\tDBP_OSD.SetMode(_DBPOSD_CLOSE);\n}\n",
    "static void DBP_CloseOSD()\n{\n\tDBP_OSD.SetMode(_DBPOSD_CLOSE);\n}\n\n#ifdef DBP_STANDALONE\nstatic void DBPS_OpenControllerMapperOnEmuThread()\n{\n\tif (DBPS_IsShowingOSD()) DBP_OSD.SetMode(DBPOSD_MAPPER);\n\telse DBP_StartOSD(DBPOSD_MAPPER);\n}\n\nvoid DBPS_OpenControllerMapper()\n{\n\t// Do not overwrite another deferred emulator-thread action (for example, Open Content).\n\tif (!dbps_emu_thread_func) dbps_emu_thread_func = DBPS_OpenControllerMapperOnEmuThread;\n}\n\nstatic void DBPS_OpenOnScreenKeyboardOnEmuThread()\n{\n\tif (DBPS_IsShowingOSD()) DBP_OSD.SetMode(DBPOSD_OSK);\n\telse DBP_StartOSD(DBPOSD_OSK);\n}\n\nvoid DBPS_OpenOnScreenKeyboard()\n{\n\t// Preserve any other deferred emulator-thread action.\n\tif (!dbps_emu_thread_func) dbps_emu_thread_func = DBPS_OpenOnScreenKeyboardOnEmuThread;\n}\n\nstatic void DBPS_ToggleControllerMapperOnEmuThread()\n{\n\tif (DBPS_IsShowingOSD() && DBP_OSD.mode == DBPOSD_MAPPER) DBP_CloseOSD();\n\telse if (DBPS_IsShowingOSD()) DBP_OSD.SetMode(DBPOSD_MAPPER);\n\telse DBP_StartOSD(DBPOSD_MAPPER);\n}\n\nvoid DBPS_ToggleControllerMapper()\n{\n\tif (!dbps_emu_thread_func) dbps_emu_thread_func = DBPS_ToggleControllerMapperOnEmuThread;\n}\n\nstatic void DBPS_ToggleOnScreenKeyboardOnEmuThread()\n{\n\tif (DBPS_IsShowingOSD() && DBP_OSD.mode == DBPOSD_OSK) DBP_CloseOSD();\n\telse if (DBPS_IsShowingOSD()) DBP_OSD.SetMode(DBPOSD_OSK);\n\telse DBP_StartOSD(DBPOSD_OSK);\n}\n\nvoid DBPS_ToggleOnScreenKeyboard()\n{\n\tif (!dbps_emu_thread_func) dbps_emu_thread_func = DBPS_ToggleOnScreenKeyboardOnEmuThread;\n}\n#endif\n",
)
