from pathlib import Path

ROOT = Path(".")

def replace_once(path, old, new):
    p = ROOT / path
    data = p.read_text(encoding="utf-8")
    count = data.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one patch point, found {count}")
    p.write_text(data.replace(old, new, 1), encoding="utf-8")

# Signal the shared post-game finish path before Pure's optional key wait.
replace_once(
    "dosbox-pure/dosbox_pure_osd.h",
    "\t\t\tbool runsoloexe = (ms->exe_count == 1 && ms->fs_rows <= (int)(dbp_images.size() + 1) && !DBP_Run::patch.show_variants);\n",
    "\t\t\tbool runsoloexe = (ms->exe_count == 1 && ms->fs_rows <= (int)(dbp_images.size() + 1) && !DBP_Run::patch.show_variants);\n\t\t\tif (m == M_FINISH) DBPS_RequestPostGameReset();\n",
)

# Transfer the request safely from the emulation thread to the frontend thread.
replace_once(
    "dosbox-pure/dosbox_pure_libretro.cpp",
    "#include <sstream>\n",
    "#include <sstream>\n#include <atomic>\n",
)
replace_once(
    "dosbox-pure/dosbox_pure_libretro.cpp",
    "static bool dbp_game_running, dbp_pause_events, dbp_paused_midframe, dbp_frame_pending, dbp_biosreboot, dbp_biospoweroff, dbp_system_cached, dbp_system_scannable, dbp_refresh_memmaps;\n",
    "static bool dbp_game_running, dbp_pause_events, dbp_paused_midframe, dbp_frame_pending, dbp_biosreboot, dbp_biospoweroff, dbp_system_cached, dbp_system_scannable, dbp_refresh_memmaps;\nstatic std::atomic<bool> dbps_post_game_reset_requested(false);\n",
)
replace_once(
    "dosbox-pure/dosbox_pure_libretro.cpp",
    "void DBP_ForceReset(bool forcemenu)\n{\n\t#ifdef DBP_STANDALONE\n\tif (dbp_wasloaded) DBPS_OnReset();\n\t#endif\n\tinit_dosbox(forcemenu);\n}\n",
    "void DBP_ForceReset(bool forcemenu)\n{\n\t#ifdef DBP_STANDALONE\n\tif (dbp_wasloaded) DBPS_OnReset();\n\t#endif\n\tinit_dosbox(forcemenu);\n}\n\nvoid DBPS_RequestPostGameReset()\n{\n\tdbps_post_game_reset_requested.store(true, std::memory_order_release);\n}\n\nbool DBPS_ConsumePostGameReset()\n{\n\treturn dbps_post_game_reset_requested.exchange(false, std::memory_order_acq_rel);\n}\n\nvoid DBPS_ForceResetToMenu()\n{\n\tDBP_ForceReset(true);\n}\n",
)
replace_once(
    "dosbox-pure/dosbox_pure_sta.h",
    "bool DBPS_IsGameRunning();\n",
    "bool DBPS_IsGameRunning();\nvoid DBPS_RequestPostGameReset();\nbool DBPS_ConsumePostGameReset();\nvoid DBPS_ForceResetToMenu();\n",
)

# Consume the one-shot request after retro_run, on the frontend thread.
replace_once(
    "main/main.cpp",
    "\n\t// Restore SOFI Space only after the launched DOS program has actually run and then exited.\n",
    """
\n\t// Reset DOSBox Pure after its shared post-game finish path, without waiting for a key.
\tif (DBPS_ConsumePostGameReset())
\t{
\t\tDBPS_ForceResetToMenu();
\t\tif (SofiLauncherWaitingForGameExit)
\t\t{
\t\t\tSofiLauncherWaitingForGameExit = false;
\t\t\tSofiLauncherGameWasRunning = false;
\t\t\tSofiLauncherProfileFilterActive = false;
\t\t\tSofiLauncherProfileCyclesMaxActive = false;
\t\t\tSofiLauncherProfileCyclesMax.clear();
\t\t\tSofiLauncherRestoreProfileCyclesMax();
\t\t\tSofiLauncherRestoreProfileVideoOverrides();
\t\t\tSofiLauncherRestoreProfileAudioOverrides();
\t\t\tSofiLauncherRestoreProfileCoreOverrides();
\t\t}
\t\tDoApplyInterfaceOptions = true;
\t\tif (ImGuiReady)
\t\t{
\t\t\tImGuiIO& io = ImGui::GetIO();
\t\t\tio.AddMouseButtonEvent(0, false);
\t\t\tio.AddMouseButtonEvent(1, false);
\t\t\tio.AddMouseButtonEvent(2, false);
\t\t\tImGui::ClearActiveID();
\t\t\tImGui::GetCurrentContext()->MovingWindow = NULL;
\t\t}
\t\tSofiCommanderCaptured = false;
\t\tZL_Display::SetPointerLock(false);
\t\tSofiUIVisible = true;
\t\tshowOSD = DBPS_IsShowingOSD();
\t}
\n\t// Restore SOFI Space only after the launched DOS program has actually run and then exited.
""",
)
