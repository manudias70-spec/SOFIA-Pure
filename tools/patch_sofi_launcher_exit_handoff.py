from pathlib import Path


def replace_once(path, old, new):
    source = path.read_text(encoding="utf-8")
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one match, found {count}: {old!r}")
    path.write_text(source.replace(old, new, 1), encoding="utf-8")


osd = Path("dosbox-pure/dosbox_pure_osd.h")
sta = Path("dosbox-pure/dosbox_pure_sta.h")

replace_once(
    osd,
    "static void DBP_PureMenuProgram(Program** make)\n{\n",
    "static bool dbps_post_game_wait_key_accepted = false;\n"
    "static bool dbps_return_to_frontend_after_wait = false;\n\n"
    "static void DBP_PureMenuProgram(Program** make)\n{\n",
)

replace_once(
    osd,
    "else if (pressedKey == key) pressedAnyKey = true;",
    "else if (pressedKey == key)\n"
    "\t\t\t{\n"
    "\t\t\t\tpressedAnyKey = true;\n"
    "\t\t\t\tif (msgType == 2) dbps_post_game_wait_key_accepted = true;\n"
    "\t\t\t}",
)

replace_once(
    osd,
    "\t\t\tmsgType = msg_type;\n",
    "\t\t\tmsgType = msg_type;\n"
    "\t\t\tif (msgType == 2) dbps_post_game_wait_key_accepted = false;\n",
)

replace_once(
    osd,
    "\t\t\t\tif (!interceptor.WaitAnyKeyPress(2)) return;\n\t\t\t\tm = M_NORMAL;",
    "\t\t\t\tif (!interceptor.WaitAnyKeyPress(2)) return;\n"
    "\t\t\t\tif (dbps_return_to_frontend_after_wait && dbps_post_game_wait_key_accepted)\n"
    "\t\t\t\t{\n"
    "\t\t\t\t\tdbps_return_to_frontend_after_wait = false;\n"
    "\t\t\t\t\tDBP_FullscreenOSD = false;\n"
    "\t\t\t\t\tdelete ms;\n"
    "\t\t\t\t\treturn;\n"
    "\t\t\t\t}\n"
    "\t\t\t\tm = M_NORMAL;",
)

replace_once(
    osd,
    "\t};\n\t*make = new Menu;\n}\n\nstatic void DBP_WheelShiftOSD",
    "\t};\n\t*make = new Menu;\n}\n\n"
    "void DBPS_SetReturnToFrontendAfterWait(bool enabled)\n"
    "{\n"
    "\tdbps_return_to_frontend_after_wait = enabled;\n"
    "}\n\n"
    "bool DBPS_ConsumePostGameWaitKey()\n"
    "{\n"
    "\tconst bool accepted = dbps_post_game_wait_key_accepted;\n"
    "\tdbps_post_game_wait_key_accepted = false;\n"
    "\treturn accepted;\n"
    "}\n\n"
    "static void DBP_WheelShiftOSD",
)

replace_once(
    sta,
    "bool DBPS_IsShowingOSD();\n",
    "bool DBPS_IsShowingOSD();\n"
    "void DBPS_SetReturnToFrontendAfterWait(bool enabled);\n"
    "bool DBPS_ConsumePostGameWaitKey();\n",
)

print("Installed targeted post-game key handoff without terminating the DOS shell.")
