# Dear ImGui vendored for SOFIA-Pure

- Upstream: https://github.com/ocornut/imgui
- Pinned release: `v1.91.9b`
- License: MIT (see `LICENSE.txt`)
- Integration target: Windows desktop, ZillaLib OpenGL Core context
- Renderer backend: `backends/imgui_impl_opengl3.cpp`
- GLSL version passed by SOFIA UI: `#version 140`

Only the Dear ImGui core translation units and OpenGL3 renderer backend are compiled by the Windows Visual Studio project. No SDL2 platform backend is included: window creation, event pumping and presentation remain owned by ZillaLib.

Keep this directory pinned to the stated upstream release unless the backend compatibility audit and Windows CI build are repeated.
