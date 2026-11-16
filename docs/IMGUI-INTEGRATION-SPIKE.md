# SOFIA-Pure — Dear ImGui Integration Spike

Status: architecture investigation only. No application source, build configuration, or emulator code has been changed.

Target branch: `feature/sofia-ui-redesign`

## Decision

Keep ZillaLib as the application/window/rendering host for the first integration experiment. Do not replace it as part of the initial UI redesign.

Evaluate Dear ImGui as an optional presentation layer rendered after the existing game/OSD composition. The integration must be isolated behind a small SOFIA-Pure UI adapter so it can be disabled at build time and removed without affecting the emulator.

## What the current frontend confirms

- The application derives `sDOSBoxPure` from `ZL_Application`.
- Window creation, input initialization, key events, resize notifications, joystick setup, and the application frame lifecycle are managed through ZillaLib.
- The frame callback is `AfterFrame()`, which calls `OnDraw()`.
- `OnDraw()` runs `retro_run()`, resets the GL framebuffer, then draws the game surface, OSD bitmap, notifications, and diagnostics.
- DOSBox Pure supplies the OSD bitmap through `DBPS_SubmitOSDFrame()`; the frontend does not generate the OSD menu contents.
- The project currently has no Dear ImGui sources or build dependency.

## Integration constraints to prove before coding

1. **Graphics context ownership:** identify how ZillaLib creates and retains the SDL window and GL context, and confirm which GL profile is used by each supported build.
2. **Event ownership:** ZillaLib owns the SDL event loop. Do not add a second event-polling loop. Determine whether its SDL events can be forwarded safely to ImGui, or whether a thin platform adapter should feed ImGui from existing ZillaLib input callbacks.
3. **Render-state isolation:** ImGui rendering must preserve/restore the GL state used by ZillaLib. It must not disturb the emulator texture, OSD texture, shaders, viewport, framebuffer, or swap lifecycle.
4. **Input arbitration:** when the new SOFIA-Pure UI is active, keyboard/mouse/gamepad events consumed by UI controls must not leak into the emulated machine. When the UI is hidden, existing input behavior must remain unchanged.
5. **Build isolation:** add ImGui as a separate dependency/target group; do not modify the DOSBox Pure source list or its compile definitions.

## Preferred experiment

Create a minimal, compile-time optional ImGui overlay that only displays a small diagnostic panel. Do not create the desktop shell or game explorer in this spike.

- Initialize and shut down the ImGui context with the application lifecycle.
- Start and render the ImGui frame at a point that is known to have the correct GL context current and after the existing scene composition.
- First test mouse and keyboard capture without forwarding captured events to DOSBox Pure.
- Validate window resize, fullscreen, controller input, mouse capture, OSD visibility, game video, audio, and frame pacing.

## Backend strategy

Do not assume that the stock SDL2 + OpenGL3 backends can be dropped in unchanged. They normally expect access to an SDL_Window, an SDL_GLContext, and the SDL event stream. Those handles and event-pump ownership have not yet been proven available through the current ZillaLib integration.

First inspect ZillaLib's public API and platform implementation. Then choose, in order:

1. Standard Dear ImGui SDL2/OpenGL3 backends if the required window/context/event hooks are safely accessible.
2. A narrow SOFIA-Pure platform adapter using existing ZillaLib input callbacks, paired with a renderer compatible with the actual GL context.
3. A different UI approach only if the first two cannot be integrated without invasive changes.

## Non-negotiable boundaries

- No changes to CPU, memory, devices, timing, audio mixing, libretro callbacks, game loading, save states, or filesystem behavior.
- Do not change `DBPS_SubmitOSDFrame()` or the existing game/OSD rendering path for this experiment.
- No replacement of ZillaLib in the initial spike.
- No changes to the default branch until the experiment is built and validated.

## Next implementation gate

Before adding ImGui source files, document the exact ZillaLib APIs or SDL handles available for:
- current window and GL context;
- event forwarding or input callbacks;
- framebuffer/GL state boundaries;
- frame timing and resize.

Only proceed to the diagnostic overlay once those are verified.


## Source audit: stock Dear ImGui backends

Audited the upstream `backends/imgui_impl_opengl3.cpp` and `backends/imgui_impl_sdl2.cpp` sources on 2026-11-16. This is a source review, not a build or runtime test; the project has not selected or pinned an ImGui revision yet.

