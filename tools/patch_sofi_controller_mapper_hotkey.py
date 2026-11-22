from pathlib import Path

def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one patch anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")

main = Path("main/main.cpp")

replace_once(
    main,
    "static bool SofiL3WasDown[_BIND_PORTS] = {};",
    "static bool SofiL3WasDown[_BIND_PORTS] = {}, SofiR3WasDown[_BIND_PORTS] = {};"
)

replace_once(
    main,
    """\tif (bid == BIND_ID_L3)
\t{
\t\tif (port >= _BIND_PORTS) return 0;
\t\tSJoyBind& l3 = JoyBinds[port][BIND_ID_L3];
\t\tconst bool down = (l3.Joy && l3.GetVal(false));
\t\tconst bool pressed = (down && !SofiL3WasDown[port]);
\t\tSofiL3WasDown[port] = down;
\t\t// L3 is reserved for the native Controller Mapper; never pass it to Pure's Start Menu binding.
\t\tif (pressed && !DBPS_IsShowingOSD()) DBPS_OpenControllerMapper();
\t\treturn 0;
\t}""",
    """\tif (bid == BIND_ID_L3)
\t{
\t\tif (port >= _BIND_PORTS) return 0;
\t\tSJoyBind& l3 = JoyBinds[port][BIND_ID_L3];
\t\tconst bool down = (l3.Joy && l3.GetVal(false));
\t\tconst bool pressed = (down && !SofiL3WasDown[port]);
\t\tSofiL3WasDown[port] = down;
\t\t// L3 is reserved for the native Controller Mapper; never pass it to Pure's Start Menu binding.
\t\tif (pressed && !DBPS_IsShowingOSD()) DBPS_OpenControllerMapper();
\t\treturn 0;
\t}
\tif (bid == BIND_ID_R3)
\t{
\t\tif (port >= _BIND_PORTS) return 0;
\t\tSJoyBind& r3 = JoyBinds[port][BIND_ID_R3];
\t\tconst bool down = (r3.Joy && r3.GetVal(false));
\t\tconst bool pressed = (down && !SofiR3WasDown[port]);
\t\tSofiR3WasDown[port] = down;
\t\t// R3 is reserved for the native on-screen keyboard; never pass it to the emulated program.
\t\tif (pressed && !DBPS_IsShowingOSD()) DBPS_OpenOnScreenKeyboard();
\t\treturn 0;
\t}"""
)

replace_once(
    main,
    "static bool pressedMidiNext, pressedMidiNextF12;",
    "static bool pressedMidiNext, pressedMidiNextF12, pressedControllerMapperF11;"
)

replace_once(
    main,
    """\tconst bool midiNextF12 = (e.key == ZLK_F12 && HotkeyMod != 0 && (mod & HotkeyMod) == HotkeyMod && !(mod & ((ZLKMOD_CTRL|ZLKMOD_SHIFT|ZLKMOD_ALT|ZLKMOD_META|ZLKMOD_MODE)&~HotkeyMod)));""",
    """\tconst bool controllerMapperF11 = (e.key == ZLK_F11 && HotkeyMod != 0 && (mod & HotkeyMod) == HotkeyMod && !(mod & ((ZLKMOD_CTRL|ZLKMOD_SHIFT|ZLKMOD_ALT|ZLKMOD_META|ZLKMOD_MODE)&~HotkeyMod)));
\tif (controllerMapperF11 || pressedControllerMapperF11)
\t{
\t\tif (e.is_down && !pressedControllerMapperF11)
\t\t{
\t\t\tpressedControllerMapperF11 = true;
\t\t\tif (DBPS_IsGameRunning() && !DBPS_IsShowingOSD())
\t\t\t\tDBPS_OpenControllerMapper();
\t\t}
\t\telse if (!e.is_down) pressedControllerMapperF11 = false;
\t\treturn true;
\t}
\tconst bool midiNextF12 = (e.key == ZLK_F12 && HotkeyMod != 0 && (mod & HotkeyMod) == HotkeyMod && !(mod & ((ZLKMOD_CTRL|ZLKMOD_SHIFT|ZLKMOD_ALT|ZLKMOD_META|ZLKMOD_MODE)&~HotkeyMod)));"""
)

replace_once(
    main,
    """\t\t\t\t\tImGui::Text("MIDI NEXT: Scroll Lock  |  Hotkey Modifier + F12");
\t\t\t\t\tImGui::TextDisabled("F12 sin modificador se envía al programa DOS.");""",
    """\t\t\t\t\tImGui::Text("MIDI NEXT: Scroll Lock  |  Hotkey Modifier + F12");
\t\t\t\t\tImGui::Text("Controller Mapper: Hotkey Modifier + F11");
\t\t\t\t\tImGui::TextDisabled("F12 y F11 sin modificador se envían al programa DOS.");"""
)

replace_once(
    main,
    """\t\t\t\t\tImGui::TextDisabled("INPUT  //  CONFIGURACIÓN DEL TECLADO, MOUSE Y CONTROLES");
\t\t\t\t\tImGui::Separator();""",
    """\t\t\t\t\tImGui::TextDisabled("INPUT  //  CONFIGURACIÓN DEL TECLADO, MOUSE Y CONTROLES");
\t\t\t\t\tImGui::TextDisabled("Durante el juego: presiona L3 para abrir la configuración del control.");
\t\t\t\t\tImGui::Separator();"""
)
