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
    "bool DBPS_IsShowingOSD();\nvoid DBPS_OpenControllerMapper();\n",
)
replace_once(
    root / "dosbox_pure_osd.h",
    "if (dbp_map_osd == 'o' && dbp_game_running) { mode = DBPOSD_OSK; } // only osk",
    "if (dbp_map_osd == 'o' && dbp_game_running && in_mode != DBPOSD_MAPPER) { mode = DBPOSD_OSK; } // only osk unless explicitly opening Controller Mapper",
)
replace_once(
    root / "dosbox_pure_osd.h",
    "static void DBP_CloseOSD()\n{\n\tDBP_OSD.SetMode(_DBPOSD_CLOSE);\n}\n",
    "static void DBP_CloseOSD()\n{\n\tDBP_OSD.SetMode(_DBPOSD_CLOSE);\n}\n\n#ifdef DBP_STANDALONE\nstatic void DBPS_OpenControllerMapperOnEmuThread()\n{\n\tif (DBPS_IsShowingOSD()) DBP_OSD.SetMode(DBPOSD_MAPPER);\n\telse DBP_StartOSD(DBPOSD_MAPPER);\n}\n\nvoid DBPS_OpenControllerMapper()\n{\n\t// Do not overwrite another deferred emulator-thread action (for example, Open Content).\n\tif (!dbps_emu_thread_func) dbps_emu_thread_func = DBPS_OpenControllerMapperOnEmuThread;\n}\n#endif\n",
)