### OpenGL renderer findings

The current OpenGL3 renderer explicitly backs up and restores the state it changes, including:
- active texture unit, program, texture binding on texture unit 0, and sampler binding where supported;
- array/element buffer and VAO state (or the relevant vertex attribute state on paths without VAOs);
- viewport and scissor rectangle;
- blend factors/equations and enable flags for blend, cull, depth, stencil, and scissor;
- polygon mode and primitive-restart enable state where supported.

It configures blend, cull, depth, stencil, scissor, viewport, shader, buffers/vertex attributes and texture bindings for its draw. It does not bind a different framebuffer, and the inspected render path does not modify depth function or depth write mask. Those facts are important because `ZL_GL_ResetFrameBuffer()` sets the framebuffer, viewport, blend, depth/cull baseline, and depth mask before the app draws its frame.

This makes the upstream OpenGL3 renderer a promising candidate: it has a deliberate state backup/restore path rather than relying on `ZL_GL_ResetFrameBuffer()` afterward. However, the state contract must be rechecked against the exact pinned ImGui revision and the exact ZillaLib GL profile. Do not assume it preserves arbitrary GL state it does not modify.

### SDL platform backend findings

`ImGui_ImplSDL2_ProcessEvent()` consumes an SDL event supplied by the caller; the backend does not require a second SDL event-polling loop. Its OpenGL initialization still requires an `SDL_Window*` and `SDL_GLContext`. ZillaLib's inspected public API does not expose those handles, and ZillaLib owns SDL event dispatch.

Therefore the preferred first experiment is:
- use the Dear ImGui OpenGL renderer backend only, if its GL requirements match the actual context;
- implement a narrow SOFIA-Pure platform/input adapter fed by ZillaLib's public keyboard, text, mouse, wheel, focus, resize and timing signals;
- do not access SDL internals, create another event loop, or modify ZillaLib merely to obtain SDL handles.

### Remaining compatibility checks

1. Verify the exact desktop GL version/profile and available entry points for the user's actual Visual Studio configuration. The `ZL_VIDEO_OPENGL2` and `ZL_VIDEO_OPENGL_CORE` build paths must not be conflated.
2. Pin a specific Dear ImGui revision and inspect its OpenGL renderer code at that revision.
3. Verify how ZillaLib reports mouse coordinates, logical/display dimensions, focus and text input so the adapter can supply correct ImGui IO values.
4. Verify event ordering and capture arbitration so UI-consumed keyboard/mouse input does not reach the emulated machine.
5. Only then add a compile-time optional diagnostic panel and build it on the user's target configuration.

No application, build, ZillaLib, or emulation-core code has been modified. This update is documentation only.


## Windows Visual Studio configuration and input API audit

Inspected the actual `DOSBoxPure-vs.vcxproj`, its imported `ZillaApp-vs.props`, and ZillaLib public headers.

### GL profile selection

- The SOFIA-Pure Visual Studio project imports `$(ZillaLibDir)/ZillaApp-vs.props`.
- The standard Visual Studio `Debug` and `Release` configurations do not add `ZL_VIDEO_OPENGL_CORE`; on desktop they therefore use ZillaLib's default `ZL_VIDEO_OPENGL2` path.
- The optional `DebugGLCORE` / `ReleaseGLCORE` configurations add `ZL_VIDEO_OPENGL_CORE`.
- The imported props file has a case variation in the spelling of the Debug GLCORE condition (`DebugGLCORE` vs `DebugGLCore`); MSBuild condition string comparisons are case-insensitive, but this should be cleaned up only if a future build-system change is actually needed. No change is proposed now.

The repository alone cannot tell us which configuration the user currently builds or runs. The first prototype must target the actual selected configuration, not assume the Core profile. For the lowest-risk first pass, use the existing standard Windows Debug configuration unless the user's normal workflow is known to use another one.

### Public input and display interface

ZillaLib publicly exposes:
- `ZL_Display::sigKeyDown` / `sigKeyUp`;
- `sigTextInput`;
- `sigPointerMove`, `sigPointerDown`, `sigPointerUp`;
- `sigMouseWheel`;
- `sigActivated` and `sigResized`;
- current pointer coordinates, key/button state, display width/height and focus queries.

