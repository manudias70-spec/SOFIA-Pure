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


## Follow-up inspection: SDL/OpenGL implementation

Further inspection of the public ZillaLib source confirms:

- The desktop SDL platform implementation owns a static `SDL_Window*` and creates the OpenGL context in `ZL_CreateWindow`. The main loop calls `ZL_MainApplication->Frame()` and then `SDL_GL_SwapWindow`.
- SDL event polling is centralized in the private `ProcessSDLEvents()` callback, connected to `ZL_Application::sigKeepAlive`. SOFIA should not add a second competing event-pump.
- ZillaLib translates SDL keyboard down/up, text input, pointer movement/buttons, mouse wheel, window resize/focus and joystick changes into public `ZL_Display` signals. These are the preferred input source for a UI adapter.
- The SDL window and context are private implementation details; the inspected public API does not provide their handles. This makes the stock Dear ImGui SDL2 platform backend a poor fit unless ZillaLib itself is extended. That extension is not necessary for the initial spike.
- `ZL_Application.h` selects `ZL_VIDEO_OPENGL2` by default on ordinary desktop builds when no GL mode is explicitly defined. The SDL platform only requests a specific context version/profile for `ZL_VIDEO_OPENGL_CORE` or GLES modes. Therefore the default desktop path is compatibility-style OpenGL, but the actual SOFIA build configuration and runtime GL version still need verification.

### Updated integration direction

Prefer a narrow adapter driven by ZillaLib's public input signals and a renderer tested against the actual desktop GL profile. The Dear ImGui OpenGL2 renderer backend is now a plausible first candidate for the Windows desktop build, but it is not approved until we verify the build's GL defines, confirm required GL entry points, and test state preservation after ZillaLib's game/OSD drawing. Do not add a second SDL event pump or assume access to the private SDL window/context.

### Remaining validation gate

1. Confirm the exact GL-related preprocessor definitions in the SOFIA-Pure Visual Studio project and Makefile.
2. Inspect the application's frame composition and ZillaLib's GL reset/state setup to identify the safest overlay insertion point.
3. Verify resize and input coordinate scaling for the app's actual viewport.
4. Only then implement a compile-time optional diagnostic overlay, leaving the engine and default behavior unchanged.


## SOFIA-Pure build-profile and frame-composition findings

Inspection of the SOFIA-Pure project files adds an important platform distinction:

- The Visual Studio project declares the ordinary `Debug|x64` and `Release|x64` configurations and imports `ZillaApp-vs.props`. The imported props add `ZL_VIDEO_OPENGL_CORE` only for the dedicated `DebugGLCore` / `ReleaseGLCORE` configurations. The ordinary Windows Debug/Release configurations therefore do not explicitly select Core and inherit ZillaLib's desktop OpenGL2 default.
- The Makefile selects exactly one GL context macro and defaults ordinary desktop builds to `ZL_VIDEO_OPENGL_CORE` (with platform exceptions for ARM/mobile-like targets). Therefore Makefile desktop builds and ordinary Visual Studio builds have different default GL profiles.
- In SOFIA-Pure's `OnDraw()`, `retro_run()` and save/load/interface work happen first; the app then calls `ZL_GL_ResetFrameBuffer()`, clears and draws the core image, OSD and the remaining overlays/diagnostics. `AfterFrame()` calls `OnDraw()` and then network polling. The end of `OnDraw()` is the natural place to evaluate an optional SOFIA overlay, after the existing game/OSD composition and before the frame is swapped.
- The symbol `ZL_GL_ResetFrameBuffer()` is declared as an external function at the call site in `main.cpp`; it was not found in the inspected public ZillaLib display/GLSL source files. Its definition and exact GL-state guarantees remain to be located before relying on it as a state boundary.

### Revised build strategy

Treat Windows Visual Studio Debug/Release as the first integration target unless the user chooses another build. Keep Makefile/OpenGL-Core support as a separate compatibility target. Do not silently force one GL profile across both build systems. The first experiment should be compile-time optional and should target the exact profile used by the Windows configuration, with no changes to the emulation core.

### Remaining gate

Locate the implementation of `ZL_GL_ResetFrameBuffer()`, inspect its state reset semantics, and confirm the effective Windows project configuration selected for the user's build. Then prototype a diagnostic overlay behind a build flag and verify it does not disturb the game/OSD renderer or keyboard/mouse/gamepad input.


## Unresolved framebuffer-reset symbol

A targeted scan of the inspected ZillaLib public headers and implementation files did not find a definition of `ZL_GL_ResetFrameBuffer()`. In SOFIA-Pure's tracked `main.cpp`, it appears only as a local `extern` declaration immediately before the call in `OnDraw()`. The Visual Studio project and Makefile both reference the DOSBox Pure core as an external sibling directory (`../dosbox-pure` / `$(DBPDir)`), and that core source is not present in the tracked SOFIA-Pure repository snapshot inspected here.

This means the reset function's implementation and GL-state contract cannot yet be verified from the currently accessible SOFIA-Pure and ZillaLib source. Do not infer that it restores all GL state or use it as an ImGui state boundary. The next source needed is the exact DOSBox Pure core revision used in the user's local build, especially the file defining `ZL_GL_ResetFrameBuffer()`. Once located, inspect its framebuffer binding, viewport, shader/program, texture units, buffers/VAO and blend/depth state behavior before selecting the overlay insertion point.
