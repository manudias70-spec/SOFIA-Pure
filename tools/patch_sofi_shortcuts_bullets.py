from pathlib import Path

def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one patch anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")

main = Path("main/main.cpp")

# SOFI OSD: keep ATAJOS at its existing top position, but give every shortcut
# its own bullet and line. The section order and all shortcut behavior stay intact.
replace_once(
    main,
    """\t\t\t\t\tImGui::Text("F1  Pausa  |  F2  Cámara lenta  |  F3  Avance rápido");
\t\t\t\t\tImGui::Text("F5  Guardado rápido  |  F7  Pantalla completa  |  F9  Carga rápida");
\t\t\t\t\tImGui::Text("MIDI NEXT: Scroll Lock  |  Hotkey Modifier + F12");
\t\t\t\t\tImGui::Text("Controller Mapper: Hotkey Modifier + F11");
\t\t\t\t\tImGui::TextDisabled("F12 y F11 sin modificador se envían al programa DOS.");""",
    """\t\t\t\t\tImGui::BulletText("F1 — Pausa");
\t\t\t\t\tImGui::BulletText("F2 — Cámara lenta");
\t\t\t\t\tImGui::BulletText("F3 — Avance rápido");
\t\t\t\t\tImGui::BulletText("F5 — Guardado rápido");
\t\t\t\t\tImGui::BulletText("F7 — Pantalla completa");
\t\t\t\t\tImGui::BulletText("F9 — Carga rápida");
\t\t\t\t\tImGui::BulletText("MIDI NEXT — Scroll Lock | Hotkey Modifier + F12");
\t\t\t\t\tImGui::BulletText("Controller Mapper — Hotkey Modifier + F11");
\t\t\t\t\tImGui::TextDisabled("F11 y F12 sin modificador se envían al programa DOS.");"""
)

# SOFI UI > INPUT: device headings with indented sub-bullets.
replace_once(
    main,
    """\t\t\t\t\tImGui::TextDisabled("Durante el juego: presiona L3 para abrir la configuración del control.");""",
    """\t\t\t\t\tImGui::BulletText("JOYSTICK");
\t\t\t\t\tImGui::Indent();
\t\t\t\t\tImGui::BulletText("L3 — Abrir Controller Mapper durante el juego.");
\t\t\t\t\tImGui::Unindent();
\t\t\t\t\tImGui::BulletText("TECLADO");
\t\t\t\t\tImGui::Indent();
\t\t\t\t\tImGui::BulletText("Hotkey Modifier + F11 — Abrir Controller Mapper.");
\t\t\t\t\tImGui::Unindent();"""
)