This is sufficient in principle to build a platform adapter without polling SDL independently. Exact event field semantics, coordinate scaling, key mapping and input-capture ordering still need inspection before implementation.

### Render placement and input routing constraints

The existing `OnDraw()` calls `retro_run()`, applies save/load and geometry/interface changes, calls `ZL_GL_ResetFrameBuffer()`, then composes the game image and OSD. The ImGui draw call should be evaluated after all existing game/OSD/notification/diagnostic drawing and before the frame returns to ZillaLib for presentation.

Input must be arbitrated before it reaches existing DOSBox hotkey and emulated-input handlers: when the SOFIA UI owns keyboard or pointer interaction, consumed events must not leak into the emulated machine. The current code also uses pointer lock and direct SDL cursor calls in the host, so overlay mode must deliberately suspend or coordinate pointer lock rather than fighting it.

No source, project, build, or engine code was changed. This remains a documentation-only audit. No compilation or runtime test has been performed.


## Follow-up audit: actual context and input boundaries

Inspected the current ZillaLib SDL implementation, public event structures, and the SOFIA-Pure frontend callbacks.

### Actual GL context request

- With `ZL_VIDEO_OPENGL_CORE`, ZillaLib requests an OpenGL **3.1 Core** context through SDL.
- With the desktop `ZL_VIDEO_OPENGL2` path, ZillaLib does **not** set an explicit GL version or profile in the inspected SDL creation path. The resulting compatibility context is therefore platform/driver dependent and must be queried at runtime; it is not safe to assume a specific GLSL version from the macro name alone.
- ZillaLib creates the SDL GL context internally, but the inspected implementation does not retain the return value from `SDL_GL_CreateContext()` in a public handle. The SDL window pointer is also private to the platform source.
- Consequently, the standard ImGui SDL2 platform backend cannot be initialized from SOFIA-Pure without reaching into ZillaLib internals. That remains outside the preferred integration boundary.

### Public event data and the real input path

ZillaLib's public event structures provide the fields needed for a small adapter:
- keyboard: `is_down`, `is_repeat`, key and modifier mask;
- pointer motion: absolute and relative coordinates plus button-state bits;
- pointer button: button, down/up state and coordinates;
- wheel: horizontal and vertical deltas;
- window resize: previous dimensions plus fullscreen/maximized flags;
- activation: keyboard focus, mouse focus and minimized/maximized state.

Important limitation: these signals do not expose a general-purpose “consumed” return value. In SOFIA-Pure, `OnKeyDown()` and `OnKeyUp()` currently pass keyboard events into the libretro keyboard callback after hotkey handling. Therefore UI capture must be implemented explicitly in the SOFIA-Pure frontend callbacks; merely subscribing another listener to the same ZillaLib signal will not prevent the event reaching DOSBox.

Mouse input has a separate, critical path: `retro_input_state_cb()` polls `ZL_Input::MouseDelta()`, `Held()`, `MouseWheel()`, and pointer position directly. UI capture must gate those libretro mouse/pointer reads while the UI owns the pointer. Otherwise clicks and movement can leak into the emulated game even if pointer events were also delivered to ImGui.

### Pointer-lock coordination

The existing frontend applies pointer lock and cursor visibility from `OnDraw()`, based on the DOSBox OSD state, pause state and its pointer-lock option. The SOFIA-Pure UI needs an explicit ownership state:
- when the UI is interactive, release the game's pointer lock and expose the cursor;
- while the UI is closed, preserve the existing pointer-lock and cursor behavior;
- do not change the core's OSD behavior or mouse emulation policy outside this frontend arbitration.

### Updated implementation gate

The next safe implementation is still a compile-time optional frontend-only adapter and diagnostic panel. Before source changes, the build target must be identified: Windows Visual Studio standard configurations request the GL2 path, Windows GLCORE configurations request 3.1 Core, and the Makefile can select a different default according to target platform. The actual Git-based build job/configuration has not yet been identified.

No application source, build configuration, ZillaLib source, or DOSBox Pure core code has been modified. This remains a source audit only; no build or runtime test has been performed.


## GitHub Actions build target verified

The repository workflow `.github/workflows/build.yml` was inspected on both `main` and `feature/sofia-ui-redesign`; the file is identical (blob `fa561c53b21201adbdf453df93f08462f598b068`).

### Triggers and source checkout

