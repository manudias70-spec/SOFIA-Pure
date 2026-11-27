from pathlib import Path

def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one patch anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")

header = Path("imgui/backends/imgui_impl_opengl3.h")
source = Path("imgui/backends/imgui_impl_opengl3.cpp")

replace_once(
    header,
    "IMGUI_IMPL_API void     ImGui_ImplOpenGL3_RenderDrawData(ImDrawData* draw_data);",
    "IMGUI_IMPL_API void     ImGui_ImplOpenGL3_RenderDrawData(ImDrawData* draw_data);\nIMGUI_IMPL_API void     ImGui_ImplOpenGL3_SetViewportOffset(int x, int y);"
)
replace_once(
    source,
    '#include "imgui_impl_opengl3.h"\n',
    '#include "imgui_impl_opengl3.h"\n\n'
    'static int SofiViewportOffsetX = 0;\n'
    'static int SofiViewportOffsetY = 0;\n\n'
    'void ImGui_ImplOpenGL3_SetViewportOffset(int x, int y)\n'
    '{\n'
    '    SofiViewportOffsetX = x;\n'
    '    SofiViewportOffsetY = y;\n'
    '}\n'
)
replace_once(
    source,
    "GL_CALL(glViewport(0, 0, (GLsizei)fb_width, (GLsizei)fb_height));",
    "GL_CALL(glViewport(SofiViewportOffsetX, SofiViewportOffsetY, (GLsizei)fb_width, (GLsizei)fb_height));"
)
replace_once(
    source,
    "GL_CALL(glScissor((int)clip_min.x, (int)((float)fb_height - clip_max.y), (int)(clip_max.x - clip_min.x), (int)(clip_max.y - clip_min.y)));",
    "GL_CALL(glScissor(SofiViewportOffsetX + (int)clip_min.x, SofiViewportOffsetY + (int)((float)fb_height - clip_max.y), (int)(clip_max.x - clip_min.x), (int)(clip_max.y - clip_min.y)));"
)
print("Applied SOFIA Space proportional viewport and scissor offsets to ImGui OpenGL3 backend")
