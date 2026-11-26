from pathlib import Path

def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one match, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

osd = Path("dosbox-pure/dosbox_pure_osd.h")
sta = Path("dosbox-pure/dosbox_pure_sta.h")

replace_once(
    osd,
    "static void DBP_PureMenuProgram(Program** make)\n{\n",
    "static bool dbps_post_game_wait_key_accepted = false;\n\n"
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
    "\t\t\tdbps_post_game_wait_key_accepted = false;\n",
)

replace_once(
    osd,
    "bool DBPS_IsShowingOSD() { return (dbp_intercept && dbp_intercept->usegfx()); }\n",
    "bool DBPS_IsShowingOSD() { return (dbp_intercept && dbp_intercept->usegfx()); }\n"
    "bool DBPS_ConsumePostGameWaitKey() { bool accepted = dbps_post_game_wait_key_accepted; dbps_post_game_wait_key_accepted = false; return accepted; }\n",
)

replace_once(
    sta,
    "bool DBPS_IsShowingOSD();\n",
    "bool DBPS_IsShowingOSD();\n"
    "bool DBPS_ConsumePostGameWaitKey();\n",
)

print("Installed the read-only post-game wait-key notification.")
