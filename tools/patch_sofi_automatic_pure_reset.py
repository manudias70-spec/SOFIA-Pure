from pathlib import Path

ROOT = Path(".")

def replace_once(path, old, new):
    p = ROOT / path
    data = p.read_text(encoding="utf-8")
    count = data.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one patch point, found {count}")
    p.write_text(data.replace(old, new, 1), encoding="utf-8")

# Pure: M_FINISH is the common post-game path. Skip the obsolete key wait.
replace_once(
    "dosbox-pure/dosbox_pure_osd.h",
    """\t\t\tif (m == M_FINISH)
\t\t\t{
\t\t\t\t// ran without auto start or only for a very short time (maybe crash), wait for user confirmation
\t\t\t\tif (!interceptor.WaitAnyKeyPress(2)) return;
\t\t\t\tm = M_NORMAL;
\t\t\t}""",
    """\t\t\tif (m == M_FINISH)
\t\t\t{
\t\t\t\tDBPS_RequestPostGameReset();
\t\t\t\tm = M_NORMAL;
\t\t\t}""",
)

# Pure: transfer the request from the emulation thread to the frontend thread.
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
    """void DBP_ForceReset(bool forcemenu)
{
\t#ifdef DBP_STANDALONE
\tif (dbp_wasloaded) DBPS_OnReset();
\t#endif
\tinit_dosbox(forcemenu);
}""",
    """void DBP_ForceReset(bool forcemenu)
{
\t#ifdef DBP_STANDALONE
\tif (dbp_wasloaded) DBPS_OnReset();
\t#endif
\tinit_dosbox(forcemenu);
}

void DBPS_RequestPostGameReset()
{
\tdbps_post_game_reset_requested.store(true, std::memory_order_release);
}

bool DBPS_ConsumePostGameReset()
{
\treturn dbps_post_game_reset_requested.exchange(false, std::memory_order_acq_rel);
}

void DBPS_ForceResetToMenu()
{
\tDBP_ForceReset(true);
}""",
)

# Public standalone bridge declarations.
replace_once(
    "dosbox-pure/dosbox_pure_sta.h",
    "bool DBPS_IsGameRunning();\n",
    "bool DBPS_IsGameRunning();\nvoid DBPS_RequestPostGameReset();\nbool DBPS_ConsumePostGameReset();\nvoid DBPS_ForceResetToMenu();\n",
)

# SOFIA Space: consume after retro_run, on the frontend thread.
replace_once(
    "main/main.cpp",
    "\n\t// Restore SOFI Space only after the launched DOS program has actually run and then exited.\n",
    """
\t// Reset DOSBox Pure after its common post-game finish path, without waiting for a key.
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

\t// Restore SOFI Space only after the launched DOS program has actually run and then exited.
""",
)
