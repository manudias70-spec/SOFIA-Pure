from pathlib import Path

def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one patch anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")

main = Path("main/main.cpp")

# SOFI OSD: present all shortcuts as a compact list, including Controller Mapper.
replace_once(
    main,
    """\t\t\t\t\tImGui::Text("F1  Pausa  |  F2  Cámara lenta  |  F3  Avance rápido");
\t\t\t\t\tImGui::Text("F5  Guardado rápido  |  F7  Pantalla completa  |  F9  Carga rápida");
\t\t\t\t\tImGui::Text(SofiText("MIDI NEXT: Scroll Lock  |  Modificador de atajo + F12", "MIDI NEXT: Scroll Lock  |  Hotkey Modifier + F12"));
\t\t\t\t\tImGui::Text(SofiText("Controller Mapper: Modificador de atajo + F11", "Controller Mapper: Hotkey Modifier + F11"));
\t\t\t\t\tImGui::TextDisabled(SofiText("F11 y F12 sin modificador se envían al programa DOS.", "F11 and F12 without a modifier are sent to the DOS program."));""",
    """\t\t\t\t\tImGui::BulletText(SofiText("F1: Pausa", "F1: Pause"));
\t\t\t\t\tImGui::BulletText(SofiText("F2: Cámara lenta", "F2: Slow motion"));
\t\t\t\t\tImGui::BulletText(SofiText("F3: Avance rápido", "F3: Fast forward"));
\t\t\t\t\tImGui::BulletText(SofiText("F5: Guardado rápido", "F5: Quick save"));
\t\t\t\t\tImGui::BulletText(SofiText("F7: Pantalla completa", "F7: Fullscreen"));
\t\t\t\t\tImGui::BulletText(SofiText("F9: Carga rápida", "F9: Quick load"));
\t\t\t\t\tImGui::BulletText(SofiText("MIDI NEXT: Scroll Lock : Modificador de atajo + F12", "MIDI NEXT: Scroll Lock : Hotkey Modifier + F12"));
\t\t\t\t\tImGui::BulletText(SofiText("Controller Mapper: Modificador de atajo + F11", "Controller Mapper: Hotkey Modifier + F11"));
\t\t\t\t\tImGui::TextDisabled(SofiText("F11 y F12 sin modificador se envían al programa DOS.", "F11 and F12 without a modifier are sent to the DOS program."));"""
)

# Move the complete ATAJOS section to the very beginning of SOFI OSD.
shortcut_section = """\t\t\t\t\tImGui::Separator();
\t\t\t\t\tImGui::TextColored(ImVec4(0.25f, 0.75f, 1.0f, 1.0f), "ATAJOS");
\t\t\t\t\tImGui::BulletText(SofiText("F1: Pausa", "F1: Pause"));
\t\t\t\t\tImGui::BulletText(SofiText("F2: Cámara lenta", "F2: Slow motion"));
\t\t\t\t\tImGui::BulletText(SofiText("F3: Avance rápido", "F3: Fast forward"));
\t\t\t\t\tImGui::BulletText(SofiText("F5: Guardado rápido", "F5: Quick save"));
\t\t\t\t\tImGui::BulletText(SofiText("F7: Pantalla completa", "F7: Fullscreen"));
\t\t\t\t\tImGui::BulletText(SofiText("F9: Carga rápida", "F9: Quick load"));
\t\t\t\t\tImGui::BulletText(SofiText("MIDI NEXT: Scroll Lock : Modificador de atajo + F12", "MIDI NEXT: Scroll Lock : Hotkey Modifier + F12"));
\t\t\t\t\tImGui::BulletText(SofiText("Controller Mapper: Modificador de atajo + F11", "Controller Mapper: Hotkey Modifier + F11"));
\t\t\t\t\tImGui::TextDisabled(SofiText("F11 y F12 sin modificador se envían al programa DOS.", "F11 and F12 without a modifier are sent to the DOS program."));"""

replace_once(main, shortcut_section, "")
replace_once(
    main,
    """\t\t\t\t\tImGui::TextColored(ImVec4(0.25f, 0.75f, 1.0f, 1.0f), "HOTKEYS");""",
    shortcut_section + """
\t\t\t\t\tImGui::Separator();
\t\t\t\t\tImGui::TextColored(ImVec4(0.25f, 0.75f, 1.0f, 1.0f), "HOTKEYS");"""
)

# SOFI UI > INPUT: ordinary informative text with plain colon punctuation.
replace_once(
    main,
    """\t\t\t\t\tImGui::TextDisabled(SofiText("Durante el juego: presioná L3 para abrir la configuración del control.", "In-game: press L3 to open controller configuration."));""",
    """\t\t\t\t\tImGui::Text(SofiText("JOYSTICK:", "JOYSTICK:"));
\t\t\t\t\tImGui::Text(SofiText("L3: Abrir Controller Mapper durante el juego.", "L3: Open Controller Mapper while in-game."));
\t\t\t\t\tImGui::Text(SofiText("R3: Abrir teclado en pantalla durante el juego.", "R3: Open the on-screen keyboard while in-game."));
\t\t\t\t\tImGui::Text(SofiText("TECLADO:", "KEYBOARD:"));
\t\t\t\t\tImGui::Text(SofiText("Modificador de atajo + F11: Abrir Controller Mapper.", "Hotkey Modifier + F11: Open Controller Mapper."));"""
)
