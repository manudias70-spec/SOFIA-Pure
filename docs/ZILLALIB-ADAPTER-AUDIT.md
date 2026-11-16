# ZillaLib adapter audit for SOFIA-Pure

Status: source-level audit of the checked-in ZillaLib repository; no application or engine code changed.

## Repositories and build relationship

- SOFIA-Pure references the sibling dependency as `../ZillaLib` in `DOSBoxPure-vs.vcxproj`.
- That project imports `$(ZillaLibDir)/ZillaApp-vs.props`.
- The dependency repository available under the project owner's GitHub account is `manudias70-spec/ZillaLib`, default branch `main`.
- ZillaLib public headers are under `Include/`; implementation sources are under `Source/`.

## Confirmed public integration surface

- `Include/ZL_Application.h` defines the `ZL_Application` lifecycle and chooses a desktop default of `ZL_VIDEO_OPENGL2` unless another GL mode is explicitly defined. This is a compile-time default, not proof of the exact runtime GL version/profile.
- `Include/ZL_Display.h` exposes `ZL_Display::Init(...)`, display dimensions, and input/event signals.
- `Source/ZL_Display.cpp` defines the public input signals and translates ZillaLib events into them. The signal set includes key down/up, text input, pointer move/down/up, mouse wheel, resize, activation/focus, joystick changes, and file drop.
- `ZL_Display::Init` delegates window creation to the internal `ZL_CreateWindow(...)` implementation and then initializes ZillaLib's GL rendering/shaders.
- The inspected public headers do not expose an SDL_Window or SDL_GLContext handle, nor a public API for attaching an SDL event watcher or obtaining the native event queue.

## Consequence for Dear ImGui

The stock Dear ImGui SDL2 platform backend cannot yet be wired directly through the public ZillaLib API: the necessary SDL window handle and direct SDL event stream are not part of the inspected public surface.

A narrower SOFIA-Pure adapter is the better first experiment:

1. Feed ImGui input from ZillaLib's public signals (keyboard, text, pointer, wheel, focus, resize). Translate coordinate origin and scale carefully; ZillaLib converts pointer Y to a bottom-left origin.
2. Use a renderer compatible with the actual ZillaLib desktop GL mode. The desktop header default is OpenGL 2, so investigate the Dear ImGui OpenGL2 renderer backend first rather than assuming OpenGL3.
3. Keep rendering in the existing application frame, after the current game/OSD composition, with explicit GL-state isolation/restoration.
4. Add input arbitration so ImGui can capture pointer/keyboard input without accidentally sending the same interaction to DOSBox/game controls.
5. Keep the adapter behind a compile-time feature flag and leave the emulation core, libretro callbacks, game surface, and OSD data path untouched.

## Remaining verification gate

Before writing the adapter, inspect the active Windows GL implementation and frame/swap sequence to verify:
- exact GL context/version/profile and whether compatibility functions are available;
- whether the renderer can safely draw after ZillaLib's own draw calls and before swap;
- how GL state is reset/restored by ZillaLib;
- whether the input signal API exposes all key/modifier details needed by ImGui;
- how window resizing and high-DPI scaling are represented.

Do not add ImGui source files or alter build files until these points are checked. Do not change the default branch until a real build and runtime test pass.