- Automatic runs occur on pushes to `main` and pull requests targeting `main`.
- The workflow also declares `workflow_dispatch` with an optional version string.
- The checked-out SOFIA-Pure source is placed in the runner's `main/` directory. Thus a PR build checks out the PR source, not an unrelated local Visual Studio configuration.
- A push directly to `feature/sofia-ui-redesign` does not match the automatic push trigger. To build this branch, it needs a PR targeting `main` or a manually dispatched run selecting the branch.

### Windows build profile — decisive result

Both Windows jobs use MSBuild with `/p:Configuration=ReleaseGLCORE`:
- Win64: `/p:Platform=x64`
- Win32: `/p:Platform=Win32`
- Windows ARM64: `/p:Platform=ARM64`, also applying ARM64 project substitutions.

Therefore the principal Windows CI target is **ReleaseGLCORE**, not standard Release/GL2. This resolves the earlier uncertainty for the Windows artifacts produced by this workflow.

### Other CI targets

- Linux x64: `make linux-release -j4 ZL_VIDEO_OPENGL_CORE=1` (GL Core).
- Linux ARM64: regular CI build uses `ZL_VIDEO_OPENGL_ES2=1`; release/versioned build additionally produces GL Core and GLES2 artifacts.
- macOS x64 and ARM64: `make macos-release` without an explicit GL override in the workflow.

### Dependency reproducibility note

Each job clones `dosbox-pure` and `ZillaLib` from the owner's `main` branch at run time with `--depth 1`. Those dependency revisions are not pinned to immutable SHAs by this workflow. The workflow references the public `dosbox-pure` repository; the separately available private `dosbox-unleashed` repository is not named in these clone commands. This distinction should be preserved until the intended source relationship is verified.

### What this changes for the UI spike

Use **Windows x64 ReleaseGLCORE** as the first CI compatibility target for the ImGui renderer adapter, then validate Win32 and ARM64. Linux x64 GL Core is a useful second target. Keep the adapter frontend-only and optional; do not change the DOSBox core or dependency checkout policy as part of the first UI prototype.

No workflow or application code was changed. This was a read-only audit; no workflow run was started and no build has been executed by this audit.


## Pinned renderer candidate: Dear ImGui v1.91.9b

Inspected the exact upstream tag `v1.91.9b` rather than relying on the moving default branch.

- Tag: `v1.91.9b`
- Renderer source blob: `7d0b53621960d4f86f54077f7fdc8dda88bbece7` (the tag's Git commit SHA was not independently resolved in this audit)
- Renderer source: `backends/imgui_impl_opengl3.cpp`
- The backend contains its own small OpenGL loader in `imgui_impl_opengl3_loader.h`; it does not require ZillaLib's private SDL window/context handles and does not require the frontend to expose ZillaLib's function-pointer globals.
- The loader is deliberately isolated to the renderer translation unit. Keep ImGui's renderer backend in its own .cpp compilation unit; do not amalgamate it with ZillaLib GL headers or sources.
- The backend supports desktop OpenGL 3.1. Its own GLSL compatibility table maps GL 3.1 to GLSL 1.40, so initialize it explicitly with `ImGui_ImplOpenGL3_Init("#version 140")` for the ReleaseGLCORE target.
- OpenGL 3.1 support includes the primitive-restart state path. The backend only enables its base-vertex draw path on GL 3.2+, so the 3.1 target does not assume that later core feature.
- Its render path backs up and restores the GL state it changes. This remains preferable to trying to use `ZL_GL_ResetFrameBuffer()` as a restore operation; that ZillaLib function establishes a baseline and does not restore arbitrary prior state.

### Decision for the first CI prototype

Use Dear ImGui v1.91.9b, the OpenGL3 renderer backend only, and GLSL `#version 140` for the first Windows x64 `ReleaseGLCORE` diagnostic-overlay experiment. Feed ImGui through a SOFIA-Pure adapter using ZillaLib's public signals and frame timing. Do not use the stock SDL2 platform backend, do not create another GL context or SDL event loop, and do not modify ZillaLib or the DOSBox Pure core.

This is a source-level compatibility decision only. The tag has not been vendored, linked, compiled, or run in SOFIA-Pure. Input capture, mouse coordinate scaling, frame ordering, and actual CI validation remain open gates.

No application or build source has been modified; this update records the chosen integration candidate and its rationale.
