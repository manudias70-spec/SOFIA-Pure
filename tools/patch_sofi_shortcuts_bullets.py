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
\t\t\t\t\tImGui::Text("MIDI NEXT: Scroll Lock  |  Hotkey Modifier + F12");
\t\t\t\t\tImGui::Text("Controller Mapper: Hotkey Modifier + F11");
\t\t\t\t\tImGui::TextDisabled("F12 y F11 sin modificador se envían al programa DOS.");""",
    """\t\t\t\t\tImGui::BulletText("F1: Pausa");
\t\t\t\t\tImGui::BulletText("F2: Cámara lenta");
\t\t\t\t\tImGui::BulletText("F3: Avance rápido");
\t\t\t\t\tImGui::BulletText("F5: Guardado rápido");
\t\t\t\t\tImGui::BulletText("F7: Pantalla completa");
\t\t\t\t\tImGui::BulletText("F9: Carga rápida");
\t\t\t\t\tImGui::BulletText("MIDI NEXT: Scroll Lock : Hotkey Modifier + F12");
\t\t\t\t\tImGui::BulletText("Controller Mapper: Hotkey Modifier + F11");
\t\t\t\t\tImGui::TextDisabled("F11 y F12 sin modificador se envían al programa DOS.");"""
)

# Move the complete ATAJOS section to the very beginning of SOFI OSD.
shortcut_section = """\t\t\t\t\tImGui::Separator();
\t\t\t\t\tImGui::TextColored(ImVec4(0.25f, 0.75f, 1.0f, 1.0f), "ATAJOS");
\t\t\t\t\tImGui::BulletText("F1: Pausa");
\t\t\t\t\tImGui::BulletText("F2: Cámara lenta");
\t\t\t\t\tImGui::BulletText("F3: Avance rápido");
\t\t\t\t\tImGui::BulletText("F5: Guardado rápido");
\t\t\t\t\tImGui::BulletText("F7: Pantalla completa");
\t\t\t\t\tImGui::BulletText("F9: Carga rápida");
\t\t\t\t\tImGui::BulletText("MIDI NEXT: Scroll Lock : Hotkey Modifier + F12");
\t\t\t\t\tImGui::BulletText("Controller Mapper: Hotkey Modifier + F11");
\t\t\t\t\tImGui::TextDisabled("F11 y F12 sin modificador se envían al programa DOS.");"""

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
    """\t\t\t\t\tImGui::TextDisabled("Durante el juego: presiona L3 para abrir la configuración del control.");""",
    """\t\t\t\t\tImGui::Text("JOYSTICK:");
\t\t\t\t\tImGui::Text("L3: Abrir Controller Mapper durante el juego.");
\t\t\t\t\tImGui::Text("TECLADO:");
\t\t\t\t\tImGui::Text("Hotkey Modifier + F11: Abrir Controller Mapper.");"""
)
